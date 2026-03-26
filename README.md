# Folder Scanner using Local AI

A simple Python tool that scans folders and uses a local AI model to analyze, organize, or process files automatically.

## Features

- Recursive folder scanning
- Local AI processing (no external APIs required)
- Customizable file handling
- Lightweight and easy to use

## Requirements

- Python 3.12
- pip

## Installation

```bash
git clone https://github.com/tariqsenosy/folder-scanner-using-local-ai.git
cd folder-scanner-using-local-ai
```

## Usage

```bash
python main.py --path /path/to/folder
```

### Example

```bash
python main.py --path ./documents
```

## Configuration

You can customize:

- Target folder path
- Included/excluded file types
- Local AI model settings

## Project Structure

```
.
├── main.py
├── scanner.py
├── filter.py
├── sendr.py
└── README.md
```

## Notes

- Ensure your local AI model is installed and running (e.g., Ollama).
- Performance depends on your machine resources.

## Future Improvements

- Add GUI
- Support more file types
- Enhance AI processing

## License

MIT License
