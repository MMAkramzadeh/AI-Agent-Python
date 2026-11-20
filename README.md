# AI Agent

An AI-powered coding agent that can list directories, read files, write files, and execute Python code using function calling with NVIDIA's Nemotron model.

## Features

- **File System Operations**: List directories, read file contents, and write/overwrite files
- **Python Execution**: Run Python scripts with optional arguments and capture stdout/stderr
- **Function Calling**: Built-in tool use with NVIDIA's Nemotron-3.5-Super-VL model via OpenAI-compatible API
- **Verbose Mode**: Detailed logging of tool calls and token usage
- **Secure**: All file paths are restricted to the working directory to prevent unauthorized access

## Project Structure

```
ai-agent/
├── main.py                 # Entry point - AI agent CLI
├── call_function.py        # Function calling dispatcher
├── prompts.py              # System prompt for the AI agent
├── pyproject.toml          # Project configuration and dependencies
├── uv.lock                 # Locked dependency versions
├── .env                    # Environment variables (API keys)
├── .gitignore              # Git ignore rules
├── .python-version         # Python version specification
├── functions/              # Core function implementations
│   ├── get_files_info.py   # List directory contents
│   ├── get_file_content.py # Read file contents
│   ├── write_file.py       # Write/overwrite files
│   └── run_python_file.py  # Execute Python scripts
├── calculator/             # Example submodule
│   ├── explore.py          # Directory tree scanner
│   ├── test.txt            # Test file
│   └── README.md           # Calculator module documentation
└── tests/                  # Test files
    ├── test_get_files_info.py
    ├── test_get_file_content.py
    ├── test_write_file.py
    └── test_run_python_file.py
```

## Installation

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)
- NVIDIA API key

### Setup

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd ai-agent
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Create a `.env` file with your NVIDIA API key:
   ```bash
   echo 'NVIDIA_API_KEY="your-api-key-here"' > .env
   ```

## Usage

Run the AI agent with a prompt:

```bash
uv run main.py "Your prompt here"
```

Enable verbose mode to see tool calls and token usage:

```bash
uv run main.py "Your prompt here" --verbose
```

### Example

```bash
uv run main.py "List all files in the current directory"
uv run main.py "Read the contents of main.py" --verbose
uv run main.py "Write a hello world script to hello.py"
uv run main.py "Run the calculator explore script"
```

## Available Tools

The agent has access to the following functions:

| Function | Description |
|----------|-------------|
| `get_files_info` | List files and directories with sizes and types |
| `get_file_content` | Read the contents of a file |
| `write_file` | Write or overwrite a file |
| `run_python_file` | Execute a Python script with arguments |

## Configuration

### pyproject.toml

```toml
[project]
name = "ai-agent"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    "openai===2.44.0",
    "python-dotenv==1.1.0",
]
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NVIDIA_API_KEY` | API key for NVIDIA's model endpoints | Yes |

## Security

- All file operations are restricted to the working directory
- Path traversal attacks are prevented via `os.path.commonpath` validation
- The `.env` file containing API keys is gitignored
- `__pycache__`, `.venv`, and build artifacts are gitignored

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

This project is part of the AI Agent workspace.

## Acknowledgments

- Powered by [NVIDIA Nemotron-3.5-Super-VL-120B-A12B](https://build.nvidia.com/)
- Built with [OpenAI Python SDK](https://github.com/openai/openai-python)
- Package management with [uv](https://github.com/astral-sh/uv)