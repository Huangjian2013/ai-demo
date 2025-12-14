import os
import google.generativeai as genai
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

class GeminiLLMClient:
    """
    使用 Google Generative AI SDK 的 Gemini 客户端。
    """
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            print("警告: 未找到 GOOGLE_API_KEY 环境变量，请确保已设置。")
        
        genai.configure(api_key=self.api_key)
        self.model_name = "gemini-1.5-pro" # 默认模型，可根据需要修改
        
    def think(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """
        发送消息给 Gemini 并获取回复。
        """
        print(f"正在调用 Gemini SDK: {self.model_name}")
        
        try:
            # 提取系统提示词
            system_instruction = None
            history = []
            user_message = ""

            for msg in messages:
                role = msg["role"]
                content = msg["content"]
                
                if role == "system":
                    system_instruction = content
                elif role == "user":
                    #如果是最后一条，且是用户消息，则作为当前 prompt
                    if msg == messages[-1]:
                        user_message = content
                    else:
                        history.append({"role": "user", "parts": [content]})
                elif role == "assistant":
                    history.append({"role": "model", "parts": [content]})
            
            # 如果最后一条不是 user，那可能逻辑有问题，或者需要调整。
            # 这里简单处理，假设 logical flow 是  system -> history -> user prompt
            
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_instruction
            )

            chat = model.start_chat(history=history)
            
            response = chat.send_message(
                user_message,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature
                )
            )
            
            print("===============\n")
            print("Gemini 响应成功")
            content = response.text
            print(content)
            print("\n===============")
            return content

        except Exception as e:
            print(f"Gemini 调用失败: {e}")
            return ""

if __name__ == "__main__":
    try:
        client = GeminiLLMClient()
        messages = [
            {"role": "system", "content": "你是一个幽默的助手"},
            {"role": "user", "content": "讲个笑话"},
        ]
        client.think(messages)
    except Exception as e:
        print(f"Exception: {e}")
