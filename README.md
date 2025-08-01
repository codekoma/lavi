# BigCodeBench Data Collection Repository

**Please take the time to read through all of the instructions provided below. Review often as needed.**

## Table of Contents

- [Project Overview](#project-overview)
- [Payment Information](#payment-information)
- [Setup & Installation](#setup--installation)
- [Quick Start - Create a New Problem](#quick-start---create-a-new-problem)
- [Directory Structure](#directory-structure)
- [File Requirements](#file-requirements)
- [File Format Examples](#file-format-examples)
- [Examples](#examples)
- [Submission Guidelines](#submission-guidelines)
- [PR Workflow](#pr-workflow)
- [Development Setup](#development-setup)
- [Validation Details](#validation-details)


## Project Overview

BigCodeBench wants to challenge the model on more real-world, practical coding tasks. These tasks are different from the typical LeetCode-style, or algorithmically heavy coding benchmark prompts you may be more used to seeing in similar projects. Here, specifically we’re more interested in three things:

- **Compositional reasoning** - How well does the model implement solutions involving multiple steps that depend on each other? Usually this involves breaking down a problem into sub-problems, or “thinking in parts” the way a real developer would when solving a nontrivial problem.
- **Complex instructions** - Can the model still write an effective solution when it is given several instructions and constraints?
- **Effective library use** - Can the model combine the use of different APIs or libraries functionalities together?

BigCodeBench has **two prompt variants that need to be performed in the task**: `Instruct` and `Complete`.

| Prompt Type  | Input (What you send the model)            | Output (What the model should respond with) |
| ------------ | ------------------------------------------ | ------------------------------------------- |
| **Instruct** | Natural language prompt + method signature | Correct function implementation             |
| **Complete** | Formal docstring with function signature   | Correct function implementation             |

While the input differs, both variants should be treated similarly when designing the core problem.

All submission code **must be in Python**. You may only use the following libraries in addition to Python’s standard library.

**For BigCodeBench-Hard**, you must use **at least 3 libraries**, and at least **2 must be non-standard** taken from this list:

| Domain            | Allowed Libraries                                                                                                                          |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **Computation**   | `pandas`, `numpy`, `sklearn`, `scipy`, `math`, `nltk`, `statistics`, `cv2`, `statsmodels`, `tensorflow`, `sympy`, `textblob`, `skimage`    |
| **General**       | `random`, `re`, `collections`, `itertools`, `string`, `operator`, `heapq`, `ast`, `functools`, `regex`, `bisect`, `inspect`, `unicodedata` |
| **Visualization** | `matplotlib`, `seaborn`, `PIL`, `folium`, `wordcloud`, `turtle`, `mpl_toolkits`                                                            |
| **System**        | `os`, `json`, `csv`, `shutil`, `glob`, `subprocess`, `pathlib`, `sqlite3`, `io`, `zipfile`, `sys`, `logging`, `pickle`, `struct`, `psutil` |
| **Time**          | `datetime`, `time`, `pytz`, `dateutil`, `holidays`, `calendar`                                                                             |
| **Network**       | `requests`, `urllib`, `bs4`, `socket`, `django`, `flask`, `ipaddress`, `smtplib`, `http`, `email`, `cgi`, `ssl`, `imaplib`, `mechanize`    |
| **Cryptography**  | `hashlib`, `base64`, `binascii`, `codecs`, `rsa`, `cryptography`, `hmac`, `blake3`, `secrets`, `Crypto`                                    |



### Install uv (Python Package Manager)

[uv](https://github.com/astral-sh/uv) is a fast Python package manager that replaces pip and virtualenv. It's required to manage dependencies and run scripts in this project.

**For Mac:**
Use curl to download the script and execute it with sh:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

If your system doesn't have curl, you can use wget:
```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

Request a specific version by including it in the URL:
```bash
curl -LsSf https://astral.sh/uv/0.7.21/install.sh | sh
```

**For Windows:**
Use irm to download the script and execute it with iex:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Changing the execution policy allows running a script from the internet.

Request a specific version by including it in the URL:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/0.7.21/install.ps1 | iex"
```

### Install Dependencies
```bash
uv sync
uv run python setup_precommit.py
```

### Pre-commit Hooks
The setup automatically configures hooks that will:
- Validate submission structure
- Check file formats
- Run basic syntax checks
- Enforce coding standards

Run validation manually:
```bash
uv run python -m scripts.validation.validate_submission
```

## 🚀 Quick Start - Create a New Problem
```
# Create a new problem
uv run python -m scripts.cli.create_problem --problem-name two-sum
uv run python -m scripts.cli.create_problem --problem-name graph-algorithms

# Interactive mode
uv run python -m scripts.cli.create_problem
```

The script will:
- Get your git username automatically
- Create all required files with proper templates
- Generate the correct directory structure with today's date
- Set up templates for both prompt formats

## 📁 Directory Structure

Each problem follows this exact format:

```
problems/{YYYY-MM-DD-username-problem-name}/
├── metadata.json           # Problem metadata and configuration
├── complete_prompt.py     # PEP257 docstring format prompt
├── instruct_prompt.md     # Instruction format prompt  
├── src/
│   └── main.py            # Python solution implementation
├── test.py                # unittest-based test suite
```

## 📋 File Requirements

### `metadata.json` - Problem Configuration
**Purpose**: Central configuration file containing all problem metadata and specifications.

**Required Structure**:
```json
{
    "name": "problem-name",
    "entry_point": "task_func", 
    "doc_struct": {
        "description": ["Multi-line description", "of the problem"],
        "notes": [],
        "params": [],
        "returns": ["return_type: Description of return value"],
        "reqs": ["required", "modules"],
        "raises": [],
        "examples": [">>> example_usage()", "expected_output"]
    },
    "dependencies": {
        "package_name": ">=version"
    }
}
```

**Field Descriptions**:

| Field | Purpose |
|-------|---------|
| `name` | Short kebab-case problem identifier |
| `entry_point` | Must be `"task_func"` - the function name to implement |
| `description` | A list of lines forming the natural-language description of the task. This is shown to the model to explain what it should implement. |
| `notes` | Any additional clarifications or caveats; typically empty unless there's special behavior to call out. |
| `params` | Descriptions of each function parameter, including types. Used to build the prompt so the model knows what inputs to expect. |
| `returns` | A description of what the function should return, including types. Used to clarify expected outputs. |
| `reqs` | A list of Python modules or libraries the solution is allowed (or expected) to import and use. |
| `raises` | Exceptions that the implementation should raise under certain conditions. |
| `examples` | Interactive Python examples (the ">>>" style), which get embedded in the prompt as hints for the model. |
| `dependencies` | Python packages with version constraints (if any) required for testing |

### `complete_prompt.py`
**Purpose**: Function signature with complete docstring but no implementation.

**Requirements**:
- Must include all necessary import statements
- Function signature must match `entry_point` in metadata.json
- Docstrings should have inputs and outputs clearly defined.
- No implementation - docstring only

### `instruct_prompt.md` - Instruction Format
**Purpose**: Brief markdown instruction format for the problem.

**Requirements**:
- Clear output specification using "The function should output with:"
- Code block showing required imports and function signature (MUST HAVE)

### `src/main.py` - Reference Solution  
**Purpose**: Complete working implementation of the problem.

**Requirements**:
- Identical docstring to `complete_prompt.py`
- Must be the complete, correct implementation
- Must be **self-contained**. We don't need to include any additional assets or temporary files that may be created or interacted with in the solution during runtime. In order to run the unit tests successfully, you should include the necessary mocks for the unit tests to use.
- Must pass all tests in `test.py`

### `test.py` - Comprehensive Test Suite
**Purpose**: unittest-based test suite covering all functionality and edge cases.

**Requirements**:
- Must use `unittest.TestCase`
- Import from `src.main import task_func`
- Must have **at least** 5 unit test assertions.
- Cover normal functionality, edge cases, and error conditions  
- Test different input types and ranges
- Use descriptive test method names (good practice)
- Must include assertions for both return type and value correctness
- Mock external dependencies where needed. Mocking is a likely necessity for most tasks to some extent. Use mocks to replace or isolate any external functionality. This might include:
    - File I/O
    - network calls and api responses
    - time or random based functions (or use a seed)
- Aim for high test coverage of the implementation

## 📝 File Format Examples

### Unit Test Template

```python
import unittest
from unittest.mock import patch, Mock, MagicMock
# Add additional imports as needed

class TestCases(unittest.TestCase):
    def setUp(self):
        # Setup code
        pass

    def test_normal_operation(self):
        """Test normal operation with valid inputs"""
        # Test code

    @patch('module_name.external_resource')
    def test_involving_mocks(self):
        """Test behavior involving external resources using mocks"""
        # Test code

    def test_edge_case_1(self):
        """Test a specific edge case from the spec"""
        # Test code

    def test_error_condition_1(self):
        """Test a specific error condition from the spec"""
        # Test code

    # Additional tests...

    def tearDown(self):
        # Cleanup code
        pass
```

### Complete Prompt Template

The **Complete** variant uses a structured docstring and function stub. It includes:

- All necessary `import` statements
- Named parameters only (no `*args`, `**kwargs`, or unnamed parameters). 
- Rich, detailed docstring

Prompt Template:

Write a self-contained solution in Python within {function_name}.
```python
# [import statements]
def function_name(*, param1: type, param2: type, ...) -> return_type:
    """
    [Brief one-line description]

    [Comprehensive explanation of the real-world task, detailing what the function does and how it transforms input.]

    The function handles the following edge cases:
    - [Edge case 1 and handling]
    - [Edge case 2 and handling]

    Args:
        param1 (type): Description with constraints, valid ranges, expected format, and validation.
        param2 (type): Description with constraints, valid ranges, expected format, and validation.
        ...

    Returns:
        return_type: Format and constraints of the returned value.

    Raises:
        ExceptionType: When [condition].
        ExceptionType: When [condition].

    Examples:
        >>> function_name(example_input1, example_input2)
        expected_output

        >>> function_name(edge_case_input)
        edge_case_output

    Notes:
        - [Any extra implementation notes]
        - [Performance considerations if relevant]
    """
    pass
```

### Instruct Prompt template

There is no template for the Instruct variant. The goal is to write a more **natural language prompt version of the Complete prompt** you've already written. Importantly, the Instruct prompt should be **written in simple plain text with minimal to no structure**. Things like markdown blocks or bullet points should be minimal or nonexistent. The hardest part about this is figuring out how to write a more natural sounding prompt that still captures all of the specifications for behavior and functionality of the Complete prompt. The Instruct prompt should still provide just enough clarity that the model can be fairly expected to produce a code solution that passes all of the same unit tests cases correctly. You may want to add contextual backstory to help make the prompt sound like a real user request, but this addition is optional. Importantly, the same inputs and outputs need to be clear. Any exceptions that are raised under certain circumstances still need to be made clear too. Furthermore, the Instruct prompt should end with a code snippet containing the needed imports, and method signature, but not the docstring.

For Example such a code snippet might look like this:

```
import matplotlib.pyplot as plt
import pandas as pd
import random
from datetime import datetime

def task_func(seed=42):
```

## Examples

### metadata.json
```json
{
    "name": "permutations-sum",
    "entry_point": "task_func",
    "doc_struct": {
        "description": [
            "Calculates the average of the sums of absolute differences between each pair of consecutive numbers",
            "for all permutations of a given list. Each permutation is shuffled before calculating the differences.",
            "Args:",
            "- numbers (list): A list of numbers. Default is numbers from 1 to 10."
        ],
        "notes": [],
        "params": [],
        "returns": [
            "float: The average of the sums of absolute differences for each shuffled permutation of the list."
        ],
        "reqs": [
            "itertools",
            "random.shuffle"
        ],
        "raises": [],
        "examples": [
            ">>> result = task_func([1, 2, 3])",
            ">>> isinstance(result, float)",
            "True"
        ]
    },
    "dependencies": {
        "numpy": ">=1.26.0"
    }
}
```

### complete_prompt.py
```python
import itertools
from random import shuffle

def task_func(numbers=list(range(1, 3))):
    """
    Calculates the average of the sums of absolute differences between each pair of consecutive numbers
    for all permutations of a given list. Each permutation is shuffled before calculating the differences.

    Args:
    - numbers (list): A list of numbers. Default is numbers from 1 to 10.

    Returns:
    float: The average of the sums of absolute differences for each shuffled permutation of the list.

    Requirements:
    - itertools
    - random.shuffle

    Example:
    >>> result = task_func([1, 2, 3])
    >>> isinstance(result, float)
    True
    """
```

### instruct_prompt.md
```markdown
I need a function that analyzes all possible arrangements of a list of numbers in a specific way. For each arrangement of the numbers, I want to randomly shuffle that arrangement and then calculate the sum of absolute differences between consecutive numbers in the shuffled sequence. After doing this for every possible arrangement, I need the average of all those sums. The function should take a list of numbers as input, with a default of numbers from 1 to 3, and return the average as a float.

```
import itertools
from random import shuffle
def task_func(numbers=list(range(1, 3))):
```
```

### src/main.py
```python
import itertools
from random import shuffle

def task_func(numbers=list(range(1, 3))):
    """
    Calculates the average of the sums of absolute differences between each pair of consecutive numbers
    for all permutations of a given list. Each permutation is shuffled before calculating the differences.

    Args:
    - numbers (list): A list of numbers. Default is numbers from 1 to 10.

    Returns:
    float: The average of the sums of absolute differences for each shuffled permutation of the list.

    Requirements:
    - itertools
    - random.shuffle

    Example:
    >>> result = task_func([1, 2, 3])
    >>> isinstance(result, float)
    True
    """
    permutations = list(itertools.permutations(numbers))
    sum_diffs = 0

    for perm in permutations:
        perm = list(perm)
        shuffle(perm)
        diffs = [abs(perm[i] - perm[i+1]) for i in range(len(perm)-1)]
        sum_diffs += sum(diffs)

        avg_sum_diffs = sum_diffs / len(permutations)

    return avg_sum_diffs
```

### test.py
```python
import unittest
from unittest.mock import patch
from random import seed, shuffle
from src.main import task_func
import itertools


class TestCases(unittest.TestCase):
    
    def test_default_numbers(self):
        # Test with default number range to check that the result is a positive float.
        result = task_func()
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)
    
    def test_custom_list(self):
        # Test with a custom list of small positive integers.
        result = task_func([1, 2, 3])
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)
    
    def test_negative_numbers(self):
        # Test with negative numbers to verify proper handling.
        result = task_func([-3, -2, -1])
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)
    
    def test_single_element(self):
        # Test with a single element list - should return zero.
        result = task_func([5])
        self.assertIsInstance(result, float)
        self.assertEqual(result, 0)
    
    def test_empty_list(self):
        # Test with an empty list.
        result = task_func([])
        self.assertIsInstance(result, float)
        self.assertEqual(result, 0)
        
    def test_identical_elements(self):
        # Test with identical elements - differences should be zero.
        result = task_func([2, 2, 2])
        self.assertIsInstance(result, float)
        self.assertEqual(result, 0)
    
    def test_mixed_numbers(self):
        # Test with mixed positive and negative numbers.
        result = task_func([-10, 10, -5])
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)
```


## 📝 Submission Guidelines

### 1. One Problem Per PR
Each pull request must contain exactly **one problem submission**. This ensures:
- Easier code review and validation
- Better tracking and labeling
- Simpler merge and rollback processes
- Automated difficulty and subtask labeling

### 2. Ownership Rules
- You can only modify problems with your username in the directory name
- The validation system enforces this automatically
- Create separate PRs for different problems

### 3. File Naming
- Directory: `{YYYY-MM-DD-username-problem-name}`
- Use hyphens for spaces in problem names
- Username will be automatically detected from git config

## 🔄 PR Workflow

Watch this video walkthrough of the complete PR submission process:

[![PR Workflow Video](https://img.shields.io/badge/▶️_Watch_Video-Loom-00D4AA?style=for-the-badge&logo=loom&logoColor=white)](https://www.loom.com/share/feceee0bd71745ec9d755c9b58533431)

> 🎥 **Click the badge above to watch the complete PR workflow tutorial**

## 🛠️ Development Setup

This section assumes you've completed the [Setup & Installation](#setup--installation) steps above.

For additional development tools and advanced configuration, refer to the individual script documentation in the `scripts/` directory.

## 🔍 Validation Details

The validation system checks:

### Structure Validation
- ✅ Correct directory naming format
- ✅ All required files present
- ✅ Proper file extensions and naming
- ✅ No extra or missing files

### Content Validation
- ✅ PEP257 docstring format in `complete_prompt.py`
- ✅ Instruction format in `instruct_prompt.md`
- ✅ Valid JSON in `metadata.json`
- ✅ unittest structure in `test.py`
- ✅ Function named `task_func` in `src/main.py`

### Test Validation
- ✅ Tests use unittest framework
- ✅ At least 3 test methods
- ✅ Tests import and use the solution
- ✅ Tests run successfully

---

Ready to contribute? Start by creating your first problem:

```bash
uv run python -m scripts.cli.create_problem --problem-name your-problem-name
```
