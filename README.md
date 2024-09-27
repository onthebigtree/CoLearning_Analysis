# colearning_analysis

# 仓库共学笔记分析工具（粗糙简单版）

## 项目简介

这是一个使用 OpenAI 模型来分析 Markdown 格式笔记的 Python 工具。它可以自动处理指定目录中的所有 .md 文件，提取关键点和精华，并将分析结果汇总到一个总的 Markdown 文件中。

## 主要功能

- 遍历指定目录中的所有 Markdown 文件
- 使用 GPT-4 模型分析每个笔记的内容
- 提取笔记中的关键点和精华
- 将所有分析结果汇总到一个总的 Markdown 文件中

## 使用方法

1. 确保你有有效的 OpenAI API 密钥，并且有权限使用 GPT-4 模型。
2. 在项目根目录创建一个 `.env` 文件，并添加你的 API 密钥：
   ```
   OPENAI_API_KEY=你的_OpenAI_API_密钥
   ```
3. 安装所需的 Python 库：
   ```
   pip install openai markdown beautifulsoup4 python-dotenv
   ```
4. 将你想要分析的 Markdown 笔记放在 `Downloaded_repo` 目录中。
5. 运行脚本：
   ```
   python analysis.py
   ```
6. 分析结果将保存在 `notes_analysis_summary.md` 文件中。

## 注意事项

- 处理大量或长篇笔记可能需要一些时间，请耐心等待。
- 使用 API 可能会产生费用，请注意你的使用量。


## 许可

[MIT License](LICENSE)