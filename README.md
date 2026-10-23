# 🩺 distro-doctor

> Professional-grade DevOps CLI and CI/CD utility for automatically validating project installation instructions across multiple Linux distributions in parallel using sandboxed Docker containers.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-containerized-2496ED.svg)](https://www.docker.com/)
[![DuckDB](https://img.shields.io/badge/duckdb-analytics-FFF000.svg)](https://duckdb.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Overview

Writing a `README.md` with installation commands (`apt`, `pacman`, `dnf`, `pip`) is standard practice, but verifying that your setup guide actually works across fragmented Linux environments is a significant challenge. 

**distro-doctor** solves this by automatically parsing installation steps, spinning up isolated containers across **Arch Linux, Ubuntu, Debian, Fedora, and Alpine**, executing commands concurrently in parallel, and tracking failure analytics via DuckDB.

---

## 📁 Repository Structure

```text
distro-doctor/
├── cli/
│   ├── __init__.py
│   └── main.py              # Dual-mode CLI entrypoint (run & test)
├── core/
│   ├── analytics/
│   │   └── analytics.py     # DuckDB-backed historical execution tracking
│   ├── parser/
│   │   └── parser.py        # Strict regex Markdown parser & REPL filter
│   ├── runner/
│   │   └── runner.py        # Multi-threaded parallel Docker container runner
│   └── translator/
│       ├── mappings.yml     # Cross-distro package manager mappings
│       └── translator.py    # Package syntax & name translation layer
├── distros/
│   ├── Dockerfile.alpine
│   ├── Dockerfile.arch
│   ├── Dockerfile.debian
│   ├── Dockerfile.fedora
│   └── Dockerfile.ubuntu
├── action.yml               # Official GitHub Actions composite action
├── pyproject.toml           # Global packaging & script configuration
├── .gitignore               # Privacy & clean version control rules
└── README.md                # Project documentation

```

---

## 🚀 Tech Stack & Tooling

* **Language**: Python 3.10+ (Modular architecture with clean separation of concerns).
* **Containerization**: Docker (Isolated multi-distro sandboxed environments).
* **Persistence & Analytics**: DuckDB (Lightweight, high-performance analytical engine tracking success rates and distro fragility).
* **Packaging**: Setuptools & PyYAML (`pyproject.toml` configuration exposing global system commands).
* **CI/CD**: GitHub Actions composite actions for automated pull request auditing.

---

## ⚙️ Prerequisites & Installation

**Prerequisites:**

* Python 3.10+
* Docker Daemon running locally (`sudo systemctl start docker`)

**Global System Installation:**
Clone the repository and install it globally in editable mode via `pip`:

```bash
git clone [https://github.com/Braveen811/distro-doctor.git](https://github.com/Braveen811/distro-doctor.git)
cd distro-doctor
pip install -e .

```

Once installed, the `distro-doctor` command is globally available from any terminal on your system.

---

## 💡 The Two Ways to Use Distro-Doctor

Depending on your workflow, `distro-doctor` supports two distinct operating modes:

### Option 1: Local Workspace Mode (`distro-doctor run`)

* **How it works**: Reads the `README.md` in your current working directory, extracts setup steps, and executes the test matrix.
* **Best for**: Developers actively writing and testing their own projects locally before pushing code.
* **Usage**:

```bash
cd ~/Projects/your-project
distro-doctor run

```

### Option 2: Remote URL Mode (`distro-doctor test <url>`)

* **How it works**: Securely clones any public GitHub repository into an isolated temporary directory, parses its README, previews commands, prompts for confirmation, runs the test matrix, and automatically cleans up.
* **Best for**: Beginners and maintainers auditing open-source repositories instantly without manual cloning.
* **Usage**:

```bash
distro-doctor test [https://github.com/psf/requests](https://github.com/psf/requests)

```

---

## 🧪 Testing & Validation

When executed, `distro-doctor` initiates a concurrent thread pool dispatching commands across **5 distinct Linux containers** simultaneously:

```text
Linux distro    Result       Problem
──────────────────────────────────────────────────
Alpine          PASS         None
Debian          PASS         None
Ubuntu          PASS         None
Fedora          PASS         None
Arch            PASS         None

```

DuckDB aggregates historical performance metrics in real time:

```text
📈 Analytics: Total Runs: 70 | Success Rate: 62.86% | Most Fragile: ubuntu

```

---

## 🛡️ Security Model & Hardening

* **Isolated Sandboxing**: All installation commands run inside ephemeral, unprivileged Docker containers, ensuring zero impact on the host system.
* **Temporary Directory Hygiene**: Remote URL tests utilize secure Python `tempfile` contexts with automatic cleanup handlers to prevent disk bloat and leaking credentials.
* **Strict Markdown Parsing**: The parser isolates true shell code blocks (`bash`, `sh`) while stripping out narrative prose, code comments, and interactive Python REPL artifacts (`>>>`, `...`) to prevent command injection and syntax errors.

---

## 🧠 Core Engine Features

* **Smart REPL Bypassing**: Automatically skips Python interactive shell snippets (`>>> import ...`) inside documentation code blocks.
* **Cross-Distro Translation Layer**: Resolves package name discrepancies between `apt` (`libssl-dev`), `pacman` (`openssl`), and `dnf` (`openssl-devel`).
* **Robust Exception Handling**: Gracefully handles network failures during remote git cloning and missing README errors.

---

## 🔧 System Troubleshooting & Tips

* **Docker Daemon Error**: Ensure the Docker service is running on your machine (`sudo systemctl start docker`).
* **Virtual Environment**: Always activate your Python virtual environment before installing or developing (`source venv/bin/activate`).
* **URL Escaping in Zsh**: When passing URLs with special characters, avoid enclosing them in quotes or square brackets improperly to prevent Zsh globbing errors.

---

## 🗺️ Roadmap & Contributing

**Planned Features:**

* [ ] Native GitHub Actions Composite Action for CI pipelines.
* [ ] JSON export for DuckDB analytics to power React-based dashboards.

**Contributing:**
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://www.google.com/search?q=https://github.com/Braveen811/distro-doctor/issues).

**License:**
Distributed under the MIT License.

---

**Author:** [Braveen R](https://braveenr.linklee.in/)

---
## ✌️ Wrapping Up & Operational Modes

`distro-doctor` bridges the gap between documentation and cross-platform reliability, turning multi-distro QA into an automated, seamless experience across both execution modes:

* **Local Mode (`distro-doctor run`)**: Instant validation for developers testing their own local workspace READMEs.
* **Remote URL Mode (`distro-doctor test <url>`)**: Instant auditing for maintainers and beginners checking any public GitHub repository by URL without manual cloning.

Distributed under the MIT License. Contributions, issues, and feature requests are welcome!


See you in the terminal!
