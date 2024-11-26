# weight_score_calculator_demo

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for Python package management.

### Prerequisites

1. Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd weight_score_calculator_demo
```

2. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
```

3. Install dependencies:
```bash
uv pip install -e .
```

### Running the Application

Start the Streamlit app:
```bash
streamlit run app.py
```

## Development

To add new dependencies:
```bash
uv pip install <package-name>
```

To update dependencies:
```bash
uv pip sync
```

To export dependencies (if needed):
```bash
uv pip freeze > requirements.txt
```

### Locking Dependencies

To lock dependencies declared in a `pyproject.toml`:
```bash
uv pip compile pyproject.toml -o requirements.txt
```

This README now includes:
- Installation instructions for uv
- Steps to set up a virtual environment
- Commands for managing dependencies
- Basic usage instructions
- Common development commands
- Command to lock dependencies declared in a `pyproject.toml`

Feel free to adjust the content based on your specific project needs!