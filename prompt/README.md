# Prompt Engineering (提示词工程)

提示词（Prompt）是与大语言模型（LLM）交互的桥梁。优质的提示词通过精确的指令引导模型生成更准确、更符合预期的结果。本模块收录了提示词设计的最佳实践和案例。

## 📂 内容列表

### 1. [Claude 提示设计原则](./04-Claude提示原则)
Antropic 官方推荐的 Claude 模型 Prompt 设计原则。
- 了解 XML 标签在 Prompt 中的应用。
- 学习如何通过清晰的结构化指令提升模型表现。

### 2. [反思 (Reflection) 提示词](./03-反思提示词)
探索 "反思" 机制在 Prompt 中的应用。
- 引导模型在输出最终答案前进行“思考”和“自我纠错”。
- 适用于需要复杂推理或高准确性的任务。

## 💡 提示词编写核心技巧 (通用)

1.  **清晰明确 (Clarity)**: 避免模棱两可的表达，直接说明你的需求。
2.  **提供上下文 (Context)**: 给予模型足够的背景信息。
3.  **示例引导 (Few-Shot)**: 提供 1-3 个理想的输入输出示例（Few-Shot Learning）。
4.  **分步骤 (Chain of Thought)**: 要求模型“一步步思考”（Let's think step by step）。
5.  **指定格式 (Output Format)**: 明确要求输出的格式（如 JSON, Markdown, 列表等）。
