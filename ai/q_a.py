import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import pandas as pd

RUNPOD_ID='ux0qwnl80w0dr6' 

# Load the dataset
df = pd.read_csv('/Users/robertbadinter/DoomsdayIndex/ai/filtered_news_no_zero_importance.csv', nrows=10000)

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("cerebras/btlm-3b-8k-base")
model = AutoModelForCausalLM.from_pretrained("cerebras/btlm-3b-8k-base", trust_remote_code=True, torch_dtype="auto")

# Set the prompt for generating text
prompt = """
Model: I am working on a project to assess the impact of news headlines. I have a scale from -1 to 2, where -1 represents a catastrophic event threatening humanity, 0 is neutral, and 2 signifies a worldwide positive event of great significance. Below are keywords associated with each score:

- -1.0: Catastrophic
- -0.9: Disastrous
- -0.8: Critical Concern
- -0.7: Severe Crisis
- -0,6: Critical
- -0.5: Major Negative impact
- -0.4: Serious Concern
- -0.3: Notable Adversity
- -0.2: Significant Problem
- -0.1: Minor Problem
- 0.0: Neutral / Benign
- 0.1: Slightly Positive
- 0.2: Minor Benefit
- 0.3: Noticeable Advantage
- 0.4: Moderately Good
- 0.5: Positive Impact
- 0.6: Considerably Beneficial
- 0.7: Very Positive
- 0.8: Major Positive Impact
- 0.9: Substantial Gain
- 1.0: Significant Success
- 1.1: Exceptionally Favorable
- 1.2: Remarkably Positive
- 1.3: Outstandingly Beneficial
- 1.4: Transformative Positive Effect
- 1.5: Breakthrough Achievement
- 1.6: Historical Positive Milestone
- 1.7: Revolutionary Change
- 1.8: Global Positive Influence
- 1.9: Pioneering Progress
- 2.0: World-Saving

For each headline provided in the 'filtered_news_no_zero_importance.csv' file, I need you to assign a score and a keyword from the above scale. The score should reflect the impact of the event described in the headline, and the keyword should correspond to that score. Please provide a brief justification for your choice.

Here is an example to illustrate:

Headline: "Global pandemic declared with millions at risk."
Assigned Score and Keyword: -0.8, Critical Concern
Justification: This headline indicates a significant negative impact on a global scale, hence the score of -0.8 and the keyword 'Critical Concern'.
"""

# Tokenize the prompt and convert to PyTorch tensors
inputs = tokenizer(prompt, return_tensors="pt")

def create_prompt_for_headline(headline):
    return prompt + f'Headline: "{headline}"'

# Define the batch size
batch_size = 10

# Create a new column in the DataFrame to store the generated text
# Initialize the 'Generated_Text' column
df['Generated_Text'] = ''

# Process the headlines in batches
for i in range(0, len(df), batch_size):
    batch = df[i:i+batch_size]
    
    # Generate text for each headline in the batch
    for index, row in batch.iterrows():
        headline_prompt = create_prompt_for_headline(row['Headline'])
        inputs = tokenizer(headline_prompt, return_tensors="pt")
        outputs = model.generate(**inputs, num_beams=5, max_new_tokens=50, early_stopping=True, no_repeat_ngram_size=2)
        generated_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        
        # Add the generated text to the DataFrame
        df.at[index, 'Generated_Text'] = generated_text[0]

    # Write the batch to the CSV file
    batch.to_csv('/Users/robertbadinter/DoomsdayIndex/ai/refined_data.csv', mode='a', header=False, index=False)


"""
MULTITHREADING

from concurrent.futures import ThreadPoolExecutor

def generate_text(row):
    headline_prompt = create_prompt_for_headline(row['Headline'])
    inputs = tokenizer(headline_prompt, return_tensors="pt")
    outputs = model.generate(**inputs, num_beams=5, max_new_tokens=50, early_stopping=True, no_repeat_ngram_size=2)
    generated_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return generated_text[0]

# Create a new column in the DataFrame to store the generated text
df['Generated_Text'] = ''

# Create a ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=5) as executor:
    # Generate text for each headline in the DataFrame
    df['Generated_Text'] = list(executor.map(generate_text, df.iterrows()))

# Write the DataFrame to a CSV file
df.to_csv('/path/to/your/output.csv', index=False)
"""
