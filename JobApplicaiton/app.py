import csv
import webbrowser
import time

# Replace 'file.csv' with your actual CSV file path
csv_file = 'file.csv'

# Open the CSV file and read URLs
with open(csv_file, newline='') as file:
    reader = csv.reader(file)
    urls = [row[0] for row in reader if row]  # Extract URLs from the first column

# Open the first 50 links
for i, url in enumerate(urls[:50], 1):
    webbrowser.open(url)
    time.sleep(0.5)  # Small delay to avoid overwhelming the system

# Wait for user input to open the next 20 links at a time
index = 50
while index < len(urls):
    input("Press Enter to open the next 20 links...")
    for url in urls[index:index + 20]:
        webbrowser.open(url)
        time.sleep(0.5)
    index += 20
