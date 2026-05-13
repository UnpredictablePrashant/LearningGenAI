#!/usr/bin/env python3
"""
Environment verification script for LearningGenAI.

Run this before starting any session to confirm your setup is correct.

Usage:
    python setup_check.py
"""

import sys
import os


RESET = "\033[0m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
BOLD = "\033[1m"


def pass_msg(msg: str) -> None:
    print(f"  {GREEN}PASS{RESET}  {msg}")


def fail_msg(msg: str) -> None:
    print(f"  {RED}FAIL{RESET}  {msg}")


def warn_msg(msg: str) -> None:
    print(f"  {YELLOW}WARN{RESET}  {msg}")


def check_python_version() -> bool:
    required = (3, 10)
    current = sys.version_info[:2]
    version_str = sys.version.split()[0]
    if current >= required:
        pass_msg(f"Python {version_str}")
        return True
    else:
        fail_msg(f"Python {version_str} — need Python >= 3.10")
        fail_msg("  Download from https://python.org/downloads")
        return False


def check_import(import_name: str, package_name: str | None = None) -> bool:
    """Try importing a module. Returns True if successful, False if not."""
    display = package_name or import_name
    try:
        mod = __import__(import_name)
        version = getattr(mod, "__version__", "")
        version_str = f" {version}" if version else ""
        pass_msg(f"{display}{version_str}")
        return True
    except ImportError:
        pkg = package_name or import_name
        fail_msg(f"{display} not installed")
        fail_msg(f"  Fix: pip install {pkg}")
        return False


def check_api_key() -> bool | None:
    """Check for ANTHROPIC_API_KEY. Returns None if missing (warning, not error)."""
    # Try loading from .env file
    try:
        from dotenv import load_dotenv
        if os.path.exists(".env"):
            load_dotenv()
    except ImportError:
        pass  # python-dotenv might not be installed yet

    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if key and len(key) > 20:
        masked = key[:8] + "..." + key[-4:]
        pass_msg(f"ANTHROPIC_API_KEY is set ({masked})")
        return True
    else:
        warn_msg("ANTHROPIC_API_KEY not set")
        warn_msg("  Needed for Sessions 02+. Session 01 works without it.")
        warn_msg("  Fix: copy .env.example to .env and add your key")
        return None


def check_session01_imports() -> bool:
    """Quick functional check for Session 01 specific imports."""
    all_ok = True
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        tokens = enc.encode("hello world")
        assert len(tokens) == 2
        pass_msg("tiktoken functional check (tokenize 'hello world' → 2 tokens)")
    except Exception as e:
        fail_msg(f"tiktoken functional check failed: {e}")
        all_ok = False

    try:
        import numpy as np
        a = np.array([1.0, 0.0])
        b = np.array([0.0, 1.0])
        sim = float(np.dot(a, b))
        assert sim == 0.0
        pass_msg("numpy functional check (dot product)")
    except Exception as e:
        fail_msg(f"numpy functional check failed: {e}")
        all_ok = False

    return all_ok


def main() -> None:
    print()
    print(f"{BOLD}{'=' * 52}{RESET}")
    print(f"{BOLD}  LearningGenAI — Environment Check{RESET}")
    print(f"{BOLD}{'=' * 52}{RESET}")

    failures: list[str] = []

    print("\nPython version:")
    if not check_python_version():
        failures.append("python version")

    print("\nRequired packages:")
    packages = [
        ("tiktoken", None),
        ("sentence_transformers", "sentence-transformers"),
        ("numpy", None),
        ("anthropic", None),
        ("openai", None),
        ("pypdf", None),
        ("langchain_text_splitters", "langchain-text-splitters"),
        ("chromadb", None),
        ("dotenv", "python-dotenv"),
    ]
    for import_name, package_name in packages:
        if not check_import(import_name, package_name):
            failures.append(package_name or import_name)

    print("\nFunctional checks (Session 01):")
    if not check_session01_imports():
        failures.append("functional checks")

    print("\nAPI keys:")
    check_api_key()  # Warning only, not a failure

    print()
    print(f"{BOLD}{'=' * 52}{RESET}")
    if failures:
        print(f"\n  {RED}Found {len(failures)} issue(s):{RESET}")
        for f in failures:
            print(f"    - {f}")
        print("\n  Fix the issues above, then re-run:")
        print("    pip install -r requirements.txt")
        print("    python setup_check.py")
        sys.exit(1)
    else:
        print(f"\n  {GREEN}All checks passed!{RESET}")
        print("  You're ready for Session 01.")
        print("  Start here: sessions/01_how_llms_work/README.md")
    print(f"{BOLD}{'=' * 52}{RESET}")
    print()


if __name__ == "__main__":
    main()
