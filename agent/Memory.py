from typing import List, Dict

class Memory:
    """
    记忆类，用于存储代理的执行和反思记录。
    """
    def __init__(self):
        """
        初始化记忆模块。
        """
        self.messages = []
    
    def add(self, record_type: str, message: str):
        """
        添加一条记忆记录。

        Args:
            record_type (str): 记录类型（如 'execution', 'reflection'）。
            message (str): 记录内容。
        """
        self.messages.append({"type": record_type, "content": message})
    
    def get(self) -> List[Dict[str, str]]:
        """
        获取所有记忆记录。

        Returns:
            List[Dict[str, str]]: 记忆记录列表。
        """
        return self.messages

    def get_trajectory(self) -> str:
        """
        获取格式化的记忆轨迹字符串。

        Returns:
            str: 所有记录拼接成的字符串。
        """
        return "\n".join([f"{msg['type']}: {msg['content']}" 
                for msg in self.messages])

    def get_last_execution(self) -> str:
        """
        获取最后一次执行结果。

        Returns:
            str: 最后一次执行的内容。如果未找到，返回空字符串。
        """
        for msg in reversed(self.messages):
            if msg['type'] == 'execution':
                return msg['content']
        return ""