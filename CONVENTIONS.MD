# 🧭 Conventions – VaultCLI Project

This document defines the coding and development conventions used in the **VaultCLI** project.  
It ensures that all code remains clean, readable, maintainable, and consistent throughout the project.

---

## 1. Philosophy

- Code should be **clear**, **simple**, and **consistent**.  
- Follow the **PEP 8** (Python style guide) and **PEP 257** (docstring conventions).  
- Prioritize **readability over cleverness** — code is read more often than it is written.  
- Each module and function must have **one clear responsibility** (Single Responsibility Principle).  
- Prefer explicit code to implicit behavior (`import this` → “Explicit is better than implicit.”).

---

## 2. Project Structure

Each module serves a specific purpose.

```
vaultcli/
│
├── src/
│   ├── __init__.py
│   ├── cli.py           # Handles command-line parsing and user interaction
│   ├── encryption.py    # Encryption and decryption logic
│   ├── storage.py       # Reading and writing encrypted data
│   ├── auth.py          # Master password setup and verification
│   ├── password_gen.py  # Random password generation
│   └── utils.py         # Helper functions and formatting tools
│
├── requirements.txt
├── setup.py
└── README.md
```

This structure follows modular design and makes testing and maintenance easier.

---

## 3. Naming Conventions

| Type                | Convention              | Example                |
|---------------------|------------------------|------------------------|
| Variable / Function | `snake_case`           | `get_vault_data()`     |
| Class               | `PascalCase`           | `PasswordManager`      |
| Constant            | `ALL_CAPS`             | `DEFAULT_VAULT_PATH`   |
| File / Module       | lowercase_with_underscores | `storage.py`        |

Avoid abbreviations unless widely known (`db`, `pwd`, etc.).

---

## 4. Functions and Classes

- Functions should be short (under ~25 lines).  
- Each function does one job only.  
- Use **type hints** for parameters and return values.  
- All public functions must include **docstrings** in this format:

```python
def encrypt_data(data: dict, key: bytes) -> bytes:
    """
    Encrypts a dictionary into an encrypted byte string.

    Args:
        data (dict): The data to encrypt.
        key (bytes): The encryption key.

    Returns:
        bytes: The encrypted data.
    """
```

---

## 5. Formatting and Linting

- Indentation: 4 spaces (never tabs).
- Maximum line length: 88 characters.
- Use Black for automatic formatting and Ruff (or Flake8) for linting.
- No unused imports or commented-out code should remain in commits.
- Separate logical code blocks with blank lines for clarity.

---

## 6. Git Commit Conventions

Follow Conventional Commits syntax:

```
<type>: <short description>
```

Common types:

- feat: new feature
- fix: bug fix
- refactor: code improvement without changing behavior
- docs: documentation update
- test: add or modify tests
- chore: maintenance or setup task

Example commits:

```
feat: add encryption support to vault storage
fix: handle missing vault file gracefully
docs: update conventions.md with new naming rules
```

---

## 7. Testing Guidelines

- Use pytest for all tests.
- Each module has a corresponding test file in the tests/ directory.
- Test function names must start with `test_`.
- Tests must be independent — no shared files or state.
- Each test should verify a single behavior or function.

---

## 8. Error Handling and Logging

- Use exceptions for real errors, not flow control.
- CLI layer (`cli.py`) should catch exceptions and display clear messages.
- Logic modules should not print directly to the console.
- Optionally use the logging module for debugging or error logs.

---

## 9. Documentation and Comments

- Prefer descriptive variable names over excessive comments.
- Use comments only when logic isn’t obvious.
- Each module begins with a short header docstring describing its role.
- Public functions and classes must have docstrings.

Example:

```python
"""
Module: storage
Handles reading and writing encrypted vault data to disk.
"""
```

---

## 10. Collaboration Rules

Even if this project is individual, follow professional habits:

- Code must pass all tests and linters before being considered “done.”
- Keep dependencies minimal and listed in `requirements.txt`.
- Write meaningful commit messages and small commits.
- Avoid pushing experimental or broken code to the main branch.

