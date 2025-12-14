import os;
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict
from constant import system_prompt

load_dotenv()

class LLMClient:
    """
    LLM客户端类，用于与OpenAI API进行交互。
    封装了初始化客户端和发送请求的逻辑。
    """
    def __init__(self):
        """
        初始化LLMClient。
        从环境变量中读取API Key和Base URL，并创建OpenAI客户端实例。
        """
        self.api_key = os.getenv("LLM_API_KEY")
        self.base_url = os.getenv("LLM_BASE_URL")
        self.model = os.getenv("LLM_MODEL_ID")
        
        # 初始化OpenAI客户端
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=600
        )

    def think(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """
        发送消息给LLM并获取回复。

        Args:
            messages (List[Dict[str, str]]): 消息列表，包含角色和内容。
            temperature (float): 采样温度，控制输出的随机性。默认为0.7。

        Returns:
            str: LLM生成的回复内容。如果调用失败，返回空字符串。
        """
        max_retries = 3
        import time
        
        for attempt in range(max_retries):
            print(f"正在调用LLM: {self.model} (尝试 {attempt + 1}/{max_retries})")
            try:
                # 发送聊天完成请求，启用流式输出
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    stream=True,
                )
                print("===============\n")
                print("LLM 响应成功: ")
                collected_chunks = []
                # 逐块接收流式响应
                for chunk in response:
                    content = chunk.choices[0].delta.content
                    if content:
                        print(content, end="", flush=True)
                        collected_chunks.append(content)
                print("\n===============")
                return "".join(collected_chunks)

            except Exception as e:
                # 捕获并打印异常
                print(f"LLM 调用失败: {e}")
                if attempt < max_retries - 1:
                    print("正在重试...")
                    time.sleep(2)  # Wait a bit before retrying
                else:
                    return ""
if __name__ == "__main__":
    try:
        agent = LLMClient()
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "写一个快排算法"},
        ]
        response = agent.think(messages)
        print("\nLLM 响应:", response)
    except Exception as e:
        print(f"Exception: {e}")