import re

def extract_install_steps(readme_path):
    if not readme_path:
        return []
        
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Match code blocks with optional language specifier: ```lang\n...```
    pattern = r"```([a-zA-Z0-9_-]*)\s*\n(.*?)```"
    matches = re.findall(pattern, content, re.DOTALL)
    
    steps = []
    for lang, match in matches:
        # Skip python/code examples as they are not shell installation scripts
        if lang and lang.lower() in ["python", "py", "pycon", "json", "yaml", "yml", "javascript", "js"]:
            continue
            
        lines = match.strip().splitlines()
        for line in lines:
            line = line.strip()
            
            # Skip empty lines, comments, or python REPL lines
            if not line or line.startswith("#") or line.startswith(">>>") or line.startswith("..."):
                continue
                
            # Strip leading shell prompt symbols if present
            if line.startswith("$ "):
                line = line[2:].strip()
                
            steps.append(line)
                
    return steps
