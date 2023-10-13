# Git-Clone

**Command for Implementing :** git clone [ github_link ].git


## Shell Script for implementing

    if [ "$#" -ne 2 ]; then
        echo "Usage: $0 <GitHub_Repo_URL> <Local_Directory>"
        exit 1
    fi
    
    github_repo_url="$1"
    local_directory="$2"
    
    git clone "$github_repo_url" "$local_directory"
    
    if [ $? -eq 0 ]; then
        echo "Repository cloned successfully to $local_directory"
    else
        echo "Failed to clone the repository"
        exit 1
    fi

**Execution :** ./clone_github_repo.sh [github link] [ location for local machine ]

**Example :** ./clone_github_repo.sh https://github.com/Krishna4802/Nested-task /Users/krishnaprasath/workspace/clone

***

## Task 
### Input :
  * git repo name
  * local file folder path

### Need to create a new folder inside the local dir as below 

  * local_dir/clone/yyyymmddhhmmss
  * pull git repos into the newly created folder
  * create a soft link as current -> local_dir/clone/yyyymmddhhmmss


# Working code

    #!/bin/bash
    
    # Prompt the user for the repository name
    read -p "Enter the GitHub repository name: " repository_name
    
    # Check if a repository name was provided
    if [ -z "$repository_name" ]; then
        echo "GitHub repository name is required."
        exit 1
    fi
    
    # Prompt the user for the local directory
    read -p "Enter the Local Directory: " local_directory
    
    # Check if a local directory was provided
    if [ -z "$local_directory" ]; then
        echo "Local Directory is required."
        exit 1
    fi
    
    # Generate a timestamp (yyyymmddhhmmss)
    timestamp=$(date +'%Y%m%d%H%M%S')
    
    # Create the new folder structure
    clone_dir="$local_directory/clone/$timestamp/$repository_name"
    mkdir -p "$clone_dir"
    
    # Construct the GitHub repository URL
    github_repo_url="https://github.com/Krishna4802/$repository_name"
    
    # Clone the GitHub repository to the newly created folder
    git clone "$github_repo_url" "$clone_dir"
    
    # Check if the clone was successful
    if [ $? -eq 0 ]; then
        echo "Repository cloned successfully to $clone_dir"
    
        # Remove the previous "current" symlink if it exists
        current_link="$local_directory/current"
        [ -L "$current_link" ] && rm -f "$current_link"
    
        # Create a symbolic link to the newly created folder
        ln -s "$clone_dir" "$current_link"
        echo "Symbolic link 'current' created: $current_link"
    else
        echo "Failed to clone the repository"
        exit 1
    fi

**Execution :** ./clone_github_repo_with_folder.sh 
