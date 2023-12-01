import pandas as pd
from nltk.tokenize import word_tokenize

# Lire le fichier CSV
df = pd.read_csv('/Users/robertbadinter/DoomsdayIndex/ai/filtered_news_no_zero_importance.csv')

print(df.columns) 

# Assumer que la colonne de texte est appelée 'text'
text = df['Headline'].str.cat(sep=' ')

# Tokeniser le texte
tokens = word_tokenize(text)

# Compter le nombre de tokens
num_tokens = len(tokens)

print(f'Le nombre de tokens est : {num_tokens}')
