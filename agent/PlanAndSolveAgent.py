import os;
from dotenv import load_dotenv
from LLMClient import LLMClient
from typing import List
from constant import system_prompt

load_dotenv()  

PLANNER_PROMPT_TEMPLATE = """
你是一个顶级的AI规划专家。你的任务是将用户提出的复杂问题分解成一个由多个简单步骤组成的行动计划。

## 任务要求
1. 将复杂问题拆解为逻辑清晰、可执行的子步骤。
2. 每个步骤必须是独立的，且包含足够的信息。
3. 步骤之间必须有明确的逻辑顺序。
4. 只需要输出计划列表，不要包含任何解释或其他内容。

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

class Planner:
    """
    规划器类，负责生成解决问题的步骤计划。
    """
    def __init__(self, llmclient: LLMClient):
        """
        初始化规划器。

        Args:
            llmclient (LLMClient): LLM客户端实例。
        """
        self.llmclient = llmclient
    
    def plan(self, question: str, reflection: str = "") -> List[str]:
        """
        根据问题生成计划。

        Args:
            question (str): 用户的问题。
            reflection (str): 可选的反思内容，用于优化计划。

        Returns:
            List[str]: 计划步骤列表。如果生成失败，返回空列表。
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": PLANNER_PROMPT_TEMPLATE.format(question=question, reflection=reflection)}
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
    def __init__(self, llmclient: LLMClient):
        """
        初始化执行器。

        Args:
            llmclient (LLMClient): LLM客户端实例。
        """
        self.llmclient = llmclient
    
    def execute(self, plan: List[str]) -> str:
        """
        执行计划。

        Args:
            plan (List[str]): 计划步骤列表。

        Returns:
            str: 执行日志，包含每个步骤的输入和输出。
        """
        execution_log = []
        for step in plan:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": step}
            ]
            response_text = self.llmclient.think(messages)
            if not response_text:
                continue
            print(f"步骤 {step}: {response_text}")
            execution_log.append(f"步骤: {step}\n结果: {response_text}")
        return "\n\n".join(execution_log)

class PlanAndSolveAgent:
    """
    Plan-and-Solve 代理类，结合规划和执行来解决问题。
    """
    def __init__(self, llmclient: LLMClient):
        """
        初始化PlanAndSolveAgent。

        Args:
            llmclient (LLMClient): LLM客户端实例。
        """
        self.llmclient = llmclient
        self.planner = Planner(llmclient)
        self.executor = Executor(llmclient)
    
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
        return self.executor.execute(plan)

if __name__ == "__main__":
    try:
        llmclient = LLMClient()
        agent = PlanAndSolveAgent(llmclient)
        question = "一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？"
        answer = agent.run(question)
        print("\n最终答案:", answer)
    except Exception as e:
        print(f"Exception: {e}")