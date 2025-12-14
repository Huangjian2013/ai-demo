# 通用 Agent 架构实践

本模块包含了一系列不依赖第三方繁重框架（如 LangChain, AutoGen），而是尽量使用原生 Python 代码实现的 AI Agent 架构 Demo。旨在帮助开发者理解 Agent 的底层工作原理。

## 🧩 核心组件

- **LLMClient.py**: 封装了大模型 API 的调用接口。
- **Memory.py**: 实现了 Agent 的记忆机制（短期记忆/上下文管理）。
- **ToolExecutor.py**: 工具执行器，负责解析和运行外部工具。
- **SearchApi.py**: 搜索工具实现（示例）。

## 🤖 Agent 实现类型

按照复杂度从低到高排列：

### 1. Simple Agent ([SimpleAgent.py](./SimpleAgent.py))
最基础的对话 Agent，主要演示 LLM 的基本交互和上下文保持。

### 2. ReAct Agent ([ReActAgent.py](./ReActAgent.py))
实现了 **ReAct (Reasoning + Acting)** 范式。
- 模型在执行动作前会先进行推理（Though），然后执行工具（Action），最后观察结果（Observation）。
- 這是目前最主流的 Agent 基础模式。

### 3. Plan & Solve Agent ([PlanAndSolveAgent.py](./PlanAndSolveAgent.py))
实现了 **Plan-and-Solve** 策略。
- 在开始执行前，先制定一个完整的步骤计划。
- 能够处理更复杂的、需要多步推理的问题。

### 4. Reflection Agent ([ReflectionAgent.py](./ReflectionAgent.py))
带有**反思（Self-Reflection）**机制的 Agent。
- 在输出最终结果前，会评估自己的答案并尝试修正错误。
- 能够显著提升解决难题的准确率。

## 🛠️ 如何运行

1.  复制 `.env.example` 为 `.env` 并填入 API Key。
2.  安装依赖：
    ```bash
    pip install -r requirements.txt
    ```
3.  直接运行对应的 Python 文件：
    ```bash
    python ReActAgent.py
    ```
