import os
import fnmatch
import itertools
import sys

def find_files_with_extensions(unc_path, output_file, extensions):
    """Find files with specified extensions in the UNC path and append to the output file if not already present."""
    # Initialize an empty set for existing files
    existing_files = set()

    # Check if the output file exists before trying to read it
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            existing_files = set(f.read().splitlines())

    found_files = False  # Flag to track if any files were found
    new_files = []  # List to store new files found

    # Set up a spinner animation using itertools
    spinner = itertools.cycle(['-', '\\', '|', '/'])  # Characters to simulate a rotating spinner
    spinner_counter = 0  # Counter to update the spinner less frequently

    for root, dirs, files in os.walk(unc_path, topdown=True):
        # Update spinner and display current directory every 500 iterations
        if spinner_counter % 500 == 0:
            sys.stdout.write(f"\rScanning... {next(spinner)}  Current directory: {root[:50]}")  # Limit dir length to 50 characters
            sys.stdout.flush()
        spinner_counter += 1

        # Loop through each extension and filter files
        for ext in extensions:
            matching_files = fnmatch.filter(files, f"*{ext}")
            for file in matching_files:
                file_path = os.path.join(root, file)
                # Only add the file path if it hasn't been found already
                if file_path not in existing_files:
                    new_files.append(file_path)
                    print(f"\nFound: {file_path}")  # Print each found file on a new line
                    found_files = True  # Set the flag to True if files are found

    # Append the new files to the output file if any are found
    if new_files:
        with open(output_file, 'a') as f:
            for file_path in new_files:
                f.write(file_path + '\n')

    # Clear the spinner line when done
    sys.stdout.write("\rScanning completed.          \n")
    sys.stdout.flush()

    return found_files

# Define output directory and file
output_dir = "PWHunter"  # Folder to store the output text file
output_file = os.path.join(output_dir, "found_files.txt")

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created output directory: {output_dir}")

# Define the file extensions you want to search for
extensions = ['.kdbx', '.apw']  # Add more extensions as needed

while True:
    # Prompt user for the UNC path
    unc_path = input("Enter the UNC path to scan (e.g., \\\\main\\shared) or type 'quit' to exit: ").strip()

    # Check if the user wants to quit
    if unc_path.lower() == 'quit':
        print("Exiting the program. Goodbye!")
        break

    try:
        if find_files_with_extensions(unc_path, output_file, extensions):
            print(f"Previous scan completed. New results appended to {output_file}\n")
        else:
            print(f"No new files with extensions {extensions} found in the specified path.\n")
    except PermissionError as e:
        print(f"Permission error: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
