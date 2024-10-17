import subprocess
import os
import shutil
import git
import configparser

def create_git_clone(user_name, repo_name, repo_url, repo_origin_url, repo_upstream_url, git_repo_dir, branch_name):
    if os.path.exists(git_repo_dir):
        print(f"Removing existing directory: {git_repo_dir}")
        shutil.rmtree(git_repo_dir)

    # Clone the repository
    git_command = [
        ["git", "clone", repo_url, git_repo_dir],
        ["git", "-C", git_repo_dir, "checkout", "master"],
        ["git", "-C", git_repo_dir, "pull", "origin", "master"],
        ["git", "-C", git_repo_dir, "checkout", "-b", branch_name]
    ]

    try:
        for cmd in git_command:
            print(f"Executing command: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=True, capture_output=True)
            print(result.stdout.decode())
            print(result.stderr.decode())

        print(f"Repository cloned successfully at {git_repo_dir}")
        subprocess.run(['git', 'remote', 'add', 'upstream', repo_upstream_url], check=True, capture_output=True)
        subprocess.run(['git', 'remote', 'add', 'origin', repo_origin_url], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing Git command: {e}")
        print(f"Standard Output: {e.stdout.decode()}")
        print(f"Standard Error: {e.stderr.decode()}")

def add_files_to_repo(folder, repo_dir):
    git_repo = git.Repo(repo_dir)
    files_to_add = []

    def should_exclude_file(file_name):
        return file_name.startswith(".DS_Store") or file_name.startswith(".") or file_name.endswith(".properties") or \
            file_name.endswith(".ini") or ".properties" in file_name or file_name.endswith(".json") or \
            file_name.endswith(".htm") or file_name.endswith(".log") or file_name.endswith(".xlsx") or \
            file_name.endswith(".pdf") or ".properties" in file_name or file_name.endswith(".rb") or "REVISION" in file_name 

    def should_skip_directory(directory_name):
        return directory_name.startswith(".") or directory_name == "__pycache__" or directory_name == "repo"

    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if not should_skip_directory(d)]

        for file in files:
            if should_exclude_file(file):
                continue

            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, folder)
            dest_path = os.path.join(repo_dir, relative_path)

            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            try:
                print(f"Copying from {file_path} to {dest_path}")
                shutil.copy2(file_path, dest_path)
                
                if not os.path.exists(dest_path):
                    print(f"File was not copied to destination: {relative_path}")
                elif os.path.getsize(file_path) != os.path.getsize(dest_path):
                    print(f"File size mismatch for: {relative_path}")
                else:
                    with open(file_path, 'r') as src_file:
                        src_content = src_file.read()
                    with open(dest_path, 'r') as dest_file:
                        dest_content = dest_file.read()
                    if src_content != dest_content:
                        print(f"Content mismatch for: {relative_path}")
                    else:
                        files_to_add.append(relative_path)
                        print(f"Successfully copied and added to index: {relative_path}")
            except Exception as e:
                print(f"Error updating file {relative_path}: {e}")

    if files_to_add:
        git_repo.index.add(files_to_add)
        print(f"Added to git index: {', '.join(files_to_add)}")

def raise_git_pr(user_name, repo_name, git_repo_dir, branch_name):
    os.chdir(git_repo_dir)

    try:
        result = subprocess.run(['git', 'branch', '--list', branch_name], capture_output=True, text=True)
        if branch_name not in result.stdout:
            print(f"Branch {branch_name} does not exist. Creating new branch.")
            subprocess.run(['git', 'checkout', '-b', branch_name], check=True, capture_output=True, text=True)
        else:
            print(f"Branch {branch_name} already exists. Checking out.")
            subprocess.run(['git', 'checkout', branch_name], check=True, capture_output=True, text=True)
        print(f"Switched to branch: {branch_name}")

        subprocess.run(['git', 'add', '.'], check=True, capture_output=True, text=True)
        subprocess.run(['git', 'status'], check=True, capture_output=True, text=True)

        subprocess.run(['git', 'commit', '-am', f"{branch_name} files"], check=True, capture_output=True, text=True)
        subprocess.run(['git', 'status'], check=True, capture_output=True, text=True)

        push_result = subprocess.run(['git', 'push', '--set-upstream', 'origin', branch_name], capture_output=True, text=True, check=True)
        
        push_output = push_result.stdout
        print(push_output)

        pr_url = None
        for line in push_output.splitlines():
            if "Create a pull request for" in line:
                pr_url = line.split(" ", 1)[1]
                break

        if pr_url:
            print(f"Suggested pull request URL: {pr_url}")
            return pr_url
        else:
            print("Pull request URL not found in the push output.")
            return None

    except subprocess.CalledProcessError as e:
        print(f"Error pushing branch: {e}")
        print(f"Standard Output: {e.stdout}")
        print(f"Standard Error: {e.stderr}")
        return None

config = configparser.ConfigParser()
config.read('config.ini')

USER_NAME = config['git']['USER_NAME']

REPO_NAME = input("Enter the repository name: ")
BRANCH_NAME = input("Enter the branch name: ")

REPO_URL = f"git@github.com:{USER_NAME}/{REPO_NAME}.git"
REPO_ORIGIN_URL = f"git@github.com:{USER_NAME}/{REPO_NAME}.git"
REPO_UPSTREAM_URL = f"git@github.com:{USER_NAME}/{REPO_NAME}.git"
directory = REPO_NAME.lower()
LOCAL_DIR = f'user/krishna/Desktop/{directory}/current'
GIT_REPO_DIR = f"/user/krishna/test_git/{REPO_NAME}"

create_git_clone(USER_NAME, REPO_NAME, REPO_URL, REPO_ORIGIN_URL, REPO_UPSTREAM_URL, GIT_REPO_DIR, BRANCH_NAME)
add_files_to_repo(LOCAL_DIR, GIT_REPO_DIR)
pr_link = raise_git_pr(USER_NAME, REPO_NAME, GIT_REPO_DIR, BRANCH_NAME)
if pr_link:
    print(f"Pull Request URL: {pr_link}")
