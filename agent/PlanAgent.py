import os;
from dotenv import load_dotenv
from LLMClient import LLMClient
from typing import List
#from constant import system_prompt
from ToolExecutor import ToolExecutor

load_dotenv()  

PLANNER_PROMPT_TEMPLATE = """
你是一个顶级的AI规划专家。你的任务是将用户提出的复杂问题分解成一个由多个简单步骤组成的行动计划。

## 可用工具
{tools}

## 任务要求
1. 将复杂问题拆解为逻辑清晰、可执行的子步骤。
2. 每个步骤必须是独立的，且包含足够的信息。
3. 步骤之间必须有明确的逻辑顺序。
4. **最后一个步骤必须是根据前面的信息生成最终答案**。
5. 只需要输出计划列表，不要包含任何解释或其他内容。
6. 如果可以通过工具直接解决，步骤可以包含对工具的使用描述。

## 输出格式
请严格按照以下格式输出（Python列表格式）：
```python
[
    "步骤1描述",
    "步骤2描述",
    ...
]
```

## 示例
问题: 比较iPhone 15和华为Mate 60的参数。
```python
[
    "搜索iPhone 15的主要参数配置",
    "搜索华为Mate 60的主要参数配置",
    "对比两款手机的处理器、屏幕、摄像头和电池等关键参数",
    "总结两款手机的优缺点差异"
]
```

## 当前任务
问题: {question}
提醒：{reflection}

"""

EXECUTOR_PROMPT_TEMPLATE = """
你是一个执行代理，负责执行计划中的某一个步骤。

## 可用工具
{tools}

## 执行说明
你可以使用工具来辅助完成任务。如果不需要工具，直接回答即可。

## 回应格式
Thought: 思考当前步骤需要做什么。
Action: 采取的行动，必须是以下格式之一：
- `{{tool_name}}[{{tool_input}}]`: 调用工具。例如 `search[OpenAI 2025 models]`
- `Finish[内容]`: 步骤执行完成，返回结果。

## 上下文信息
{context}

## 当前步骤任务
{step}
"""

class Planner:
    """
    规划器类，负责生成解决问题的步骤计划。
    """
    def __init__(self, llmclient: LLMClient, tool_executor: ToolExecutor):
        """
        初始化规划器。

        Args:
            llmclient (LLMClient): LLM客户端实例。
            tool_executor (ToolExecutor): 工具执行器实例。
        """
        self.llmclient = llmclient
        self.tool_executor = tool_executor
    
    def plan(self, question: str, reflection: str = "") -> List[str]:
        """
        根据问题生成计划。

        Args:
            question (str): 用户的问题。
            reflection (str): 可选的反思内容，用于优化计划。

        Returns:
            List[str]: 计划步骤列表。如果生成失败，返回空列表。
        """
        tools_desc = self.tool_executor.get_tools()
        messages = [
            #{"role": "system", "content": system_prompt},
            {"role": "user", "content": PLANNER_PROMPT_TEMPLATE.format(
                question=question, 
                reflection=reflection,
                tools=tools_desc
            )}
        ]
        response_text = self.llmclient.think(messages)
        if not response_text:
            return []
        
        try:
            # 清理可能存在的markdown代码块标记
            response_text = response_text.replace("```python", "").replace("```", "").strip()
            plan = eval(response_text)
            return plan
        except Exception as e:
            print(f"无法解析计划: {e}")
            return []

class Executor:
    """
    执行器类，负责按顺序执行计划中的步骤。
    """
    def __init__(self, llmclient: LLMClient, tool_executor: ToolExecutor):
        """
        初始化执行器。

        Args:
            llmclient (LLMClient): LLM客户端实例。
            tool_executor (ToolExecutor): 工具执行器实例。
        """
        self.llmclient = llmclient
        self.tool_executor = tool_executor
    
    def _parse_response(self, response_text: str):
        import re
        thought_match = re.search(r"Thought: (.*)", response_text, re.DOTALL)
        action_match = re.search(r"Action: (.*)", response_text, re.DOTALL)
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        return thought, action

    def _parse_action(self, action: str):
        import re
        match = re.match(r"(\w+)\[(.*)\]", action, re.DOTALL)
        if match:
            return match.group(1), match.group(2)
        return None, None

    def execute(self, plan: List[str]) -> str:
        """
        执行计划。

        Args:
            plan (List[str]): 计划步骤列表。

        Returns:
            str: 最后一个步骤的执行结果作为最终答案。
        """
        context = ""  # 用于存储之前步骤的执行结果
        last_step_result = ""
        tools_desc = self.tool_executor.get_tools()

        for i, step in enumerate(plan):
            print(f"\n正在执行步骤 {i+1}/{len(plan)}: {step}")
            
            # 步骤内的微循环 (ReAct loop)
            step_history = []
            max_step_turns = 3
            step_result = ""
            
            for turn in range(max_step_turns):
                prompt = EXECUTOR_PROMPT_TEMPLATE.format(
                    tools=tools_desc,
                    context=f"前序步骤及结果：\n{context}" if context else "无前序步骤",
                    step=step
                )
                if step_history:
                    prompt += "\n\nStep Execution History:\n" + "\n".join(step_history)

                messages = [
                    #{"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
                
                response_text = self.llmclient.think(messages)
                if not response_text:
                    print(f"步骤 {step} 执行失败，无返回内容")
                    break
                
                print(f"Loop {turn+1}: {response_text}")
                
                thought, action = self._parse_response(response_text)
                if not action:
                    # 如果没有标准的Action格式，直接将回复作为结果
                    step_result = response_text
                    break
                
                if action.startswith("Finish"):
                    import re
                    match = re.match(r"Finish\[(.*)\]", action, re.DOTALL)
                    if match:
                        step_result = match.group(1)
                    else:
                        step_result = action # Fallback
                    break
                
                # 执行工具
                tool_name, tool_input = self._parse_action(action)
                if tool_name:
                    tool_func = self.tool_executor.get_tool(tool_name)
                    if tool_func:
                        obs = tool_func(tool_input)
                    else:
                        obs = f"工具 {tool_name} 不存在"
                    print(f"观察结果: {obs}")
                    step_history.append(f"Thought: {thought}\nAction: {action}\nObservation: {obs}")
                else:
                     step_history.append(f"Thought: {thought}\nAction: {action}\nError: 无法解析Action")

            if not step_result: 
                 # 如果循环结束还没结果，取最后一次Observation或Thought
                 step_result = "步骤执行完成，但未明确返回Finish。"

            # 更新上下文和日志
            print(f"步骤 {i+1} 结果: {step_result}")
            context += f"步骤: {step}\n结果: {step_result}\n\n"
            last_step_result = step_result
            
        print("\n所有步骤执行完毕。")
        return last_step_result

class PlanAndSolveAgent:
    """
    Plan-and-Solve 代理类，结合规划和执行来解决问题。
    """
    def __init__(self, llmclient: LLMClient, tool_executor: ToolExecutor):
        """
        初始化PlanAndSolveAgent。

        Args:
            llmclient (LLMClient): LLM客户端实例。
            tool_executor (ToolExecutor): 工具执行器实例。
        """
        self.llmclient = llmclient
        self.tool_executor = tool_executor
        self.planner = Planner(llmclient, tool_executor)
        self.executor = Executor(llmclient, tool_executor)
    
    def run(self, question: str) -> str:
        """
        运行代理解决问题。

        Args:
            question (str): 用户的问题。

        Returns:
            str: 执行结果日志。
        """
        plan = self.planner.plan(question)
        if not plan:
            return ""
        print("生成计划:", plan)
        return self.executor.execute(plan)

if __name__ == "__main__":
    try:
        from SearchApi import search
        from ToolExecutor import get_current_time
        
        llmclient = LLMClient()
        tool_executor = ToolExecutor()
        tool_executor.register_tool("search", "一个网页搜索，可以搜索信息", search)
        tool_executor.register_tool("get_current_time", "获取当前时间", get_current_time)
        
        agent = PlanAndSolveAgent(llmclient, tool_executor)
        question = "在直线跑道上，小亮和小伟站在同一起跑线上，面朝相同方向进行一场游戏，每一回合通过猜拳方式决定胜负（无平局），胜者前进1米，负者后退1米，如果出现连胜情况，每回合胜者前进距离依次增加1米，负者后退距离保持不变.例如，在小亮的3连胜中，他第一回合前进1米，第二回合前进2米，第三回合前进3米，小伟每回合后退1米，若两人一共进行20回合的游戏，其中小亮出现一次3连胜，小伟出现一次3连胜和一次4连胜，此外，两人均未出现其他连胜情况，则在游戏结束时两人相距多少米." 
        answer = agent.run(question)
        print("\n最终答案:", answer)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Exception: {e}")