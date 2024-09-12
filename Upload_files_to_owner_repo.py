import os
import git
import shutil
from github import Github
from jproperties import Properties

properties = Properties()
with open('/Users/krishnaprasath/Desktop/git_upload_config.properties', 'rb') as f:
    properties.load(f, "utf-8")

GITHUB_TOKEN = properties['token'].data
REPO_OWNER = "krishna0408"
REPO = input("Enter REPO : ").strip()
FOLDER_NAME = input("Enter FOLDER : ").strip()
REPO_NAME = REPO_OWNER + '/' + REPO
BRANCH_NAME = input("Enter Branch Name : ").strip()
FOLDER = "/Users/krishnaprasath/Desktop/"
FOLDER_PATH = FOLDER + FOLDER_NAME + '/current'
print(FOLDER_PATH)
repo_dir = "/Users/krishnaprasath/Desktop/tmp/local_repo"

g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

if os.path.exists(repo_dir):
    shutil.rmtree(repo_dir)
    print(f"Cleaned up existing repo_dir: {repo_dir}")

fork_repo_url = f"https://{GITHUB_TOKEN}@github.com/krishna4802/{REPO}.git"
git_repo = git.Repo.clone_from(fork_repo_url, repo_dir)

def sync_fork_with_upstream():
    upstream_url = f"https://{GITHUB_TOKEN}@github.com/krishna0408/{REPO}.git"


    if "upstream" not in [remote.name for remote in git_repo.remotes]:
        git_repo.create_remote('upstream', upstream_url)
        print(f"Added upstream remote: {upstream_url}")


    git_repo.remotes.upstream.fetch()
    print("Fetched changes from upstream (original repo).")


    git_repo.git.checkout('main')
    git_repo.git.merge('upstream/main')
    print("Merged changes from upstream/main into local main branch.")


    git_repo.remotes.origin.push('main')
    print("Pushed merged changes to forked repository (origin).")

sync_fork_with_upstream()

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
    return file_name.startswith(".DS_Store") or file_name.startswith(".") or file_name.endswith(".properties") or \
           file_name.endswith(".ini") or ".properties" in file_name or file_name.endswith(".json") or \
           file_name.endswith(".htm") or file_name.endswith(".log") or file_name.endswith(".xlsx") or \
           file_name.endswith(".pdf")

def should_skip_directory(directory_name):
    return directory_name.startswith(".") or directory_name == "__pycache__" or directory_name == "repo"

def add_files_to_repo(folder, repo_dir):
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
                with open(file_path, "rb") as src_file:
                    with open(dest_path, "wb") as dest_file:
                        dest_file.write(src_file.read())
                git_repo.index.add([relative_path]) 
                print(f"Added to git index: {relative_path}")
            except OSError as e:
                print(f"Error updating file {relative_path}: {e}")

add_files_to_repo(FOLDER_PATH, repo_dir)

commit_message = "Added Snowflake folder contents (excluding certain files)"
git_repo.index.commit(commit_message)
git_repo.remotes.origin.push(BRANCH_NAME)
print(f"Pushed branch '{BRANCH_NAME}' to remote repository.")

pr_title = "Add Snowflake Folder (excluding certain files)"
pr_body = "This PR adds the contents of the Snowflake folder, excluding hidden files and certain file types."
base_branch = "main"

pr = repo.create_pull(
    title=pr_title,
    body=pr_body,
    head=f"krishna4802:{BRANCH_NAME}",
    base=base_branch
)

print(f"Pull request created: {pr.html_url}")
 
