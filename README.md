# 🔐 Vault-CLI

**A secure command-line password manager built with Python.**

Vault-CLI helps you manage your passwords securely with strong encryption and an intuitive command-line interface. All your passwords are encrypted locally using industry-standard cryptography.

---

## ✨ Features

- 🔒 **Strong Encryption** — AES-256-GCM with PBKDF2 key derivation (200k iterations)
- 🎲 **Password Generator** — Create cryptographically secure passwords with entropy calculation
- 💬 **Interactive CLI** — Smart prompts and helpful defaults
- 🛡️ **Secure by Default** — No plaintext storage, password masking in terminal
- ✅ **Input Validation** — Duplicate detection and confirmation prompts
- 📊 **Detailed Feedback** — Shows username and password info when listing entries

---

## 📦 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/7n4xt/Vault-CLI.git
cd Vault-CLI

# Install the package
pip install -e .
```

### Basic Usage

```bash
# Create a new vault
vault-cli init

# Add a password
vault-cli add --name github --username your_username

# List all entries
vault-cli list

# Get a password
vault-cli get --name github

# Generate a secure password
vault-cli generate --length 20

# Delete an entry
vault-cli delete
```

---

## 💻 Commands

### `init` - Initialize a New Vault
Creates a new encrypted vault file protected by your master password.

```bash
vault-cli init
```

### `add` - Add a Password Entry
Store a new password entry. Supports interactive prompts and password suggestions.

```bash
vault-cli add --name github --username your_username
# Prompts for password or suggests a secure one
# Example: Suggested password (entropy 103.4 bits): ,I}T]R1I;;82O*h5
```

### `list` - View All Entries
Display all stored entries with details (username and password length).

```bash
vault-cli list
```

### `get` - Retrieve a Password
Get a specific password entry by name.

```bash
vault-cli get --name github
```

### `generate` - Generate Strong Passwords
Create cryptographically secure passwords with customizable options.

```bash
vault-cli generate --length 20 --symbols
```

### `delete` - Remove an Entry
Delete a password entry with confirmation prompt.

```bash
vault-cli delete
```

---

## 🔧 Technical Details

### Security
- **AES-256-GCM** encryption (authenticated encryption)
- **PBKDF2-SHA256** key derivation with 200,000 iterations
- Cryptographically secure random generation using Python's `secrets` module
- All passwords encrypted at rest—no plaintext storage

### Architecture
```
src/
├── cli.py           # Command-line interface
├── encryption.py    # AES-GCM encryption with PBKDF2
├── storage.py       # Vault CRUD operations
├── auth.py          # Secure password input
├── password_gen.py  # Password generation with entropy
└── utils.py         # Utility functions
```

### Requirements
- Python 3.7+
- `cryptography` library

---

## 📚 "Les Bonnes Pratiques de Développeur"

**This project showcases professional software development practices.**

Beyond being a functional password manager, Vault-CLI demonstrates how to build clean, maintainable software following industry standards. This makes it an educational resource for developers learning best practices.

### What Makes This Project Special

#### 1. **Clean Code & Architecture**
- Modular design with clear separation of concerns
- PEP 8 compliance and meaningful naming conventions
- Single Responsibility Principle—each function does one thing well
- Type hints and comprehensive docstrings

#### 2. **Development Process**
- Documented conventions in [CONVENTIONS.MD](CONVENTIONS.MD) before building complex features
- Systematic refactoring when code became messy (reduced 624 lines to 208)
- Proper git workflow with Conventional Commits

#### 3. **User Experience Focus**
- Interactive prompts for missing arguments
- Smart defaults and clear error messages
- Confirmation prompts for destructive operations
- Password suggestions with entropy display

#### 4. **Quality Assurance**
- Comprehensive error handling at appropriate layers
- Input validation (duplicate detection, confirmation prompts)
- Secure by default (password masking, encrypted storage)

### Key Takeaways

✅ **Planning** — Established conventions early to prevent technical debt  
✅ **Structure** — Modular architecture makes testing and maintenance easier  
✅ **Refactoring** — Continuously improved code quality through iterative refinement  
✅ **Security** — Used proven cryptographic libraries and best practices  
✅ **UX** — Clear prompts and helpful defaults improve usability  
✅ **Documentation** — Code and conventions documented for future maintainers  

### Notable Issues We Resolved

**File Duplication** — Discovered code duplicated 2-3 times (624 lines), systematically removed duplicates  
**Complex Functions** — Refactored 150-line `main()` into focused handler functions  
**Error Messages** — Replaced cryptic exceptions with clear, actionable user messages  

---

For detailed coding standards and conventions, see [CONVENTIONS.MD](CONVENTIONS.MD).

---

## 🛠️ Technical Stack

| Component | Technology | Reason |
|-----------|-----------|--------|
| CLI Framework | `argparse` | Standard library, no external deps |
| Encryption | `cryptography` (AES-GCM) | Industry-standard, authenticated encryption |
| Key Derivation | PBKDF2-SHA256 | Resistant to brute-force attacks |
| Password Gen | `secrets` module | Cryptographically secure randomness |
| Password Input | `getpass` | Secure, no terminal echo |
| Storage Format | JSON | Human-readable (when decrypted), easy to parse |

---

## 🔍 Code Quality Highlights

### Before Refactoring (Messy Code)
```python
# 150-line main() function with nested if/else
# Duplicate code everywhere
# Hard to follow logic flow
```

### After Refactoring (Clean Code)
```python
def main():
    """Clean entry point with handler dispatch."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    
    # Define subcommands...
    
    handlers = {
        'init': handle_init,
        'add': handle_add,
        'list': handle_list,
        'get': handle_get,
        'delete': handle_delete,
        'generate': handle_generate,
        'help': lambda args: parser.print_help()
    }
    
    handlers[args.command](args)  # Clean dispatch!
```

**Result:** 208 lines of clear, maintainable code.

---

## 📚 Key Takeaways

1. **Architecture Matters**
   - Proper separation of concerns prevents technical debt
   - Clear module boundaries make maintenance easier

2. **Refactoring is Essential**
   - First implementations are rarely optimal
   - Address complexity early before it compounds
   - Code duplication should be treated as a bug

3. **User Experience in CLI Tools**
   - Clear error messages reduce debugging time
   - Interactive prompts improve usability
   - Confirmation dialogs prevent accidental data loss

4. **Security Requires Discipline**
   - Use proven cryptographic libraries—never roll your own
   - Encrypt sensitive data at rest
   - Use cryptographically secure random generators

5. **Documentation is Investment**
   - Establish conventions early to prevent inconsistency
   - Write clear documentation for future maintainers
   - Comments should explain "why", not "what"

6. **Testing Enables Confidence**
   - Tests allow fearless refactoring
   - Testable modules indicate good architecture

---

## 🐛 Notable Issues Resolved

### File Duplication
**Problem:** File grew to 624 lines with code duplicated 2-3 times  
**Solution:** Systematic removal of duplicate blocks, reduced to 208 clean lines  
**Lesson:** Always verify file changes and review diffs carefully

### Complex Main Function
**Problem:** 150-line `main()` function with deeply nested conditionals  
**Solution:** Extracted focused handler functions and helper utilities  
**Lesson:** When a function requires scrolling, it's time to refactor

### Cryptic Error Messages
**Problem:** Wrong password caused unclear "InvalidTag" exception  
**Solution:** Added plaintext detection and clear, actionable error messages  
**Lesson:** Error messages should guide users, not confuse them

---

## 🤝 Contributing

While this is primarily an educational project, contributions that demonstrate additional best practices are welcome:

- Follow the guidelines in [CONVENTIONS.MD](CONVENTIONS.MD)
- Write tests for new features
- Keep commits small and focused
- Document your reasoning in commit messages

---

## 💡 Final Thoughts

This project demonstrates that good software development practices apply to projects of all sizes:
- **Planning** — Established conventions before complexity grew
- **Structure** — Designed modular architecture from the start
- **Refinement** — Refactored code when quality declined
- **Validation** — Tested to ensure reliability
- **Documentation** — Provided clear guidance for future maintainers

**Vault-CLI is more than a password manager—it's a demonstration of professional software development practices applied to a real-world project.**

---

**Repository:** [github.com/7n4xt/Vault-CLI](https://github.com/7n4xt/Vault-CLI)  
**Created:** 2025 | *"Les Bonnes Pratiques de Développeur"*
