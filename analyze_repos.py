import os
from download import download_repos
from analysis import analyze_repo

def main():
    # 定义要分析的仓库列表
    repos = [
        ("https://github.com/user1/repo1.git", "./downloaded_repos/repo1"),
        ("https://github.com/user2/repo2.git", "./downloaded_repos/repo2"),
        # 添加更多仓库...
    ]

    # 下载所有仓库
    print("开始下载仓库...")
    download_repos(repos)

    # 分析每个仓库
    for _, repo_dir in repos:
        output_file = f"{repo_dir}_analysis.md"
        analyze_repo(repo_dir, output_file)

    print("所有仓库分析完成！")

if __name__ == "__main__":
    main()