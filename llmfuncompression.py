import openai
import json
import os
import time
import argparse

# Set your GPT-4 Mini API key here
openai.api_key = 'your_openai_api_key_here'

def compress_content_with_gpt(content: str) -> str:
    """
    Use GPT-4 Mini to compress the content (either JSON or HTML) by reducing redundancy
    while maintaining structure.
    """
    try:
        # Prepare the prompt to GPT-4 Mini to compress the content
        prompt = f"Compress the following JSON or HTML content while keeping its structure intact:\n\n{content}"

        # Make a request to the GPT-4 Mini API
        response = openai.Completion.create(
            model="gpt-4-mini",  # Use GPT-4 Mini model
            prompt=prompt,
            max_tokens=2048,  # Limit the response length
            temperature=0.5,  # Control randomness, lower is more deterministic
        )
        
        compressed_content = response.choices[0].text.strip()
        return compressed_content

    except Exception as e:
        print(f"Error during compression: {e}")
        return None

def decompress_content_with_gpt(compressed_content: str) -> str:
    """
    Use GPT-4 Mini to decompress the content (either JSON or HTML).
    This assumes that the compressed content is still structured and can be "uncompressed" by GPT-4.
    """
    try:
        # Prepare the prompt to GPT-4 Mini to decompress the content
        prompt = f"Decompress the following JSON or HTML content back to its original structure:\n\n{compressed_content}"

        # Make a request to GPT-4 Mini API
        response = openai.Completion.create(
            model="gpt-4-mini",  # Use GPT-4 Mini model
            prompt=prompt,
            max_tokens=2048,  # Limit the response length
            temperature=0.5,  # Control randomness, lower is more deterministic
        )
        
        decompressed_content = response.choices[0].text.strip()
        return decompressed_content

    except Exception as e:
        print(f"Error during decompression: {e}")
        return None

def read_file(file_path: str) -> str:
    """
    Reads a JSON or HTML file and returns its content as a string.
    """
    with open(file_path, 'r') as file:
        return file.read()

def save_compressed_file(compressed_content: str, output_path: str):
    """
    Saves the compressed content to a new file.
    """
    with open(output_path, 'w') as file:
        file.write(compressed_content)
    print(f"Compressed content saved to: {output_path}")

def save_decompressed_file(decompressed_content: str, output_path: str):
    """
    Saves the decompressed content to a new file.
    """
    with open(output_path, 'w') as file:
        file.write(decompressed_content)
    print(f"Decompressed content saved to: {output_path}")

def compare_content(input_content: str, decompressed_content: str):
    """
    Compares the original content to the decompressed content and prints the differences.
    """
    if input_content == decompressed_content:
        print("Success: The original content and decompressed content match exactly!")
    else:
        print("Mismatch detected between the original and decompressed content.")
        
        # Output the first 500 characters of each to highlight the difference
        print("\nOriginal Input (First 500 characters):")
        print(input_content[:500])  # Show the first 500 characters for comparison

        print("\nDecompressed Output (First 500 characters):")
        print(decompressed_content[:500])  # Show the first 500 characters for comparison
        
        # Optionally, you can show a diff between the two files
        diff = difflib.unified_diff(input_content.splitlines(), decompressed_content.splitlines())
        print("\nDifferences between original and decompressed content:")
        for line in diff:
            print(line)

def main():
    """
    The main function orchestrates the compression or decompression process of JSON or HTML files.
    """
    # Command-line arguments
    parser = argparse.ArgumentParser(description="Compress or Decompress JSON or HTML files using GPT-4 Mini.")
    parser.add_argument('--mode', type=str, required=True, choices=['compress', 'decompress'], 
                        help="Mode to run: either 'compress' or 'decompress'.")
    parser.add_argument('--input_file', type=str, required=True, help="Input JSON or HTML file.")
    parser.add_argument('--output_file', type=str, required=True, help="Output file to save the compressed content.")
    parser.add_argument('--decompressed_file', type=str, required=True, help="Output file to save the decompressed content.")
    args = parser.parse_args()

    # Read the input JSON or HTML file
    text_input = read_file(args.input_file)
    print(f"Loaded {args.input_file} with {len(text_input)} characters.")

    if args.mode == 'compress':
        # Compress the file using GPT-4 Mini
        print(f"Compressing using GPT-4 Mini...")
        compressed_content = compress_content_with_gpt(text_input)
        if compressed_content:
            save_compressed_file(compressed_content, args.output_file)

    elif args.mode == 'decompress':
        # Read the compressed file
        compressed_content = read_file(args.input_file)
        print(f"Loaded compressed file with {len(compressed_content)} characters.")

        # Decompress the file using GPT-4 Mini
        print(f"Decompressing using GPT-4 Mini...")
        decompressed_content = decompress_content_with_gpt(compressed_content)
        if decompressed_content:
            save_decompressed_file(decompressed_content, args.decompressed_file)

        # Automatically compare the decompressed content to the original
        compare_content(text_input, decompressed_content)

    print("Process completed.")

if __name__ == "__main__":
    start_time = time.time()
    main()
