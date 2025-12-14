import os
from dotenv import load_dotenv
from LLMClient import LLMClient
from constant import system_prompt

load_dotenv()

class SimpleAgent:
    """
    一个简单的代理，直接将用户问题发送给LLM并返回结果。
    """
    def __init__(self, llmclient: LLMClient):
        """
        初始化SimpleAgent。

        Args:
            llmclient (LLMClient): LLM客户端实例。
        """
        self.llmclient = llmclient
    
    def run(self, question: str) -> str:
        """
        运行代理解决问题。

        Args:
            question (str): 用户的问题。

        Returns:
            str: LLM的回复。
        """
        messages = [
           # {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
        response = self.llmclient.think(messages)
        return response

if __name__ == "__main__":
    try:
        llmclient = LLMClient()
        # from GeminiLLMClient import GeminiLLMClient
        # llmclient = GeminiLLMClient()
        
        agent = SimpleAgent(llmclient)
        #question = "在直线跑道上，小亮和小伟站在同一起跑线上，面朝相同方向进行一场游戏，每一回合通过猜拳方式决定胜负（无平局），胜者前进1米，负者后退1米，如果出现连胜情况，每回合胜者前进距离依次增加1米，负者后退距离保持不变.例如，在小亮的3连胜中，他第一回合前进1米，第二回合前进2米，第三回合前进3米，小伟每回合后退1米，若两人一共进行20回合的游戏，其中小亮出现一次3连胜，小伟出现一次3连胜和一次4连胜，此外，两人均未出现其他连胜情况，则在游戏结束时两人相距多少米."
        # question = "Hello"
        question = "我要调查Google的股票是否会上涨，帮我分析一下。"
        print(f"问题: {question}")
        answer = agent.run(question)
        print(f"\n回答: {answer}")
    except Exception as e:
        print(f"Exception: {e}")
