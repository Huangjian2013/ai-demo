import re
from LLMClient import LLMClient
from ToolExecutor import ToolExecutor
from dotenv import load_dotenv
from SearchApi import search
from ToolExecutor import get_current_time
from constant import system_prompt

load_dotenv()

# ReAct 提示词模板
REACT_PROMPT_TEMPLATE = """
你是一个强大的智能助手，可以利用工具解决复杂问题。

## 可用工具
{tools}

## 回应格式
请务必严格遵守以下格式进行回应（不要输出任何其他多余内容）：

Thought: 思考当前的情况，分析问题，决定下一步做什么。
Action: 采取的行动，必须是以下格式之一：
- `{{tool_name}}[{{tool_input}}]`: 调用工具。例如 `search[OpenAI 2025 models]`
- `Finish[最终答案]`: 任务完成，返回最终答案。

## 示例
Question: 2024年奥运会在哪里举办？
Thought: 我需要搜索2024年奥运会的举办地点。
Action: search[2024 olympics location]
Observation: 2024 Summer Olympics will be held in Paris, France.
Thought: 我已经获得了答案，2024年奥运会在巴黎举办。
Action: Finish[2024年奥运会将在法国巴黎举办。]

## 当前任务
Question: {question}
提醒：{reflection}
History:
{history}

请根据 History 继续思考。如果 History 为空，请开始第一步思考。
"""

class ReActAgent:
    """
    ReAct代理类，实现推理+行动的循环。
    """
    def __init__(self, llmclient: LLMClient, tool_executor: ToolExecutor, max_step:int = 5):
        """
        初始化ReActAgent。

        Args:
            llmclient (LLMClient): LLM客户端实例。
            tool_executor (ToolExecutor): 工具执行器实例。
            max_step (int): 最大思考步数，默认为5。
        """
        self.llmclient = llmclient
        self.tool_executor = tool_executor
        self.max_step = max_step
    
    def _parse_response(self, response_text: str):
        """
        解析LLM的响应，提取Thought和Action。

        Args:
            response_text (str): LLM的响应文本。

        Returns:
            tuple: (thought, action) 字符串元组。
        """
        thought_match = re.search(r"Thought: (.*)", response_text, re.DOTALL)
        action_match = re.search(r"Action: (.*)", response_text, re.DOTALL)
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        return thought, action

    def _parse_action(self, action: str):
        """
        解析Action字符串，提取工具名称和输入。

        Args:
            action (str): Action字符串，格式为 tool_name[tool_input]。

        Returns:
            tuple: (tool_name, tool_input) 字符串元组。
        """
        match = re.match(r"(\w+)\[(.*)\]", action, re.DOTALL)
        if match:
            return match.group(1), match.group(2)
        return None, None

    def run(self, question: str, reflection: str = ""):
        """
        运行ReAct循环解决问题。

        Args:
            question (str): 用户的问题。
            reflection (str): 可选的反思内容，用于提示LLM。

        Returns:
            str: 最终答案。如果未找到答案或达到最大步数，返回None。
        """
        self.history = []
        
        current_step = 0
        while current_step < self.max_step:
            current_step += 1
            print(f"\n当前步数: {current_step}")

            tools = self.tool_executor.get_tools()
            # 格式化提示词
            prompt = REACT_PROMPT_TEMPLATE.format(
                tools=tools,
                question=question,
                history="\n".join(self.history),
                reflection=reflection
            )
            #print(f"Prompt:\n{prompt}")
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            # 调用LLM进行思考
            response_text = self.llmclient.think(messages)
            print(response_text)
            if not response_text:
                print("LLM 响应失败")
                break
            
            # 解析响应
            thought, action = self._parse_response(response_text)
            if not action:
                print("未获得下一步action, 步骤结束")
                break

            # 检查是否完成任务
            if action.startswith("Finish"):
                final_answer_match = re.match(r"Finish\[(.*)\]", action, re.DOTALL)
                if final_answer_match:
                    final_answer = final_answer_match.group(1)
                    print(f"🎉 最终答案: {final_answer}")
                    return final_answer
                else:
                    print("无法解析 Finish action")
                    break
            
            # 解析并执行工具调用
            tool_name, tool_input = self._parse_action(action)
            if not tool_name:
                print("LLM 响应格式错误")
                break
            
            tool_function = self.tool_executor.get_tool(tool_name)
            if not tool_function:
                observation = f"工具 '{tool_name}' 不存在"
            else:
                observation = tool_function(tool_input)
            print(f"观察结果: {observation}")
            
            # 更新历史记录
            self.history.append(f"Thought: {thought}\nAction: {action}")
            self.history.append(f"Observation: {observation}")

        print("已经达到最大步数，流程终止")
        return None
        

if __name__ == "__main__":
    try:
        llmclient = LLMClient()
        tool_executor = ToolExecutor()
        tool_executor.register_tool("search", "一个网页搜索，可以搜索信息", search)
        tool_executor.register_tool("get_current_time", "获取当前时间", get_current_time)

        agent = ReActAgent(llmclient, tool_executor)
        question = "2025年OpenAI发布过的模型都有什么？"
        answer = agent.run(question)
        print("\n最终答案:", answer)
    except Exception as e:
        print(f"Exception: {e}")
