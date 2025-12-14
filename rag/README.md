# RAG (Retrieval-Augmented Generation) 学习指南

本目录包含了一系列 Jupyter Notebook，旨在带你从零开始掌握 RAG 技术。RAG 是目前解决 LLM 幻觉问题和利用私有数据进行问答的最有效方案之一。

## 📚 学习路径

建议按照以下分类和顺序进行学习：

### 第一阶段：RAG 基础 (Basics)
理解 RAG 的核心概念和组成部分。
- **[03-初识RAG.ipynb](./03-初识RAG.ipynb)**: RAG 的基本概念介绍，通过简单示例演示 RAG 的工作流程。
- **[07-分词.ipynb](./07-分词.ipynb)**: 了解文本处理的第一步——分词（Tokenization），这对后续的 Embedding 至关重要。
- **[06-embedding.ipynb](./06-embedding.ipynb)**: 深入理解 Embedding（向量化），这是将文本转化为机器可理解形式的关键技术。

### 第二阶段：向量数据库 (Vector Database)
学习如何存储和检索向量数据。
- **[04_Qdrant.ipynb](./04_Qdrant.ipynb)**: 学习使用 Qdrant 向量数据库的基础操作。
- **[05_Qdrant_02.ipynb](./05_Qdrant_02.ipynb)**: Qdrant 的进阶使用技巧。

### 第三阶段：LangChain 实战 (LangChain Framework)
利用 LangChain 框架快速构建 RAG 应用。
- **[08_langchain.ipynb](./08_langchain.ipynb)**: LangChain 基础入门。
- **[09-LangChain-Chains.ipynb](./09-LangChain-Chains.ipynb)**: 学习 LangChain 中的 Chain 概念，构建复杂的处理流程。
- **[10-LangChain-pdf-rag.ipynb](./10-LangChain-pdf-rag.ipynb)**: 实战案例：基于 PDF 文档的 RAG 问答系统。

### 第四阶段：LlamaIndex 实战 (LlamaIndex Framework)
探索专注于数据索引和检索的 LlamaIndex 框架。
- **[13-NodeParser.ipynb](./13-NodeParser.ipynb)**: 学习 LlamaIndex 的核心组件 NodeParser，理解文档切片策略。
- **[11-LlamaIndex-pdf-rag.ipynb](./11-LlamaIndex-pdf-rag.ipynb)**: 使用 LlamaIndex 构建 PDF RAG 系统。

### 第五阶段：高级 RAG & 优化 (Advanced)
探索 RAG 的前沿技术和性能优化。
- **[14-quantization.ipynb](./14-quantization.ipynb)**: 模型量化技术，了解如何在资源受限的环境下运行模型。
- **[18-GraphRAG-Neo4j.ipynb](./18-GraphRAG-Neo4j.ipynb)**: GraphRAG 实战，结合知识图谱（Neo4j）增强检索效果，处理复杂的关系查询。
- **[19_schema_graphrag.ipynb](./19_schema_graphrag.ipynb)**: 深入 GraphRAG 的 Schema 设计。

---
💡 **提示**：每个 Notebook 都可以独立运行，建议配合代码实操。
