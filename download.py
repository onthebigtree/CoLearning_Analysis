import os
from git import Repo

def download_github_repo(repo_url, destination_folder):
    os.makedirs(destination_folder, exist_ok=True)
    Repo.clone_from(repo_url, destination_folder)
    print(f"仓库已成功下载到: {destination_folder}")

def download_repos(repos):
    for repo_url, destination_folder in repos:
        download_github_repo(repo_url, destination_folder)

if __name__ == '__main__':
    repo_url = input("请输入 GitHub 仓库的 URL: ").strip()
    destination_folder = input("请输入目标文件夹路径（直接回车则使用默认路径 './downloaded_repo'）: ").strip() or "./downloaded_repo"
    download_github_repo(repo_url, destination_folder)