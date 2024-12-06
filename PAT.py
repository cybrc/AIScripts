import re
from collections import Counter
import math
from datetime import datetime

# File paths
input_file = "SUMMARY.txt"
output_file = "PASummary.txt"
hvt_file = "hvts.txt"  # High Value Targets list

# Helper functions
def entropy(password):
    """Calculate the Shannon entropy of a string"""
    prob = [password.count(c) / len(password) for c in set(password)]
    return -sum(p * math.log2(p) for p in prob)

def percentage(part, total):
    """Calculate percentage"""
    return f"{(part / total) * 100:.2f}%"

# Load data
with open(input_file) as file:
    lines = file.readlines()

# Extract plaintext passwords
passwords = []
usernames = []
for line in lines:
    parts = line.strip().split(":")
    if len(parts) >= 3 and parts[2]:  # Ensure at least 3 columns and non-empty password
        usernames.append(parts[0])  # Username is in the first column
        passwords.append(parts[2])

total_entries = len(passwords)
unique_passwords = set(passwords)

# Load high value targets (HVT) list
with open(hvt_file) as hvt_file:
    hvt_users = set(hvt_file.read().splitlines())

# Calculate password entropy
password_entropy = {pwd: entropy(pwd) for pwd in passwords}

# Count occurrences of special characters across all passwords
special_characters = ''.join(passwords)
special_characters = re.sub(r'[a-zA-Z0-9]', '', special_characters)  # Remove alphanumeric characters
special_char_counter = Counter(special_characters)

# Find the most used special character and its percentage
if special_char_counter:
    most_used_special_char, most_used_special_count = special_char_counter.most_common(1)[0]
    most_used_special_char_percentage = percentage(most_used_special_count, len(special_characters))
else:
    most_used_special_char = "None"
    most_used_special_count = 0
    most_used_special_char_percentage = "0.00%"

# Root word analysis
root_words = [
    re.split(r'\d+|[^\w]', pwd.lower())[0]
    for pwd in passwords if re.split(r'\d+|[^\w]', pwd.lower())[0]
]
top_root_words = Counter(root_words).most_common(10)

# Top 10 passwords
top_passwords = Counter(passwords).most_common(10)

# Length analysis
length_counts = Counter(map(len, passwords))

# Pattern checks (digits at the end, etc.)
single_digit_end = re.compile(r"\d$")
double_digits_end = re.compile(r"\d{2}$")
triple_digits_end = re.compile(r"\d{3}$")
year_pattern = re.compile(r"(19|20)\d{2}$")
seasons = ["spring", "summer", "autumn", "fall", "winter"]
month_names = [
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december"
]
month_abbr = [month[:3] for month in month_names]
day_names = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

# Initialize counters
single_digit_count = sum(1 for pwd in passwords if single_digit_end.search(pwd))
double_digit_count = sum(1 for pwd in passwords if double_digits_end.search(pwd))
triple_digit_count = sum(1 for pwd in passwords if triple_digits_end.search(pwd))
years_on_end = Counter(year_pattern.findall(pwd)[0] for pwd in passwords if year_pattern.search(pwd))

seasons_in_passwords = Counter(season for pwd in passwords for season in seasons if season in pwd.lower())
months_in_passwords = Counter(month for pwd in passwords for month in month_names if month in pwd.lower())
abbr_months_in_passwords = Counter(month for pwd in passwords for month in month_abbr if month in pwd.lower())
days_in_passwords = Counter(day for pwd in passwords for day in day_names if day in pwd.lower())

# Identify compromised HVTs
compromised_hvts = [user for user, pwd in zip(usernames, passwords) if user in hvt_users]

# Write analysis to file
with open(output_file, "w") as output:
    output.write(f"Summary created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    output.write(f"Total entries: {total_entries}\n")
    output.write(f"Total unique entries: {len(unique_passwords)}\n\n")

    # HVT Section: Show compromised HVTs
    output.write("\nHigh Value Targets Identified:\n")
    if compromised_hvts:
        for user in compromised_hvts:
            output.write(f"{user}: COMPROMISED\n")
    else:
        output.write("No High Value Targets identified as compromised.\n")

    # Top 10 Passwords
    output.write("\nTop 10 Passwords:\n")
    for pwd, count in top_passwords:
        output.write(f"{pwd}: {count} ({percentage(count, total_entries)})\n")

    output.write("\nTop 10 Root Words:\n")
    for root, count in top_root_words:
        output.write(f"{root}: {count} ({percentage(count, total_entries)})\n")

    output.write("\nPassword Length Analysis:\n")
    for length, count in sorted(length_counts.items()):
        output.write(f"Length {length}: {count} ({percentage(count, total_entries)})\n")

    output.write("\nDigits at the End:\n")
    output.write(f"Single digit: {single_digit_count} ({percentage(single_digit_count, total_entries)})\n")
    output.write(f"Double digits: {double_digit_count} ({percentage(double_digit_count, total_entries)})\n")
    output.write(f"Triple digits: {triple_digit_count} ({percentage(triple_digit_count, total_entries)})\n")

    output.write("\nYears at the End:\n")
    for year, count in years_on_end.most_common():
        output.write(f"{year}: {count} ({percentage(count, total_entries)})\n")

    output.write("\nSeasons in Passwords:\n")
    for season, count in seasons_in_passwords.items():
        output.write(f"{season}: {count} ({percentage(count, total_entries)})\n")

    output.write("\nMonths in Passwords:\n")
    for month, count in months_in_passwords.items():
        output.write(f"{month}: {count} ({percentage(count, total_entries)})\n")

    output.write("\nAbbreviated Months in Passwords:\n")
    for abbr, count in abbr_months_in_passwords.items():
        output.write(f"{abbr}: {count} ({percentage(count, total_entries)})\n")

    output.write("\nDays in Passwords:\n")
    for day, count in days_in_passwords.items():
        output.write(f"{day}: {count} ({percentage(count, total_entries)})\n")

    output.write("\nMost Used Special Character:\n")
    output.write(f"Character: {most_used_special_char}\n")
    output.write(f"Count: {most_used_special_count} ({most_used_special_char_percentage})\n")

    output.write("\nPassword Entropy (Top 10 by Entropy):\n")
    top_entropy = sorted(password_entropy.items(), key=lambda x: x[1], reverse=True)[:10]
    for pwd, ent in top_entropy:
        output.write(f"{pwd}: Entropy = {ent:.2f}\n")

print(f"Analysis completed. Results saved to {output_file}")
