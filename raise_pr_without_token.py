import subprocess
import os
import shutil
import git

def create_git_clone(user_name, repo_name, repo_url, repo_origin_url, repo_upstream_url, git_repo_dir, branch_name):
    if not os.path.exists(git_repo_dir):
        git_command = [
            ["git", "clone", repo_url, git_repo_dir],
            ["git", "-C", git_repo_dir, "checkout", "master"],
            ["git", "-C", git_repo_dir, "pull", "origin", "master"],
            ["git", "-C", git_repo_dir, "checkout", "-b", branch_name]
        ]
    else:
        git_command = [
            ["git", "-C", git_repo_dir, "checkout", "master"],
            ["git", "-C", git_repo_dir, "fetch", "upstream"],
            ["git", "-C", git_repo_dir, "merge", "upstream/master"],
            ["git", "-C", git_repo_dir, "checkout", "-b", branch_name]
        ]

    try:
        for cmd in git_command:
            print(f"Executing command: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=True, capture_output=True)
            print(result.stdout.decode())
            print(result.stderr.decode())

        result = subprocess.run(['git', '-C', git_repo_dir, 'branch'], check=True, capture_output=True)
        print(f"Available branches: {result.stdout.decode()}")

        os.chdir(git_repo_dir)

        if not os.path.exists(git_repo_dir + "/.git"):
            print(f"Repository cloned successfully at {git_repo_dir}")
            subprocess.run(['git', 'remote', 'add', 'upstream', repo_upstream_url], check=True, capture_output=True)
            subprocess.run(['git', 'remote', 'add', 'origin', repo_origin_url], check=True, capture_output=True)
        else:
            print(f"Repository updated successfully at {git_repo_dir}")
            subprocess.run(['git', 'remote', 'add', 'upstream', repo_upstream_url], check=True, capture_output=True)
            subprocess.run(['git', 'remote', 'set-url', 'origin', repo_origin_url], check=True, capture_output=True)
            subprocess.run(['git', 'remote', 'set-url', 'upstream', repo_upstream_url], check=True, capture_output=True)
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
        subprocess.run(['git', 'checkout', branch_name], check=True, capture_output=True)
        print(f"Switched to branch: {branch_name}")

        subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
        subprocess.run(['git', 'status'], check=True, capture_output=True)

        subprocess.run(['git', 'commit', '-am', f"{branch_name} files"], check=True, capture_output=True)
        subprocess.run(['git', 'status'], check=True, capture_output=True)

        subprocess.run(['git', 'push', '--set-upstream', 'origin', branch_name], check=True, capture_output=True)

        subprocess.run(['gh', 'repo', 'set-default', f'{user_name}/{repo_name}'], check=True, capture_output=True)

        title = "From_prod-pth_machine"
        body = "itc_files_from_prod-pth_machine"
        pr_command = f'gh pr create --repo {user_name}/{repo_name} --title "{title}" --body "{body}"'
        print(f"Executing pull request creation command: {pr_command}")
        process = subprocess.run(pr_command, shell=True, check=True, capture_output=True)

        print(process.stdout.decode())
        print(process.stderr.decode()) 

        pr_link = process.stdout.strip().decode().split('\n')[0]

        if pr_link:
            print("Pull request created successfully.")
            return pr_link
        else:
            print("Found no changes, so pull request was not created.")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error creating pull request: {e}")
        print(f"Standard Output: {e.stdout.decode()}")
        print(f"Standard Error: {e.stderr.decode()}")
        return None

USER_NAME = "rpx"
REPO_NAME = "ITC"
REPO_URL = "git@github.com:rpx/ITC.git"
REPO_ORIGIN_URL = "git@github.com:rpx/ITC.git"
REPO_UPSTREAM_URL = "git@github.com/rpx/ITC.git"
GIT_REPO_DIR = f"/spark_shared/tmp/{REPO_NAME}"
LOCAL_DIR = '/opt/pentaho/repos/itc/current'
BRANCH_NAME = "from_prod-pth"

create_git_clone(USER_NAME, REPO_NAME, REPO_URL, REPO_ORIGIN_URL, REPO_UPSTREAM_URL, GIT_REPO_DIR, BRANCH_NAME)
add_files_to_repo(LOCAL_DIR, GIT_REPO_DIR)
pr_link = raise_git_pr(USER_NAME, REPO_NAME, GIT_REPO_DIR, BRANCH_NAME)
if pr_link:
    print(f"Pull Request URL: {pr_link}")
