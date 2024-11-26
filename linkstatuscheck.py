import requests
from collections import defaultdict
from urllib.parse import urlparse
import os
import time

def is_valid_url(url):
    """Check if the URL is valid and well-formed."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def categorize_links(input_file_path):
    """Reads links from a file, checks their HTTP status, and categorizes them."""
    status_categories = defaultdict(list)
    invalid_links = []

    # Read the input file containing URLs
    with open(input_file_path, 'r') as input_file:
        links = [line.strip() for line in input_file if line.strip()]
    
    print(f"Checking {len(links)} links...")

    for link in links:
        if not is_valid_url(link):
            invalid_links.append(link)
            print(f"Invalid URL skipped: {link}")
            continue

        try:
            # Make a HEAD request to check the status code
            response = requests.head(link, timeout=5, allow_redirects=True)
            status_code = response.status_code
        except requests.exceptions.RequestException as e:
            # Treat inaccessible links as 'Unknown'
            status_code = 'Unknown'
        
        # Categorize the link based on the status code
        status_categories[status_code].append(link)
        print(f"Processed: {link} -> {status_code}")
        
        # Add a 1-second delay between requests
        time.sleep(1)

    # Automatically name the output file as 'checkedlinks.txt'
    output_file_path = os.path.join(os.getcwd(), "checkedlinks.txt")
    with open(output_file_path, 'w') as output_file:
        for status, links in sorted(status_categories.items()):
            output_file.write(f"=== Status {status} ===\n")
            output_file.write("\n".join(links))
            output_file.write("\n\n")
        
        if invalid_links:
            output_file.write("=== Invalid Links ===\n")
            output_file.write("\n".join(invalid_links))
            output_file.write("\n\n")

    print(f"Links categorized and saved to {output_file_path}")

# Main function to run the script
if __name__ == "__main__":
    # Prompt user for input file path
    input_file_path = input("Enter the path to the file containing links: ").strip()
    categorize_links(input_file_path)
