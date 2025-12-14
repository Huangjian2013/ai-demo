import os
from dotenv import load_dotenv
from LLMClient import LLMClient
from typing import List, Dict  
from constant import system_prompt
from ReActAgent import ReActAgent
from Memory import Memory
from ToolExecutor import ToolExecutor
from SearchApi import search
from ToolExecutor import get_current_time

load_dotenv()

REFLECTOR_PROMPT_TEMPLATE = """
你是一个资深的AI专家，你的任务是根据用户的问题，评估执行结果是否正确、完整且高效。

## 原始任务
{task}

## 执行结果
{execution}

## 评估要求
请仔细检查执行结果，并思考以下问题：
1. 结果是否完全回答了用户的原始任务？
2. 结果中的信息是否准确无误？
3. 是否有遗漏的关键步骤或信息？
4. 是否存在逻辑错误或矛盾？
5. **关键检查**：执行过程中是否因为缺少信息而停止？是否要求用户提供额外信息？如果是，这通常意味着任务未完成。

## 反思输出
请输出你的反思结果。
- 如果结果正确且完美，请仅输出 "Finish"。
- 如果存在问题（包括未完成、请求用户输入等），请详细描述问题所在，并给出具体的改进建议。

#反思
"""

class Reflector:
    """
    反思器类，负责评估代理的执行结果。
    """
    def __init__(self, agent: ReActAgent):
        """
        初始化反思器。

        Args:
            agent (ReActAgent): 要评估的ReAct代理实例。
        """
        self.agent = agent
    
    def reflect(self, task: str, execution: str) -> str:
        """
        对执行结果进行反思。

        Args:
            task (str): 原始任务描述。
            execution (str): 执行结果。

        Returns:
            str: 反思结果。如果调用失败，返回空字符串。
        """
        prompt = REFLECTOR_PROMPT_TEMPLATE.format(task=task, execution=execution)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        response_text = self.agent.llmclient.think(messages)
        if not response_text:
            return ""
        return response_text


class ReflectionAgent:
    """
    反思代理类，通过执行-反思-再执行的循环来提高任务完成质量。
    """
    def __init__(self, agent: ReActAgent, memory: Memory, max_retry: int = 3):
        """
        初始化反思代理。

        Args:
            agent (ReActAgent): 基础执行代理（如ReActAgent）。
            memory (Memory): 记忆模块实例。
            max_retry (int): 最大重试次数，默认为3。
        """
        self.agent = agent
        self.reflector = Reflector(agent)
        self.memory = memory
        self.max_retry = max_retry
    
    def run(self, task: str):
        """
        运行反思代理。

        Args:
            task (str): 任务描述。

        Returns:
            tuple: (最终执行结果, 最终反思结果)。
        """
        print(f"开始执行任务: {task}")
        execution_result = self.agent.run(task)
        self.memory.add("execution", execution_result)
        print(f"第1次执行结果: {execution_result}")
        
        for i in range(self.max_retry):
            reflection = self.reflector.reflect(task, execution_result)
            self.memory.add("reflection", reflection)
            print(f"第{i+1}次反思结果: {reflection}")
            if "Finish" in reflection:
                return execution_result, reflection
            execution_result = self.agent.run(task, reflection)
            self.memory.add("execution", execution_result)
            print(f"第{i+1}次重新执行结果: {execution_result}")
        return execution_result, reflection

if __name__ == "__main__":
    try:
        llmclient = LLMClient()
        memory = Memory()
        tool_executor = ToolExecutor()
        tool_executor.register_tool("search", "一个网页搜索，可以搜索信息", search)
        tool_executor.register_tool("get_current_time", "获取当前时间", get_current_time)
        agent = ReActAgent(llmclient, tool_executor)
        reflector = Reflector(agent)
        reflection_agent = ReflectionAgent(agent, memory)
        task = "2025年OpenAI发布过的模型都有什么？"
        reflection_agent.run(task)
    except Exception as e:
        print(f"Exception: {e}")
