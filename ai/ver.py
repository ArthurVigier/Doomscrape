import csv

# Specify the file path
file_path = "/Users/robertbadinter/DOOMSDAYINDEX/filtered_news_no_zero_importance.csv"

# Initialize the token counter
token_count = 0

# Open the CSV file
with open(file_path, "r") as file:
    # Create a CSV reader
    reader = csv.reader(file)
    
    # Go through each row in the CSV file
    for row in reader:
        # Go through each cell in the row
        for cell in row:
            # Split the cell into tokens
            tokens = cell.split()
            
            # Add the number of tokens to the token counter
            token_count += len(tokens)

# Print the total number of tokens
print(token_count)