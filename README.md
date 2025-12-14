# AI Demo 学习指南

欢迎来到 AI Demo 项目！这是一个专门为希望学习和探索人工智能（AI）技术的开发者准备的实战案例集合。

本项目通过具体的代码示例、Jupyter Notebook 教程和相关资料，帮助你深入理解从 Prompt Engineering 到 RAG（检索增强生成）再到 AI Agent（智能体）的各项核心技术。

## 📂 目录结构与学习路径

为了方便学习，本项目按照技术领域进行了模块化组织。你可以根据自己的兴趣和基础选择相应的模块进行学习。

### 1. [📚 提示词工程 (Prompt)](./prompt/README.md)
**适合人群**：AI 初学者、希望提升 LLM 输出质量的开发者。
- 学习如何编写高效的提示词。
- 掌握 Claude 等模型的提示词设计原则。

### 2. [🧠 RAG - 检索增强生成 (Rag)](./rag/README.md)
**适合人群**：希望构建基于私有知识库问答系统的开发者。
- **基础篇**：了解 RAG 基本概念，Embedding 和向量数据库（Qdrant）。
- **进阶篇**：掌握 LangChain 和 LlamaIndex 框架的使用。
- **高阶篇**：探索 GraphRAG 等前沿技术。

### 3. [🛠️ 原生 Agent 实现 (Agent)](./agent/README.md)
**适合人群**：希望深入理解 Agent 底层原理，不依赖框架手写 Agent 的开发者。
- 包含了 ReAct, Plan-and-Solve, Reflection 等经典架构的原生 Python 实现。
- 学习如何自己封装 LLM, Vision, Memory 和 Tool。

### 4. [🤖 OpenAI 技术演示 (OpenAI)](./OpenAI/README.md)
**适合人群**：对 OpenAI 最新技术（如 Swarm 多智能体框架）感兴趣的开发者。
- 学习 OpenAI Swarm 框架。
- 探索基于 OpenAI 技术栈的 Agent 开发。

### 5. [✨ 特色功能演示 (Feature)](./feature/README.md)
**适合人群**：寻找特定 AI 应用场景灵感的开发者。
- 计算机视觉（Supervision）应用。
- AI 应用的云端部署（Cloudflare）。

### 6. [📖 学习资料 (Ebooks)](./ebooks/README.md)
**适合人群**：所有 AI 学习者。
- 收集了关于 LLM、Agent 和 AI 趋势的优质 PDF 报告和电子书。

## 🚀 如何开始

建议按照以下顺序进行学习：

1.  **基础入门**：先浏览 `ebooks` 中的入门资料，了解 LLM 的基本概念。
2.  **动手实践**：从 `prompt` 目录开始，学习如何与 AI 对话。
3.  **核心技术**：深入 `rag` 目录，这是目前最热门的 LLM 企业级应用方向。
4.  **底层原理**：阅读 `agent` 目录的代码，理解 Agent 是如何思考和行动的。
5.  **进阶探索**：尝试 `OpenAI` 目录中的案例，构建基于 Swarm 的 Agent 应用。
6.  **拓展视野**：查看 `feature` 目录，了解 AI 在不同领域的应用潜力。

---
*希望能在这个 AI 时代助你一臂之力！如有问题或建议，欢迎提交 Issue。*