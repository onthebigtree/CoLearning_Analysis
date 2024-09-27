import os
import openai
import markdown
from bs4 import BeautifulSoup
from dotenv import load_dotenv

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

def analyze_note(content):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  #
        messages=[
            {"role": "system", "content": "你是一个专业的笔记分析助手。请分析给定的笔记内容，提炼出其中的关键点和精华。"},
            {"role": "user", "content": f"请分析以下笔记内容，提炼出其中的关键点和精华：\n\n{content}"}
        ]
    )
    return response.choices[0].message['content']

def process_notes(directory):
    analysis_results = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 提取纯文本
                text_content = extract_text_from_markdown(content)
                
                print(f"正在分析文件: {file_path}")
                analysis = analyze_note(text_content)
                
                analysis_results.append((file, analysis))
                
                print(f"文件 {file} 分析完成\n")
    
    return analysis_results

def save_analysis_results(results, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 笔记分析总结\n\n")
        for file_name, analysis in results:
            f.write(f"## {file_name} 的分析结果\n\n")
            f.write(analysis)
            f.write("\n\n---\n\n")  # 添加分隔线

if __name__ == "__main__":
    notes_directory = "./Downloaded_repo"
    output_file = "./notes_analysis_summary.md"
    
    print(f"开始分析 {notes_directory} 目录中的笔记...")
    analysis_results = process_notes(notes_directory)
    
    print(f"正在将分析结果保存到 {output_file}...")
    save_analysis_results(analysis_results, output_file)
    
    print("分析完成！结果已保存到总结文件中。")
