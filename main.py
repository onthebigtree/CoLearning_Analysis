import os
from git import Repo

def download_github_repo(repo_url, destination_folder):
    # 确保目标文件夹存在
    os.makedirs(destination_folder, exist_ok=True)
    
    # 克隆仓库
    Repo.clone_from(repo_url, destination_folder)
    
    print(f"仓库已成功下载到: {destination_folder}")

def main():
    # 提示用户输入 GitHub 仓库的 URL
    repo_url = input("请输入 GitHub 仓库的 URL: ").strip()
    
    # 提示用户输入目标文件夹（可选）
    destination_folder = input("请输入目标文件夹路径（直接回车则使用默认路径 './downloaded_repo'）: ").strip()
    
    # 如果用户没有输入目标文件夹，使用默认值
    if not destination_folder:
        destination_folder = "./downloaded_repo"

    # 调用下载函数
    download_github_repo(repo_url, destination_folder)

if __name__ == '__main__':
    main()
