#!/usr/bin/env python3
# /// script
# dependencies = [
#   "pyyaml",
# ]
# ///

"""
Update README.md and index.html with data from customizations.yml
"""

import yaml
from pathlib import Path

def load_customizations():
    """Load customizations from YAML file"""
    with open('customizations/customizations.yml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data.get('customizations', [])

def generate_markdown_table(customizations):
    """Generate markdown table for README.md"""
    lines = [
        "| Type | Title | Description |",
        "|------|-------|-------------|"
    ]
    
    for item in customizations:
        # Extract just the title text (without the link) for display
        title_text = item['title'].split('](')[0].replace('[', '')
        # Keep the markdown link in the title
        lines.append(f"| {item['type']} | {item['title']} | {item['description']} |")
    
    return '\n'.join(lines)

def generate_html_table_rows(customizations):
    """Generate HTML table rows for index.html"""
    rows = []
    
    for item in customizations:
        # Extract title text and file path from markdown link
        title_match = item['title']
        title_text = title_match.split('](')[0].replace('[', '')
        file_path = title_match.split('](')[1].replace(')', '')
        
        # Determine install URL type
        if item['type'] == 'Agent':
            url_type = 'chat-agent'
        elif item['type'] == 'Prompt':
            url_type = 'chat-prompt'
        else:
            url_type = 'chat-instructions'
        
        install_url = f"https://raw.githubusercontent.com/rjdinis-nos/.copilot/refs/heads/main/{file_path}"
        github_url = f"https://github.com/rjdinis-nos/.copilot/blob/main/{file_path}"
        
        row = f'''      <tr>
        <td>{item['type']}</td>
        <td>
          <strong><a href="{github_url}">{title_text}</a></strong>
          <br />
          <a
            class="install-btn"
            href="vscode:{url_type}/install?url={install_url}"
          >
            VS Code Install
          </a>
        </td>
        <td>
          {item['description']}
        </td>
      </tr>'''
        rows.append(row)
    
    return '\n'.join(rows)

def update_readme(customizations):
    """Update README.md with new table"""
    readme_path = Path('README.md')
    content = readme_path.read_text(encoding='utf-8')
    
    # Sort customizations by type, then by title
    sorted_customizations = sorted(customizations, key=lambda x: (x['type'], x['title']))
    
    # Generate new table
    new_table = generate_markdown_table(sorted_customizations)
    
    # Replace table between ## Available Customizations and ## License
    import re
    pattern = r'(## Available Customizations\s*\n\n)(.*?)(\n\n## License)'
    replacement = f'\\1{new_table}\\3'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content != content:
        readme_path.write_text(new_content, encoding='utf-8')
        print("✓ Updated README.md")
        return True
    else:
        print("  README.md unchanged")
        return False

def update_index_html(customizations):
    """Update index.html with new table rows"""
    html_path = Path('index.html')
    content = html_path.read_text(encoding='utf-8')
    
    # Sort customizations by type, then by title
    sorted_customizations = sorted(customizations, key=lambda x: (x['type'], x['title']))
    
    # Generate new table rows
    new_rows = generate_html_table_rows(sorted_customizations)
    
    # Replace tbody content
    import re
    pattern = r'(<tbody>\s*\n)(.*?)(\n\s*</tbody>)'
    replacement = f'\\1{new_rows}\\3'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content != content:
        html_path.write_text(new_content, encoding='utf-8')
        print("✓ Updated index.html")
        return True
    else:
        print("  index.html unchanged")
        return False

def main():
    print("Updating documentation from customizations/customizations.yml...")
    
    # Load customizations
    customizations = load_customizations()
    print(f"Loaded {len(customizations)} customizations")
    
    # Update files
    readme_updated = update_readme(customizations)
    html_updated = update_index_html(customizations)
    
    if readme_updated or html_updated:
        print("✓ Documentation updated successfully")
    else:
        print("✓ No changes needed")

if __name__ == '__main__':
    main()
