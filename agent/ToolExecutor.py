from typing import Callable
from typing import List, Dict
from SearchApi import search
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def get_current_time(*args, **kwargs):
    """
    获取当前时间的工具函数。
    
    Args:
        *args: 可变位置参数（忽略）。
        **kwargs: 可变关键字参数（忽略）。
        
    Returns:
        str: 当前时间的格式化字符串 (YYYY-MM-DD HH:MM:SS)。
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class ToolExecutor:
    """
    工具执行器类，用于注册和管理工具。
    """
    def __init__(self):
        """
        初始化工具执行器。
        创建一个空字典用于存储注册的工具。
        """
        self.tools: Dict[str, Dict[str, str]] = {}

    def register_tool(self, name: str, description: str, func: callable):
        """
        注册一个新工具。

        Args:
            name (str): 工具名称。
            description (str): 工具描述。
            func (callable): 工具对应的函数。
        """
        self.tools[name] = {
            "description": description,
            "func": func
        }
        print(f"工具 '{name}' 已注册。")

    def get_tool(self, name: str) -> Callable:
        """
        根据名称获取工具函数。

        Args:
            name (str): 工具名称。

        Returns:
            Callable: 工具函数，如果未找到则返回None。
        """
        return self.tools.get(name).get("func")

    def get_tools(self) -> str:
        """
        获取所有已注册工具的描述列表。

        Returns:
            str: 格式化的工具描述字符串，每行一个工具。
        """
        return "\n".join([
            f"- {name}: {info['description']}"
            for name, info in self.tools.items()
        ])

if __name__ == "__main__":
    executor = ToolExecutor()
    executor.register_tool("search", "一个网页搜索，可以搜索信息", search)
    executor.register_tool("get_current_time", "获取当前时间", get_current_time)
    print(executor.get_tools())

    tool_name = "search"
    tool_input = "老北京豆腐"
    tool_function = executor.get_tool(tool_name)
    if tool_function:
        result = tool_function(tool_input)
        print(f"工具 '{tool_name}' 的结果: {result}")
