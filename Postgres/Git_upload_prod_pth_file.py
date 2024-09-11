import os
import git
import shutil
from github import Github
from jproperties import Properties

properties = Properties()
with open('/opt/pentaho/repos/git_upload_config.properties', 'rb') as f:
    properties.load(f, "utf-8")

GITHUB_TOKEN = properties['token'].data
REPO_OWNER = properties['repo_owner'].data
REPO = input("Enter Folder : ").strip()
REPO_NAME = REPO_OWNER + '/' + REPO
BRANCH_NAME = input("Enter Branch Name : ").strip()
FOLDER = "/opt/pentaho/repos/"
FOLDER_PATH = FOLDER + REPO
repo_dir = "/tmp/local_repo"

g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

if os.path.exists(repo_dir):
    shutil.rmtree(repo_dir)
    print(f"Cleaned up existing repo_dir: {repo_dir}")

repo_url = f"https://{GITHUB_TOKEN}@github.com/{REPO_NAME}.git"
git_repo = git.Repo.clone_from(repo_url, repo_dir)

def branch_exists(repo, branch_name):
    try:
        repo.get_branch(branch_name)
        return True
    except:
        return False

if branch_exists(repo, BRANCH_NAME):
    print(f"Branch '{BRANCH_NAME}' already exists. Checking out the existing branch.")
    git_repo.git.checkout(BRANCH_NAME)
else:
    print(f"Branch '{BRANCH_NAME}' does not exist. Creating a new branch.")
    git_repo.git.checkout('-b', BRANCH_NAME)

def should_exclude_file(file_name):
    return file_name.startswith(".DS_Store") or file_name.startswith(".") or file_name.endswith(".properties") or file_name.endswith(".ini") or ".properties" in file_name or file_name.endswith(".json") or file_name.endswith(".htm") or file_name.endswith(".log") or file_name.endswith(".xlsx") or file_name.endswith(".pdf")

def should_skip_directory(directory_name):
    return (
        directory_name.startswith(".") or
        directory_name == "__pycache__" or
        directory_name == "repo"
    )

def add_files_to_repo(folder, repo_dir):
    for root, dirs, files in os.walk(folder):
        if os.path.basename(root) != "current" and os.path.dirname(root) != "current":
            continue
        
        dirs[:] = [d for d in dirs if not should_skip_directory(d)]

        for file in files:
            if should_exclude_file(file):
                continue

            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, folder)
            dest_path = os.path.join(repo_dir, relative_path)

            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            try:
                with open(file_path, "rb") as src_file:
                    with open(dest_path, "wb") as dest_file:
                        dest_file.write(src_file.read())
                git_repo.index.add([relative_path])
                print(f"Added to git index: {relative_path}")
            except OSError as e:
                print(f"Error updating file {relative_path}: {e}")

add_files_to_repo(FOLDER_PATH, repo_dir)

commit_message = "Added Files from Prod-pth machine"
git_repo.index.commit(commit_message)
git_repo.remote().push(BRANCH_NAME)

pr_title = "Files from Prod-pth machine"
pr_body = "Added Files from Prod-pth machin."
base_branch = "master"

pr = repo.create_pull(
    title=pr_title,
    body=pr_body,
    head=BRANCH_NAME,
    base=base_branch
)

print(f"Pull request created: {pr.html_url}")
