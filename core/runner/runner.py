import subprocess
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

DISTROS = {
    "arch": "Dockerfile.arch",
    "ubuntu": "Dockerfile.ubuntu",
    "debian": "Dockerfile.debian",
    "fedora": "Dockerfile.fedora",
    "alpine": "Dockerfile.alpine"
}

def build_image(distro_name, dockerfile_name):
    image_tag = f"distro-doctor-{distro_name}"
    check_cmd = ["docker", "image", "inspect", image_tag]
    if subprocess.run(check_cmd, capture_output=True).returncode == 0:
        return True

    distros_dir = os.path.join(os.path.dirname(__file__), "..", "..", "distros")
    dockerfile_path = os.path.join(distros_dir, dockerfile_name)
    cmd = ["docker", "build", "-t", image_tag, "-f", dockerfile_path, distros_dir]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def run_in_distro(distro_name, steps):
    image_tag = f"distro-doctor-{distro_name}"
    script_content = "\n".join(steps)
    docker_cmd = ["docker", "run", "--rm", "-i", image_tag, "bash"]
    try:
        process = subprocess.run(
            docker_cmd,
            input=script_content,
            text=True,
            capture_output=True,
            timeout=60
        )
        return {
            "distro": distro_name,
            "success": process.returncode == 0,
            "output": process.stdout,
            "error": process.stderr if process.returncode != 0 else ""
        }
    except subprocess.TimeoutExpired:
        return {
            "distro": distro_name,
            "success": False,
            "output": "",
            "error": "Execution timed out after 60 seconds."
        }

def test_single_distro(distro, dockerfile, steps, translate_func):
    if not build_image(distro, dockerfile):
        return distro, {
            "distro": distro,
            "success": False,
            "output": "",
            "error": "Container build failed."
        }
    distro_steps = translate_func(steps, distro)
    res = run_in_distro(distro, distro_steps)
    return distro, res

def run_matrix_parallel(steps, translate_func):
    results = {}
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_distro = {
            executor.submit(test_single_distro, distro, dockerfile, steps, translate_func): distro
            for distro, dockerfile in DISTROS.items()
        }
        for future in as_completed(future_to_distro):
            distro, res = future.result()
            results[distro] = res
    return results