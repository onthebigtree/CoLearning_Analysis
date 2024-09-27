import os
import openai
import markdown
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import json
import time
import random
import re

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中获取 API 密钥
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_markdown(markdown_content):
    # 将 Markdown 转换为 HTML
    html = markdown.markdown(markdown_content)
    # 使用 BeautifulSoup 提取纯文本
    soup = BeautifulSoup(html, features="html.parser")
    return soup.get_text()

def analyze_note(content, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-0613",  # 使用最新可用的模型
                messages=[
                    {"role": "system", "content": "你是一个专业的内容分析和社交媒体编辑助手。你的任务是分析给定的笔记内容，并提炼出适合在社交媒体上分享的精华内容。"},
                    {"role": "user", "content": f"""请分析以下笔记内容，并完成以下任务：

1. 提炼 3-5 个关键观点，每个观点用一句简洁的话概括。
2. 从原文中选择 1-2 个最有价值或最有趣的段落，保持原文不变。
3. 创作 3 个适合在社交媒体（如微博、Twitter 或 LinkedIn）上分享的简短文本（每个不超过 280 字）。这些文本应该基于原文内容，但要更加吸引人和易于传播。
4. 提供 3-5 个相关的话题标签（hashtags）。
5. 给这篇笔记的内容价值打分（1-10分），并简要解释原因。

请确保你的输出保持原文的核心意思，同时使其更适合在社交媒体上传播。

笔记内容如下：

{content}"""}
                ]
            )
            return response.choices[0].message['content']
        except Exception as e:
            print(f"分析笔记时发生错误: {e}. 尝试重新请求 (尝试 {attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:
                time.sleep(random.uniform(1, 3))  # 随机等待1-3秒后重试
            else:
                raise Exception("达到最大重试次数，无法完成笔记分析")

def evaluate_note(analysis, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-0613",  # 使用最新可用的模型
                messages=[
                    {"role": "system", "content": "你是一个专业的内容评估助手。你的任务是评估给定的笔记分析结果，并给出一个综合评分。"},
                    {"role": "user", "content": f"""请评估以下笔记分析结果，并给出一个 1-100 的综合评分。评分应该考虑以下因素：

1. 关键观点的重要性和新颖性
2. 选择段落的价值和吸引力
3. 社交媒体文本的传播潜力
4. 话题标签的相关性和流行度
5. 内容的整体质量和深度

请给出评分并简要解释原因。评分必须是一个1-100之间的整数。

分析结果：

{analysis}"""}
                ]
            )
            evaluation = response.choices[0].message['content']
            if extract_score(evaluation) == 0:
                raise ValueError("评分无效")
            return evaluation
        except Exception as e:
            print(f"评估笔记时发生错误: {e}. 尝试重新请求 (尝试 {attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:
                time.sleep(random.uniform(1, 3))  # 随机等待1-3秒后重试
            else:
                raise Exception("达到最大重试次数，无法完成笔记评估")

def extract_score(evaluation):
    match = re.search(r'\b(\d+)(?:/100)?\b', evaluation)
    if match:
        score = int(match.group(1))
        if 1 <= score <= 100:
            return score
    return 0  # 如果没有找到有效评分，返回0

def process_notes(directory):
    analysis_results = []
    processed_files = set()
    results_file = 'analysis_results.json'

    # 加载已处理的文件和现有的分析结果
    if os.path.exists(results_file):
        with open(results_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            analysis_results = data['results']
            processed_files = set(data['processed_files'])

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                
                # 如果文件已经处理过，跳过
                if file_path in processed_files:
                    print(f"跳过已处理的文件: {file_path}")
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    text_content = extract_text_from_markdown(content)
                    
                    print(f"正在分析文件: {file_path}")
                    analysis = analyze_note(text_content)
                    evaluation = evaluate_note(analysis)
                    
                    # 保存单个文件的分析结果
                    save_single_analysis(file, analysis, evaluation)
                    
                    analysis_results.append((file, analysis, evaluation))
                    processed_files.add(file_path)

                    # 保存当前进度
                    save_progress(results_file, analysis_results, processed_files)
                    
                    print(f"文件 {file} 分析完成\n")
                except Exception as e:
                    print(f"处理文件 {file} 时发生错误: {str(e)}")
                    # 可以选择继续处理下一个文件，或者在这里退出程序

    # 对结果进行排序
    sorted_results = sorted(analysis_results, key=lambda x: extract_score(x[2]), reverse=True)
    return sorted_results

def save_progress(results_file, analysis_results, processed_files):
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            'results': analysis_results,
            'processed_files': list(processed_files)
        }, f, ensure_ascii=False, indent=2)

def save_single_analysis(file_name, analysis, evaluation):
    output_dir = "./single_analysis"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{file_name}_analysis.md")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# {file_name} 的分析结果\n\n")
        f.write(f"## 评分\n\n{evaluation}\n\n")
        f.write(f"## 分析\n\n{analysis}\n\n")

def merge_analysis_results(output_file):
    single_analysis_dir = "./single_analysis"
    all_results = []

    for file in os.listdir(single_analysis_dir):
        if file.endswith("_analysis.md"):
            with open(os.path.join(single_analysis_dir, file), 'r', encoding='utf-8') as f:
                content = f.read()
            file_name = file.replace("_analysis.md", "")
            evaluation = content.split("## 评分\n\n")[1].split("\n\n## 分析")[0]
            analysis = content.split("## 分析\n\n")[1]
            all_results.append((file_name, analysis, evaluation))

    sorted_results = sorted(all_results, key=lambda x: int(x[2].split()[0]), reverse=True)
    save_analysis_results(sorted_results, output_file)

def analyze_repo(repo_dir, output_file):
    print(f"开始分析 {repo_dir} 目录中的笔记...")
    process_notes(repo_dir)
    
    print(f"正在合并分析结果并保存到 {output_file}...")
    merge_analysis_results(output_file)
    
    print(f"分析完成！结果已保存到 {output_file}")

if __name__ == "__main__":
    repo_dir = "./lianshang"
    output_file = "./notes_analysis_summary.md"
    analyze_repo(repo_dir, output_file)
