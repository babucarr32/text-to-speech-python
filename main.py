import torch
import sys
from TTS.api import TTS
import re

def sanitize_and_prepare_text_for_llm(text: str, min_chars=100, max_chars=300) -> str:
    """
    Sanitizes and prepares text for TTS processing by normalizing punctuation,
    removing invalid characters, and splitting into optimal chunks.
    
    Args:
        text (str): Input text to sanitize
        min_chars (int): Minimum characters per chunk (default: 100)
        max_chars (int): Maximum characters per chunk (default: 300)
    
    Returns:
        str: Sanitized text with newline-separated chunks
    """
    # Step 1: Normalize punctuation and remove bad characters
    replacements = {
        '"': '"',
        ''': "'", ''': "'",
        '—': '-', '–': '-',
        '\u00a0': ' ',  # non-breaking space
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Remove all non-printable or invalid control characters
    text = re.sub(r'[^\x20-\x7E\n\r\t]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Step 2: Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Step 3: Group sentences and append as newline-separated blocks
    lines = []
    current = ""
    for sentence in sentences:
        if not sentence.strip():
            continue
        if len(current) + len(sentence) + 1 <= max_chars:
            current += sentence + " "
        else:
            if len(current.strip()) >= min_chars:
                lines.append(current.strip())
                current = sentence + " "
            else:
                current += sentence + " "
    
    if current.strip():
        lines.append(current.strip())
    
    return "\n".join(lines)

def read_file(file_path: str) -> str:
    """
    Reads content from a text file.
    
    Args:
        file_path (str): Path to the text file
        
    Returns:
        str: Content of the file
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        IOError: If there's an error reading the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except IOError as e:
        raise IOError(f"Error reading file {file_path}: {e}")

def main(file_path: str = None):
    """
    Main function that processes text and generates speech audio.
    
    Args:
        file_path (str, optional): Path to input text file. If None, uses example text.
    """
    # Get device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # Initialize TTS model
    print("Loading TTS model...")
    tts = TTS("tts_models/en/ljspeech/tacotron2-DDC").to(device)
    
    # Determine text source and output filename
    if file_path:
        try:
            text_content = read_file(file_path)
            out_name = file_path.split(".")[0]
            print(f"Processing file: {file_path}")
        except (FileNotFoundError, IOError) as e:
            print(f"Error: {e}")
            print("Using example text instead...")
            file_path = None
    
    if not file_path:
        # Use example text when no file is provided or file reading fails
        text_content = """
        This is a longer English text to demonstrate the text-to-speech capabilities. 
        The system can handle multiple sentences and will generate natural-sounding speech.
        You can use this script to convert any text file to speech, or run it without arguments to hear this example.
        The text processing function will automatically split long texts into optimal chunks for better speech synthesis.
        """
        out_name = "example_output"
        print("Using example text...")
    
    # Process the text
    processed_text = sanitize_and_prepare_text_for_llm(text_content)
    
    if not processed_text:
        print("Error: No content to process")
        return
    
    print(f"Processed text length: {len(processed_text)} characters")
    
    # Generate speech
    output_file = f"{out_name}.wav"
    print("Generating speech audio...")
    tts.tts_to_file(text=processed_text, file_path=output_file)
    print(f"Audio saved to: {output_file}")

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            main(file_path)
        else:
            print("No file provided. Using example text...")
            main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
