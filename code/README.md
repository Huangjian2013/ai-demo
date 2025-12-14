# AI Agents & Frameworks

本模块聚焦于 **AI Agent（智能体）** 的开发与实践。Agent 是 LLM 应用的下一个阶段，它不仅能回答问题，还能使用工具、执行任务并相互协作。

## 🤖 OpenAI Swarm 框架

[Swarm](https://github.com/openai/swarm) 是 OpenAI 推出探索性的多智能体编排框架。它主打轻量级、可控性和易测试性。

### 学习案例
本目录包含以下 Swarm 框架的实战教程：

1.  **[01-Swarm.ipynb](./01-Swarm.ipynb)**
    - Swarm 基础入门。
    - 学习如何定义 Agent，以及 Agent 之间如何进行基础的切换（Handoff）。

2.  **[02-swarm-be.ipynb](./02-swarm-be.ipynb)**
    - Swarm 后端应用实战。
    - 模拟更复杂的业务场景，展示 Agent 如何协同处理后台任务。

3.  **[03-Swarm-sum.ipynb](./03-Swarm-sum.ipynb)**
    - Swarm 总结与进阶。
    - 进一步探索 Swarm 的模式和最佳实践。

## 🌟 什么是 Agent?

Agent 通俗理解就是 **LLM + Memory + Tools + Planning**。
- **LLM**: 大脑，负责推理和决策。
- **Memory**: 记忆，存储上下文和历史信息。
- **Tools**: 手脚，连接外部世界（API, 数据库, 搜索引擎等）。
- **Planning**: 规划，将复杂任务拆解并逐步执行。

通过本模块的学习，你将掌握如何构建能“干活”的 AI 应用。
