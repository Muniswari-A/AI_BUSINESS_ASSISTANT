# Contributing to DCI AI Business Assistant

Thank you for taking the time to contribute! 🎉

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Reporting Issues](#reporting-issues)
- [Style Guidelines](#style-guidelines)

---

## Code of Conduct

Please be respectful and inclusive. We welcome contributors of all experience levels.

---

## How to Contribute

### 🐛 Bug Fixes
1. Check the [Issues](../../issues) tab to see if the bug is already reported.
2. If not, open a new issue with a clear title and description.
3. Fork the repo, create a branch, fix the bug, and open a Pull Request.

### ✨ New Features
1. Open an issue to discuss the feature before coding it.
2. Reference the issue in your Pull Request.

### 📚 Documentation
Improvements to README, docstrings, or inline comments are always welcome!

---

## Development Setup

```bash
# 1. Fork and clone
git clone https://github.com/<your-username>/DCI_AI_BUSINESS_ASSISTANT.git
cd DCI_AI_BUSINESS_ASSISTANT

# 2. Create a virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
# source .venv/bin/activate  # Linux / macOS

# 3. Install dependencies (including test tools)
pip install -r requirements.txt

# 4. Copy environment config
cp .env.example .env

# 5. Ensure Ollama is running
ollama pull llama3.2
ollama serve
```

---

## Submitting a Pull Request

1. **Branch naming**: `feat/<short-description>` or `fix/<short-description>`
2. **Keep PRs focused** — one feature or fix per PR
3. **Write or update tests** for any changed behaviour
4. **Run the test suite** before submitting:
   ```bash
   python -m pytest tests/ -v -s
   ```
5. **Describe your changes** clearly in the PR description

---

## Reporting Issues

When opening an issue, please include:

- **Python version** (`python --version`)
- **Ollama model** in use
- **Steps to reproduce**
- **Expected vs. actual behaviour**
- **Any relevant logs** (copy from console or `uvicorn` output)

---

## Style Guidelines

- Follow **PEP 8** for Python code
- Add **docstrings** to all public functions and classes
- Keep functions small and focused (single responsibility)
- Use **type hints** throughout
- Prefer **`async`/`await`** for I/O-bound operations

---

Thank you for helping make DCI AI Business Assistant better! 🚀
