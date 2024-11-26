import os
import re

def extract_links_from_file(file_path):
    """Extracts URLs from a single file."""
    url_pattern = r'https?://[^\s"]+'
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
        return re.findall(url_pattern, content)

def extract_links_from_folder(root_folder, output_file_path):
    """Recursively scans a folder for files and extracts URLs."""
    all_urls = []
    
    # Walk through the directory and its subdirectories
    for root, _, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Extract URLs from the current file
                urls = extract_links_from_file(file_path)
                all_urls.extend(urls)
                print(f"Extracted {len(urls)} URLs from {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    # Write all extracted URLs to the output file
    with open(output_file_path, 'w') as output_file:
        output_file.write("\n".join(all_urls))
    
    print(f"Extracted a total of {len(all_urls)} URLs to {output_file_path}")

# Main function to prompt user input
if __name__ == "__main__":
    # Ask the user for the root folder path
    root_folder = input("Enter the root folder path to scan for log files: ").strip()
    if not os.path.isdir(root_folder):
        print(f"The path '{root_folder}' is not a valid directory. Please try again.")
    else:
        # Ask the user for the output file path
        output_file_path = input("Enter the output file path to save the extracted links: ").strip()
        extract_links_from_folder(root_folder, output_file_path)
