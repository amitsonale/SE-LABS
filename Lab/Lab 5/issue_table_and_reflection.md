# Lab 5: Static Code Analysis

## 1. Issue Documentation

| Issue                          | Type               | Original Code / Finding                                    | Fix Applied                                                               |
| ------------------------------ | ------------------ | ---------------------------------------------------------- | ------------------------------------------------------------------------- |
| Mutable default argument       | Code quality / Bug | `attendance_log=[]` in function parameters                 | Used a module-level attendance log instead of a mutable default argument  |
| Bare exception                 | Code quality       | `except:`                                                  | Caught specific exceptions: `KeyError` and `ValueError`                   |
| Shell command injection risk   | Security           | `os.system()` used to delete files                         | Used `pathlib.Path.glob()` and `Path.unlink()` instead of a shell command |
| File handling                  | Code quality       | File opened without a context manager or explicit encoding | Used `with open(..., encoding="utf-8")`                                   |
| Incorrect class capacity check | Logic / Bug        | Used `>` when checking class capacity                      | Used `>=` to prevent bookings beyond capacity                             |
| Naming convention              | Style              | `addMembers()`                                             | Renamed the function to `add_members()`                                   |
| Missing documentation          | Code quality       | Functions lacked docstrings                                | Added module and function docstrings                                      |
| Formatting                     | Style              | Missing blank lines and other PEP 8 violations             | Corrected formatting and blank lines                                      |

## 2. Reflection

### Q1. What is static code analysis?

Static code analysis examines source code without executing it to identify potential bugs, security vulnerabilities, and coding-style violations.

### Q2. What is the purpose of Pylint, Bandit, and Flake8?

- **Pylint:** Checks code quality, naming conventions, documentation, and potential programming problems.
- **Bandit:** Identifies common security vulnerabilities in Python code.
- **Flake8:** Checks Python formatting and compliance with style guidelines.

### Q3. What did you learn from this lab?

I learned how to use static analysis tools to identify and correct code-quality, security, and formatting problems. I also learned the importance of avoiding mutable default arguments, handling exceptions appropriately, and avoiding unsafe shell commands.

### Q4. How does static analysis improve software quality?

Static analysis helps identify potential problems early, improves code readability and maintainability, and reduces the likelihood of bugs and security vulnerabilities.

### Q5. Why should static analysis be used along with program testing?

Static analysis can detect many issues without executing a program, while testing checks the program's actual behaviour. Using both provides better confidence in code quality and correctness.
