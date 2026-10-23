import os
import yaml

def load_mappings():
    mapping_path = os.path.join(os.path.dirname(__file__), "mappings.yml")
    if not os.path.exists(mapping_path):
        return {}
    with open(mapping_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def translate_steps(steps, distro):
    mappings = load_mappings()
    translated_steps = []
    
    for step in steps:
        modified_step = step
        
        # Translate generic 'python ' commands to 'python3 ' for debian/ubuntu/fedora
        if distro in ["ubuntu", "debian", "fedora"]:
            modified_step = modified_step.replace("python -c", "python3 -c")
            modified_step = modified_step.replace("python ", "python3 ")

        # Translate package names using YAML mappings
        for pkg, distro_map in mappings.items():
            if pkg in modified_step and distro in distro_map:
                target_pkg = distro_map[distro]
                modified_step = modified_step.replace(pkg, target_pkg)
                
        translated_steps.append(modified_step)
        
    return translated_steps