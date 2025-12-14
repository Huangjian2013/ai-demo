import os
from serpapi import SerpApiClient
from dotenv import load_dotenv

load_dotenv()

def search(query: str) -> str:
    """
    使用SerpApi执行Google搜索。

    Args:
        query (str): 搜索查询字符串。

    Returns:
        str: 搜索结果的摘要字符串。如果搜索失败，返回空字符串。
    """
    print("================")
    print(f"正在调用搜索引擎: {query}")
    try:
        api_key = os.getenv("SERPAPI_API_KEY")
        params = {
            "engine": "google",
            "q": query,
            "gl": "cn",
            "hl": "zh-cn",
            "api_key": api_key,
        }
        client = SerpApiClient(params)
        result = client.get_dict()
        #print(result)

        result_string = ""
        # 优先返回答案框内容
        if "answer_box_list" in result:
            result_string = "\n".join(result["answer_box_list"])
        if "answer_box" in result and "answer" in result["answer_box"]:
            result_string = result["answer_box"]["answer"]
        # 其次返回知识图谱描述
        if "knowledge_graph" in result:
            result_string = result["knowledge_graph"]["description"]
        # 最后返回自然搜索结果摘要
        if "organic_results" in result:
            snippets = [
                f"[{i+1}] {res.get('title', '')}\n{res.get('snippet', '')}"
                for i, res in enumerate(result["organic_results"][:20])
            ]
            result_string = "\n\n".join(snippets)
        
        print("搜索结果:", result_string)
        print("================\n")
        if not result_string:
            return ""
        return result_string
    
    except Exception as e:
        print(f"搜索Exception: {e}")
        return ""

if __name__ == "__main__":
    try:
        query = "老北京豆腐"
        result = search(query)
        print("\n搜索结果:", result)
    except Exception as e:
        print(f"Exception: {e}")

