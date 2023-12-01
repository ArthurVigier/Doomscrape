import pandas as pd # important ne pas supprimez ; data processing, CSV file I/O (e.g. pd.read_csv)
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F


model_name = "distilbert-base-uncased-finetuned-sst-2-english"

model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

classifier = pipeline('sentiment-analysis', model=model_name, tokenizer=tokenizer)
results=classifier(["We are very happy to show you the 🤗 Transformers library.","Narrative warfare: How disinformation shapes the Israeli-Hamas conflict—and millions of minds"])


for result in results:
    print(result)

tokens = tokenizer.tokenize("We are very happy to show you the 🤗 Transformers library.")
token_ids = tokenizer.convert_tokens_to_ids(tokens)
input_ids = tokenizer("We are very happy to show you the 🤗 Transformers library.")

print(f'   Tokens: {tokens}')
print(f'Token IDs: {token_ids}')
print(f'Input IDs: {input_ids}')

X_train = ["We are very happy to show you the 🤗 Transformers library.","Narrative warfare: How disinformation shapes the Israeli-Hamas conflict—and millions of minds"]

batch = tokenizer(X_train, padding=True, truncation=True,max_length=512, return_tensors="pt")

print(batch)

with torch.no_grad():
    outputs = model(**batch, labels=torch.tensor([1, 0]))
    print(outputs)
    predictions = F.softmax(outputs.logits, dim=1)
    print(predictions)
    labels = torch.argmax(predictions, dim=1)
    print(labels)
    labels = [model.config.id2label[label_id] for label_id in labels.tolist()]
    print(labels)

#save_directory = "saved"
#tokenizer.save_pretrained(save_directory)
#model.save_pretrained(save_directory)

model_name = "oliverguhr/german-sentiment-bert"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

X_train_german = ["Ich liebe dich", "Ich hasse dich", "Ich mag dich", "Ich finde dich gut", "Ich finde dich schlecht", "Ich finde dich okay", "Ich finde dich nicht okay", "Ich finde dich nicht gut", "Ich finde dich nicht schlecht","Ich liebe dich night"]

batch = tokenizer(X_train_german, padding=True, truncation=True,max_length=512, return_tensors="pt")
batch = torch.tensor(batch['input_ids'])
print(batch)
with torch.no_grad():
    outputs = model(batch)
    label_ids = torch.argmax(outputs.logits, dim=1)
    print(label_ids)
    labels = [model.config.id2label[label_id] for label_id in label_ids.tolist()]
    print(labels)
# Compare this snippet from doomsdayindexa/middlewares.py:
# Compare this snippet from doomsdayindexa/settings.py:
