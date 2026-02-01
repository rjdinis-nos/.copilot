#!/usr/bin/env python3
# /// script
# dependencies = [
#   "pyyaml",
#   "gitpython",
# ]
# ///

"""
Build script to generate customizations.yml from agent and instruction files.
Parses frontmatter from .agent.md and .instructions.md files.
"""

import os
import re
import yaml
from pathlib import Path
from git import Repo

def derive_title_from_filename(filename):
    """Convert filename to title (e.g., uv_python_init.agent.md -> UV Python Init)"""
    # Remove extension
    name = filename.replace('.agent.md', '').replace('.instructions.md', '').replace('.prompt.md', '')
    # Split on underscores and capitalize each word
    words = name.split('_')
    # Handle special cases for acronyms
    title_words = []
    for word in words:
        if word.upper() in ['UV', 'API', 'CI', 'CD', 'HTTP', 'URL']:
            title_words.append(word.upper())
        else:
            title_words.append(word.capitalize())
    return ' '.join(title_words)

def get_git_remote_url():
    """Extract GitHub repository URL from git remote"""
    try:
        repo = Repo('.')
        if repo.remotes:
            # Get origin remote URL
            origin_url = repo.remotes.origin.url
            # Convert SSH to HTTPS if needed
            if origin_url.startswith('git@github.com:'):
                origin_url = origin_url.replace('git@github.com:', 'https://github.com/')
            # Remove .git suffix
            origin_url = origin_url.rstrip('.git')
            return origin_url
    except Exception:
        print("Warning: Could not detect git remote URL")
        return None

def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown file content"""
    # Look for code block wrapper (```chatagent or ```instructions)
    code_block_pattern = r'^```(?:chatagent|instructions)\s*\n(.*?)\n```'
    match = re.search(code_block_pattern, content, re.DOTALL | re.MULTILINE)
    
    if match:
        inner_content = match.group(1)
    else:
        inner_content = content
    
    # Extract frontmatter between --- delimiters
    frontmatter_pattern = r'^---\s*\n(.*?)\n---'
    fm_match = re.search(frontmatter_pattern, inner_content, re.DOTALL | re.MULTILINE)
    
    if fm_match:
        try:
            return yaml.safe_load(fm_match.group(1))
        except yaml.YAMLError:
            print("Warning: Failed to parse YAML frontmatter")
            return {}
    return {}

def scan_directory(directory, file_extension, item_type):
    """Scan directory for files with given extension and extract metadata"""
    items = []
    dir_path = Path(directory).resolve()
    base_path = Path('.').resolve()
    
    # Validate directory is within workspace
    if not str(dir_path).startswith(str(base_path)):
        print(f"Warning: Directory {directory} is outside workspace")
        return items
    
    if not dir_path.exists():
        print(f"Warning: Directory {directory} does not exist")
        return items
    
    for file_path in dir_path.glob(f'**/*{file_extension}'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            frontmatter = parse_frontmatter(content)
            
            # For prompts without frontmatter, extract description from first paragraph or heading
            if 'description' not in frontmatter and item_type == 'Prompt':
                # Look for first paragraph after the title
                lines = content.split('\n')
                description = ''
                for i, line in enumerate(lines):
                    if line.strip().startswith('#') and i + 2 < len(lines):
                        # Get the paragraph after the first heading
                        next_para = lines[i + 2].strip()
                        if next_para and not next_para.startswith('#'):
                            description = next_para
                            break
                frontmatter['description'] = description if description else 'Copilot prompt'
            
            # Validate required fields
            if 'description' not in frontmatter:
                print(f"Warning: Missing 'description' in {file_path}")
                frontmatter['description'] = ''
            
            # Derive title from filename
            filename = file_path.name
            title = derive_title_from_filename(filename)
            
            # Get relative path from project root
            relative_path = file_path.relative_to(base_path)
            
            items.append({
                'type': item_type,
                'title': title,
                'description': frontmatter.get('description', ''),
                'file': str(relative_path),
                'metadata': frontmatter
            })
            
        except Exception:
            print(f"Warning: Failed to process {file_path}")
    
    return items

def generate_install_url(item, base_url, branch='main'):
    """Generate VS Code install URL for an item"""
    if not base_url:
        return ''
    
    raw_url = f"https://raw.githubusercontent.com/{base_url.split('github.com/')[-1]}/refs/heads/{branch}/{item['file']}"
    
    if item['type'] == 'Agent':
        return f"vscode:chat-agent/install?url={raw_url}"
    elif item['type'] == 'Instruction':
        return f"vscode:chat-instructions/install?url={raw_url}"
    return ''

def main():
    print("Building customizations.yml...")
    
    # Get git remote URL
    git_url = get_git_remote_url()
    if git_url:
        print(f"Detected repository: {git_url}")
    
    # Scan directories
    agents = scan_directory('customizations/agents', '.agent.md', 'Agent')
    instructions = scan_directory('customizations/instructions', '.instructions.md', 'Instruction')
    prompts = scan_directory('customizations/prompts', '.prompt.md', 'Prompt')
    
    # Combine into flat array
    all_items = agents + instructions + prompts
    
    # Keep only table fields: type, title, description
    # Add markdown link to file in title
    simplified_items = []
    for item in all_items:
        title_with_link = f"[{item['title']}]({item['file']})"
        simplified_items.append({
            'type': item['type'],
            'title': title_with_link,
            'description': item['description']
        })
    
    # Generate YAML output
    output = {
        'customizations': simplified_items
    }
    
    # Write to file
    with open('customizations/customizations.yml', 'w', encoding='utf-8') as f:
        yaml.dump(output, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"✓ Generated customizations.yml with {len(all_items)} items")
    print(f"  - {len(agents)} agents")
    print(f"  - {len(instructions)} instructions")
    print(f"  - {len(prompts)} prompts")

if __name__ == '__main__':
    main()
