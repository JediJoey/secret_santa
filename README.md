# Secret Santa Generator

This script randomly assigns people who they should buy a gift for, adhering to specific incompatibility rules defined in a YAML file.

It also ensures all participants give a gift, all participants receive a gift, and prevents self-gifting.

## Prerequisites

*   **Python 3.x:** Ensure Python is installed on your system.
*   **Dependencies:** The required libraries are listed in `requirements.txt`.

You can install the necessary dependencies using pip:

```bash
pip install -r requirements.txt
```

## Files Needed
`christmas.py`: The main Python script that handles the logic.

`people.yaml`: A YAML file you must create to list the participants and their rules.

`requirements.txt`: A file listing the Python dependencies (PyYAML).

### Example people.yaml structure
```yaml
- name: Alice
  incompatibles:
    - Bob
    - Charlie
- name: Bob
  incompatibles:
    - Alice
- name: Charlie
  incompatibles:
    - Alice
    - David
- name: David
  incompatibles: []
```

`name`: The name of the participant (must be unique).

`incompatibles`: A list of names this person cannot buy a gift for (e.g., family members, themselves).
## How to Run the Script

Run from your terminal:
```bash
python christmas.py
```

## Script Output
The script executes the assignment process 10 times successfully and compiles all results into a new file named `secret_santa_results.txt` in your current directory.
### Example secret_santa_results.txt content
```
--- Secret Santa Results Log ---

--- Entry 1 ---
Alice is buying a gift for -> David
Bob is buying a gift for -> Charlie
Charlie is buying a gift for -> Bob
David is buying a gift for -> Alice

--- Entry 2 ---
... (9 more entries follow) ...

--- End of 10 Successful Assignments ---
```

## Troubleshooting
`File Not Found Error`: people.yaml: Make sure your YAML file is in the same directory as christmas.py and spelled correctly.
`ModuleNotFoundError`: No module named 'yaml': You need to install the dependencies using pip install -r requirements.txt.
`"Failed to find a valid assignment..."`: If your incompatibility rules are too restrictive (e.g., only two people who are incompatible with each other), a solution might be mathematically impossible. Relax some rules in your people.yaml file.
