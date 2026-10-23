import re

def extract_install_steps(readme_path):
    if not readme_path:
        return []
        
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Universally capture ALL code blocks to prevent inverted matching.
    # Group 1 = language tag (if any), Group 2 = inner content.
    pattern = r"```([a-zA-Z0-9_+-]*)\s*\n(.*?)```"
    matches = re.findall(pattern, content, re.DOTALL)
    
    steps = []
    for lang, match in matches:
        lang = lang.strip().lower()
        
        # 2. Safely ignore non-shell languages
        if lang in ["python", "py", "pycon", "json", "yaml", "yml", "js", "html", "css", "dockerfile"]:
            continue
            
        # 3. Process the valid shell/console/empty blocks
        for line in match.strip().splitlines():
            line = line.strip()
            
            # Filter out comments and Python REPL artifacts
            if not line or line.startswith(("#", ">>>", "...")):
                continue
                
            # Strip standard shell prompt indicators
            if line.startswith("$ "):
                line = line[2:].strip()
                
            steps.append(line)
                
    return steps
