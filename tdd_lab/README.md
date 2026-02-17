# 🧪 Test-Driven Development (TDD) Lab

## 📌 Overview
This lab focuses on **Test-Driven Development (TDD)**—writing test cases first and then implementing the required functionality. Each student will contribute **one test case** and submit a pull request.

---

## 📂 Project Structure

The repository is organized as follows:

```markdown
tdd_lab/
├── 📂 tests/                   # Contains all test cases
│   ├── 📄 test_counter.py       # Test cases for the counter API (each student contributes a test)
├── 📂 src/                      # Source code for the counter service
│   ├── 📄 __init__.py           # Flask app initialization
│   ├── 📄 counter.py            # Counter API implementation
│   ├── 📄 status.py             # HTTP status codes
├── 📄 requirements.txt          # Dependencies for the project
├── 📄 pytest.ini                # Pytest configuration
├── 📄 README.md                 # Project documentation
```

### Python Version(s)
To follow this lab, you need Python **version 3.8 or later**. The exercises have been tested with the following versions: `3.8.1`, `3.9.5`, `3.9.6`, `3.9.7`, and `3.10.10`. However, any Python version **3.8+** should work without configuration issues.  

If you encounter any setup or configuration problems, please reach out to the **T.A.** for assistance.


### 1. Upgrading PIP:
Sometimes it is useful to upgrade `pip` before installing dependencies. If you like, run: `pip install --upgrade pip` and later install the dependencies using: `pip install -r requirements.txt`

### 2. Create a Virtual Environment (Highly Recommended)
 - It is a good practice to configure python virtual environment. Use the commands below to setup python virtual environment on `Linux/MacOS` or `Windows OS`
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```
 ### 3. Install Dependencies  
```bash
pip install -r requirements.txt
```

### 4. Set Flask Environment Variable
- macOS/Linux
```bash
   export FLASK_APP=src
```
- Windows
```bash
    set FLASK_APP=src
```
### 5. Run Flask Locally to Ensure API Works
```bash
flask run
```

✅ Visit http://127.0.0.1:5000/counters/foo in the browser. If it returns {"error": "Counter not found"}, your API is working!

### 6. Merge Conflicts
If you are having trouble merging changes to the main branch of the team's repo, you can take a look at this doc: [How to Handle Merge Conflicts in the Testing Lab](doc/mergeconflicts.md).


### 7. 🛠️ Troubleshooting Guide

Below are common errors students may encounter and their solutions:

| **Error** | **Cause** | **Solution** |
|-----------|----------|-------------|
| `ImportError: cannot import name 'app' from 'src'` | Flask app is not detected | Run `export FLASK_APP=src` before running `flask run` |
| `Error: No such command 'db'` | Flask-Migrate missing | Run `pip install flask-migrate` |
| `sqlalchemy.exc.OperationalError: table account has no column named balance` | Database not migrated | Run `flask db upgrade` |
| `ModuleNotFoundError: No module named 'src'` | Missing dependencies | Run `pip install -r requirements.txt` |

If you continue to experience issues, follow these steps:
1. **Check that Flask is running** with `flask run`.
2. **Ensure all dependencies are installed** with `pip install -r requirements.txt`.
3. **Consult your team first before reaching out for help**.
4. **If the issue persists, open a GitHub Issue in your team repository**, including:
   - A clear description of the problem.
   - The exact error message.
   - Steps you have already tried.

🚀 **Debug first, then ask for help!**


