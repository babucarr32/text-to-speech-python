# Text-to-Speech (TTS) Script Documentation

## Overview

This Python script converts text files to speech audio using the Coqui TTS library. It includes advanced text preprocessing to optimize the input for natural-sounding speech synthesis.

## Features

- **Flexible Input**: Works with text files or uses built-in example text
- **Smart Text Processing**: Sanitizes and chunks text for optimal TTS performance
- **GPU Support**: Automatically detects and uses CUDA if available
- **Error Handling**: Graceful fallback to example text if file reading fails
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Requirements

### Dependencies

```bash
# Using uv (recommended):
uv add torch TTS

# Or with pip:
pip install torch TTS
```

### System Requirements

- Python 3.8+
- PyTorch
- Coqui TTS library
- Optional: CUDA-compatible GPU for faster processing

## Installation

1. Initialize a new uv project (if starting fresh):
   ```bash
   uv init tts-project
   cd tts-project
   ```

2. Add dependencies:
   ```bash
   uv add torch TTS
   ```

3. Add the script to your project and run:
   ```bash
   uv run main.py [optional-text-file]
   ```

## Usage

### Basic Usage

```bash
# Use example text (no arguments)
uv run main.py

# Convert a text file to speech
uv run main.py document.txt

# Alternative Python execution (if uv isn't available)
python main.py document.txt
```

### Command Line Arguments

- **No arguments**: Uses built-in example text
- **`<file-path>`**: Path to a text file to convert to speech

### Examples

```bash
# Convert a story to audio
uv run main.py story.txt

# Convert a document
uv run main.py README.md

# Convert a book chapter
uv run main.py "chapter1.txt"

# Use example text for testing
uv run main.py
```

### Project Structure with uv

```
tts-project/
├── pyproject.toml      # uv project configuration
├── main.py            # TTS script
├── documents/         # Your text files
│   ├── story.txt
│   └── article.md
└── audio_output/      # Generated audio files
    ├── story.wav
    └── article.wav
```

## Functions

### `sanitize_and_prepare_text_for_llm(text, min_chars=100, max_chars=300)`

Preprocesses text for optimal TTS synthesis.

**Parameters:**
- `text` (str): Input text to process
- `min_chars` (int): Minimum characters per text chunk (default: 100)
- `max_chars` (int): Maximum characters per text chunk (default: 300)

**Returns:**
- `str`: Processed text with newline-separated chunks

**Features:**
- Normalizes Unicode punctuation marks
- Removes non-printable characters
- Splits text into sentence-based chunks
- Optimizes chunk sizes for TTS processing

### `read_file(file_path)`

Safely reads content from a text file.

**Parameters:**
- `file_path` (str): Path to the text file

**Returns:**
- `str`: File content

**Raises:**
- `FileNotFoundError`: If the file doesn't exist
- `IOError`: If there's an error reading the file

### `main(file_path=None)`

Main processing function that orchestrates text-to-speech conversion.

**Parameters:**
- `file_path` (str, optional): Path to input file. Uses example text if None.

**Process:**
1. Detects available compute device (CUDA/CPU)
2. Loads TTS model
3. Reads input text or uses example
4. Processes text for optimal synthesis
5. Generates speech audio file

## Text Processing Details

The script includes sophisticated text preprocessing:

### Character Normalization
- Converts curly quotes to straight quotes
- Normalizes em-dashes and en-dashes
- Removes non-breaking spaces
- Filters out non-printable characters

### Sentence Chunking
- Splits text at sentence boundaries
- Groups sentences into optimal-sized chunks
- Ensures chunks meet minimum/maximum length requirements
- Preserves sentence integrity

### Output Format
- Chunks separated by newlines
- Optimized for natural speech rhythm
- Maintains readability and flow

## Output Files

The script generates WAV audio files with names based on the input:

- **Input file**: `document.txt` → Output: `document.wav`
- **Example text**: → Output: `example_output.wav`

## TTS Model

The script uses the **Tacotron2-DDC** model with LJSpeech dataset:
- High-quality English speech synthesis
- Female voice characteristics
- Good for general-purpose text conversion
- Relatively fast inference

## Error Handling

The script includes comprehensive error handling:

- **File not found**: Falls back to example text
- **Read errors**: Graceful degradation with user notification
- **Empty content**: Validates processed text before synthesis
- **Keyboard interrupt**: Clean exit on Ctrl+C
- **General exceptions**: Catches and reports unexpected errors

## Performance Considerations

### GPU Acceleration
- Automatically detects CUDA availability
- Significantly faster processing on compatible GPUs
- Falls back to CPU if GPU unavailable

### Memory Usage
- Text chunking reduces memory requirements
- Model loaded once per session
- Efficient processing of large documents

### Processing Speed
- Typical processing: ~1-5 seconds per sentence
- GPU can provide 2-10x speed improvement
- File I/O is minimal overhead

## Customization Options

### Model Selection
Replace the model string to use different voices:
```python
# Other available models
tts = TTS("tts_models/en/ljspeech/glow-tts")
tts = TTS("tts_models/en/ljspeech/speedy-speech")
```

### Chunk Size Tuning
Adjust text processing parameters:
```python
# Larger chunks for faster processing
processed_text = sanitize_and_prepare_text_for_llm(text, min_chars=200, max_chars=500)

# Smaller chunks for better pronunciation
processed_text = sanitize_and_prepare_text_for_llm(text, min_chars=50, max_chars=150)
```

### Output Format
Modify the output file format:
```python
# Different audio formats (if supported)
tts.tts_to_file(text=processed_text, file_path=f"{out_name}.mp3")
```

## Troubleshooting

### Common Issues

**ImportError: No module named 'TTS'**
```bash
uv add TTS
```

**uv: command not found**
```bash
# Install uv first
curl -LsSf https://astral.sh/uv/install.sh | sh
# Or with pip
pip install uv
```

**CUDA out of memory**
- Reduce text chunk sizes
- Use CPU instead: Set `device = "cpu"`

**Poor audio quality**
- Check input text encoding (use UTF-8)
- Ensure proper punctuation in source text
- Try different TTS models

**File encoding errors**
- Ensure text files are UTF-8 encoded
- Remove special characters if necessary

### uv-Specific Issues

**Dependency conflicts**
```bash
# Force reinstall dependencies
uv sync --refresh
```

**Python version issues**
```bash
# Specify Python version
uv python install 3.11
uv run --python 3.11 main.py
```

**Virtual environment issues**
```bash
# Reset the project environment
uv venv --seed
uv sync
```

### Performance Issues

**Slow processing**
- Install CUDA-compatible PyTorch: `uv add torch --index-url https://download.pytorch.org/whl/cu118`
- Verify GPU is being used (check console output)
- Reduce text chunk sizes for memory-constrained systems

**uv taking long to resolve dependencies**
- Use `uv add --no-deps` for faster installation if dependencies are already satisfied
- Clear uv cache: `uv cache clean`

## License and Attribution

This script uses the Coqui TTS library, which may have its own licensing requirements. Check the [Coqui TTS repository](https://github.com/coqui-ai/TTS) for license details.

## Contributing

To contribute improvements:
1. Test with various text types and lengths
2. Ensure cross-platform compatibility
3. Add error handling for edge cases
4. Document any new features or parameters
