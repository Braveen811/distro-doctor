import sys
import os
import tempfile
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.parser.parser import extract_install_steps
from core.runner.runner import DISTROS, run_matrix_parallel
from core.translator.translator import translate_steps
from core.analytics.analytics import log_results, get_analytics_summary

# ANSI Colors for gorgeous CLI UI
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

def print_banner():
    print(f"{CYAN}{BOLD}┌──────────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}{BOLD}│ 🩺  DISTRO-DOCTOR | Multi-Distro CI/CD CLI   │{RESET}")
    print(f"{CYAN}{BOLD}└──────────────────────────────────────────────┘{RESET}")

def execute_matrix_flow(working_dir, source_label):
    readme_path = os.path.join(working_dir, "README.md")
    print(f"{DIM}[*] Reading installation steps from {source_label}/README.md...{RESET}")
    
    if not os.path.exists(readme_path):
        print(f"{RED}[!] Error: No README.md found in {source_label}.{RESET}")
        return

    steps = extract_install_steps(readme_path)
    if not steps:
        print(f"{RED}[!] No bash code blocks or installation steps found in README.md.{RESET}")
        return
    
    print(f"{GREEN}[+] Found {len(steps)} installation command(s):{RESET}")
    for idx, step in enumerate(steps, 1):
        print(f"    {DIM}{idx}. {step}{RESET}")
    
    # Option 2 confirmation prompt for remote repos
    if source_label != "local directory":
        choice = input(f"\n{YELLOW}[?] Do you want to proceed with testing these commands in isolated containers? [y/N]: {RESET}").strip().lower()
        if choice != 'y':
            print(f"{YELLOW}[!] Aborted by user.{RESET}")
            return

    print(f"\n{YELLOW}[⚡] Running parallel multi-distro test matrix across 5 containers...{RESET}")
    
    matrix_results = run_matrix_parallel(steps, translate_steps)
    log_results(matrix_results)

    # Styled Matrix Output Table
    print(f"\n{BOLD}{'Linux distro':<15} {'Result':<12} {'Problem'}{RESET}")
    print(f"{DIM}─" * 50 + f"{RESET}")
    
    for distro, res in matrix_results.items():
        success = res["success"]
        status_badge = f"{GREEN}PASS{RESET}" if success else f"{RED}FAIL{RESET}"
        
        if success:
            problem = f"{DIM}None{RESET}"
        else:
            err_lines = [l.strip() for l in res.get("error", "").splitlines() if l.strip()]
            problem = f"{RED}{err_lines[-1] if err_lines else 'None'}{RESET}"
            if len(problem) > 30:
                problem = problem[:27] + "..."
        
        print(f"{distro.capitalize().ljust(15)} {status_badge:<21} {problem}")

    print(f"\n{CYAN}{BOLD}Suggested fixes{RESET}")
    print(f"{BOLD}Ubuntu / Debian{RESET}")
    print("sudo apt install libssl-dev")
    print(f"{BOLD}Arch{RESET}")
    print("sudo pacman -S openssl")
    print(f"{BOLD}Fedora{RESET}")
    print("sudo dnf install openssl-devel")

    summary = get_analytics_summary()
    if isinstance(summary, dict):
        print(f"\n{DIM}──────────────────────────────────────────────────{RESET}")
        print(f"{CYAN}📈 Analytics:{RESET} Total Runs: {summary['total_runs']} | Success Rate: {summary['success_rate']}% | Most Fragile: {summary['most_fragile_distro']}")
        print(f"{DIM}──────────────────────────────────────────────────{RESET}")

def main():
    print_banner()

    if len(sys.argv) < 2:
        print(f"{YELLOW}Usage:{RESET}")
        print("  python cli/main.py run                # Test current local directory")
        print("  python cli/main.py test <github_url>  # Test remote GitHub repository by URL")
        return

    command = sys.argv[1]

    if command == "run":
        # Option 1: Local execution
        execute_matrix_flow(os.getcwd(), "local directory")

    elif command == "test":
        if len(sys.argv) < 3:
            print(f"{RED}[!] Error: Please provide a GitHub repository URL.{RESET}")
            print("Usage: python cli/main.py test https://github.com/user/repo")
            return
        
        repo_url = sys.argv[2]
        print(f"{DIM}[*] Cloning target repository securely ({repo_url})...{RESET}")
        
        # Option 2: Temporary directory cloning and safe cleanup
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                clone_result = subprocess.run(
                    ["git", "clone", "--depth", "1", repo_url, temp_dir],
                    capture_output=True,
                    text=True
                )
                if clone_result.returncode != 0:
                    print(f"{RED}[!] Failed to clone repository:\n{clone_result.stderr.strip()}{RESET}")
                    return
                
                execute_matrix_flow(temp_dir, repo_url)
                
            except Exception as e:
                print(f"{RED}[!] Error during remote execution: {e}{RESET}")
    else:
        print(f"{RED}[!] Unknown command: {command}{RESET}")
        print("Available commands: run, test")

if __name__ == "__main__":
    main()