import csv
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Specify the file path
file_path = "/Users/robertbadinter/DOOMSDAYINDEX/filtered_news_no_zero_importance.csv"

# Specify the output file path
output_file_path = "/Users/robertbadinter/DOOMSDAYINDEX/output.csv"

# Specify the prompt
prompt = "As a risk management expert, your task is to assess and assign a ranking from 0 to 2 to each headline based on its global significance. A rating of 0 indicates a benign impact, while 2 signifies a potential threat to the survival of the human race. "

# Load the model and tokenizer
model = AutoModelForCausalLM.from_pretrained("01-ai/Yi-34B", device_map="auto")
tokenizer = AutoTokenizer.from_pretrained("01-ai/Yi-34B")

# Move model to GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Print the device that is being used
if device.type == 'cuda':
    print("Using CUDA (GPU).")
else:
    print("Using CPU.")

model = model.to(device)

# Open the CSV file
with open(file_path, "r") as file:
    # Create a CSV reader
    reader = csv.reader(file)
    
    # Skip the header row
    next(reader)
    
    # Open the output CSV file
    with open(output_file_path, "w") as output_file:
        # Create a CSV writer
        writer = csv.writer(output_file)
        
        # Write the header row
        writer.writerow(["headline", "output"])
        
        # Go through each row in the CSV file
        for row in reader:
            # Get the headline
            headline = row[0]
            
            # Create the input text
            input_text = prompt + headline
            
            # Encode the input text
            inputs = tokenizer(input_text, return_tensors="pt")
            
            # Move input_ids to the same device as the model
            input_ids = inputs.input_ids.to(device)
            
            # Generate the output
            output = model.generate(
                input_ids,
                max_length=256,
                eos_token_id=tokenizer.eos_token_id,
                do_sample=True,
                repetition_penalty=1.3,
                no_repeat_ngram_size=5,
                temperature=0.7,
                top_k=40,
                top_p=0.8,
            )
            
            # Decode the output
            output_text = tokenizer.decode(output[0], skip_special_tokens=True)
            
            # Write the headline and output to the CSV file
            writer.writerow([headline, output_text])