import os
import sys
import re # Import the regular expression module

# --- Constants and Markers ---
# Old placeholder for the header, which should be replaced by the folder name.
OLD_HEADER_PLACEHOLDER = "# YOUR_FOLDER_NAME_PLACEHOLDER"

# New placeholder. If this is found in a README.md, the script will generate
# the *full* README template, overwriting existing content. This is for initializing
# new problem folders.
NEW_TEMPLATE_PLACEHOLDER = "# NEW_README_TEMPLATE_PLACEHOLDER"

# HTML-like comments to delimit the code block in README.md.
# Content between these markers will be replaced by the Code.cpp content.
CODE_START_MARKER = "<!-- CODE_START -->"
CODE_END_MARKER = "<!-- CODE_END -->"

# Specific old code link pattern to look for and replace.
OLD_CODE_LINK_PATTERN = r"\[Code\.cpp\]\(Code\.cpp\)" # Regex to match "[Code.cpp](Code.cpp)"

# Markers for the description section placeholder. This allows the user to
# easily replace the default description while keeping the structure.
DESCRIPTION_START_MARKER = "<!-- DESCRIPTION_PLACEHOLDER_START -->"
DESCRIPTION_END_MARKER = "<!-- DESCRIPTION_PLACEHOLDER_END -->"

# Default content for the description when a new template is generated.
DEFAULT_DESCRIPTION_CONTENT = """*(You can add a description of the problem solved in this folder here, e.g., "This folder contains the solution for reversing a singly linked list.")*"""

# --- Template Generation Function ---
def generate_full_readme_template(folder_name: str, code_content: str) -> str:
    """
    Generates the complete README.md content based on the folder name and code.
    This function is used when the NEW_TEMPLATE_PLACEHOLDER is found, effectively
    creating a new README.md from scratch with the defined structure.
    """
    
    # Format the code block for Markdown with 'cpp' syntax highlighting.
    code_block_md = ""
    if code_content:
        code_block_md = f"\n```cpp\n{code_content.strip()}\n```"

    template = f"""# {folder_name}

This section provides an overview and visual aid for this problem.

<details>
<summary>Click to view the Approach Diagram</summary>
<br/>
![Approach Diagram](image/approach.png)
</details>

### Description

{DESCRIPTION_START_MARKER}
{DEFAULT_DESCRIPTION_CONTENT}
{DESCRIPTION_END_MARKER}

### Code

{CODE_START_MARKER}{code_block_md}
{CODE_END_MARKER}
"""
    return template

# --- Main Update Logic ---
def update_readme_files():
    """
    Scans the Git repository for README.md files and updates them.
    It identifies whether a README needs a full template generation,
    specific section updates (header, code block), or conversion from old link.
    """
    print("Running pre-commit hook to update README.md files...")

    # Get the root directory of the Git repository.
    git_root = os.popen('git rev-parse --show-toplevel').read().strip()
    if not git_root:
        print("Error: Not inside a Git repository. Skipping README update.")
        sys.exit(1)

    processed_any_readme = False

    for root, dirs, files in os.walk(git_root):
        # Skip Git internal directories and other common non-content directories
        if '.git' in root or '.vscode' in root or 'venv' in root or '__pycache__' in root or 'node_modules' in root:
            dirs[:] = []
            continue
        
        # Check if 'readme.md' (case-insensitive) exists in the current directory.
        if 'readme.md' in [f.lower() for f in files]:
            readme_path = os.path.join(root, 'README.md')
            parent_dir_name = os.path.basename(root)
            if not parent_dir_name:
                parent_dir_name = os.path.basename(git_root)
            
            relative_readme_path = os.path.relpath(readme_path, git_root)

            # Read Code.cpp content
            code_file_path = os.path.join(root, 'Code.cpp')
            code_content = ""
            if os.path.exists(code_file_path):
                try:
                    with open(code_file_path, 'r', encoding='utf-8') as f:
                        code_content = f.read()
                except Exception as e:
                    print(f"Warning: Could not read '{code_file_path}': {e}. Code block might be empty for '{relative_readme_path}'.")
            
            # Read current README.md content
            original_content = ""
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    original_content = f.read()
            except Exception as e:
                print(f"Error reading '{readme_path}': {e}. Skipping this README.")
                continue

            new_content = original_content
            modified = False
            processed_any_readme = True

            # --- Scenario 1: Initial Template Generation for New READMEs ---
            if NEW_TEMPLATE_PLACEHOLDER in original_content:
                print(f"Generating full template for: {relative_readme_path}")
                new_content = generate_full_readme_template(parent_dir_name, code_content)
                modified = True
            
            # --- Scenario 2: Update Existing READMEs ---
            else:
                # Update Header: If the old placeholder is still present.
                if OLD_HEADER_PLACEHOLDER in new_content:
                    new_content = new_content.replace(OLD_HEADER_PLACEHOLDER, f"# {parent_dir_name}", 1)
                    modified = True

                # Check if the code block markers are already present
                if CODE_START_MARKER in new_content and CODE_END_MARKER in new_content:
                    start_marker_idx = new_content.find(CODE_START_MARKER)
                    end_marker_idx = new_content.find(CODE_END_MARKER, start_marker_idx)

                    if start_marker_idx != -1 and end_marker_idx != -1:
                        current_code_block_inner_md = ""
                        if code_content:
                            current_code_block_inner_md = f"\n```cpp\n{code_content.strip()}\n```"
                        
                        # Rebuild the new_content by taking parts before and after the code block.
                        new_content_before_code_block = new_content[:start_marker_idx + len(CODE_START_MARKER)]
                        new_content_after_code_block = new_content[end_marker_idx:]
                        
                        new_content = f"{new_content_before_code_block}{current_code_block_inner_md}\n{new_content_after_code_block}"
                        modified = True
                    else:
                        print(f"Warning: {CODE_START_MARKER} or {CODE_END_MARKER} not found correctly in '{relative_readme_path}'. Code block will not be updated via markers.")
                
                # --- NEW LOGIC: Convert old [Code.cpp](Code.cpp) link to inline block ---
                # This runs ONLY if the explicit markers are NOT already present.
                elif re.search(OLD_CODE_LINK_PATTERN, new_content):
                    print(f"Converting old code link to inline block in: {relative_readme_path}")
                    
                    # Construct the new inline code block with markers
                    full_inline_code_block = ""
                    if code_content:
                        full_inline_code_block = f"{CODE_START_MARKER}\n```cpp\n{code_content.strip()}\n```\n{CODE_END_MARKER}"
                    else:
                        full_inline_code_block = f"{CODE_START_MARKER}\n<!-- No Code.cpp content found to embed. Create or add content to Code.cpp. -->\n{CODE_END_MARKER}"
                    
                    # Use re.sub to replace the old link with the new structure.
                    # This targets only the specific link and inserts the block.
                    new_content = re.sub(OLD_CODE_LINK_PATTERN, full_inline_code_block, new_content, 1) # Limit to 1 replacement
                    modified = True

            # --- Write and Stage if Content Has Changed ---
            if modified and new_content != original_content:
                try:
                    with open(readme_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated and staged: {relative_readme_path}")
                    os.system(f'git add "{readme_path}"')
                except Exception as e:
                    print(f"Error writing or staging '{readme_path}': {e}")
            elif processed_any_readme:
                print(f"No changes needed for: {relative_readme_path}")
    
    if not processed_any_readme:
        print("No README.md files found or processed in the repository.")

# --- Entry Point ---
if __name__ == "__main__":
    update_readme_files()