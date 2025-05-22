import os
import sys

def update_readme_headers():
    """
    Scans the current Git repository for README.md files
    that contain the specific placeholder 'YOUR_FOLDER_NAME_PLACEHOLDER'
    and replaces it with the name of the parent directory.
    """
    print("Running pre-commit hook to update README.md headers...")

    # Define the placeholder string to look for
    placeholder = "# YOUR_FOLDER_NAME_PLACEHOLDER"

    # Get the root of the Git repository
    git_root = os.popen('git rev-parse --show-toplevel').read().strip()
    if not git_root:
        print("Error: Not inside a Git repository. Skipping README update.")
        return

    # Get all staged files
    staged_files_output = os.popen('git diff --cached --name-only').read().strip()
    staged_files = staged_files_output.split('\n') if staged_files_output else []

    # Iterate through all files in the repository to find README.md files
    for root, dirs, files in os.walk(git_root):
        for file_name in files:
            if file_name.lower() == 'readme.md':
                readme_path = os.path.join(root, file_name)
                
                # Ensure the README.md is part of the current commit (staged or modified)
                # This check prevents modifying untracked or unstaged READMEs unnecessarily
                relative_readme_path = os.path.relpath(readme_path, git_root)
                
                # Check if the file is staged or if it's an existing file that might need updating
                # This condition is a bit broad; it ensures we process relevant READMEs.
                # A more precise check would be to only process staged READMEs, but this
                # ensures existing ones get updated if they have the placeholder.
                if not (relative_readme_path in staged_files or os.path.exists(readme_path)):
                    continue 

                try:
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    if placeholder in content:
                        # Get the parent directory name
                        parent_dir_name = os.path.basename(root)

                        # Replace the placeholder with the actual folder name
                        # We use .replace(..., 1) to only replace the first occurrence
                        new_content = content.replace(placeholder, f"# {parent_dir_name}", 1) 

                        with open(readme_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)

                        print(f"Updated header in: {relative_readme_path}")
                        
                        # Stage the modified README.md file so the changes are included in the commit
                        os.system(f'git add "{readme_path}"')
                        print(f"Staged updated README: {relative_readme_path}")

                except Exception as e:
                    print(f"Error processing {readme_path}: {e}")

if __name__ == "__main__":
    update_readme_headers()
