import openai
from dotenv import load_dotenv
import os
import csv
import concurrent.futures
from tqdm import tqdm
import argparse


try:
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if openai.api_key is None:
        raise ValueError("La clé API OpenAI n'est pas définie dans les variables d'environnement.")
except Exception as e:
    print(f"Une erreur s'est produite lors du chargement des variables d'environnement : {e}")
    exit(1)

contents ="I am working on a project to assess the impact of news headlines. I have a scale from -1 to 2, where -1 represents a catastrophic event threatening humanity, 0 is neutral, and 2 signifies a worldwide positive event of great significance. Here are the keywords associated with each score: -1.0: Catastrophic, -0.9: Disastrous, -0.8: Critical Concern, -0.7: Severe Crisis, -0.6: Critical, -0.5: Major Negative impact, -0.4: Serious Concern, -0.3: Notable Adversity, -0.2: Significant Problem, -0.1: Minor Problem, 0.0: Neutral / Benign, 0.1: Slightly Positive, 0.2: Minor Benefit, 0.3: Noticeable Advantage, 0.4: Moderately Good, 0.5: Positive Impact, 0.6: Considerably Beneficial, 0.7: Very Positive, 0.8: Major Positive Impact, 0.9: Substantial Gain, 1.0: Significant Success, 1.1: Exceptionally Favorable, 1.2: Remarkably Positive, 1.3: Outstandingly Beneficial, 1.4: Transformative Positive Effect, 1.5: Breakthrough Achievement, 1.6: Historical Positive Milestone, 1.7: Revolutionary Change, 1.8: Global Positive Influence, 1.9: Pioneering Progress, 2.0: World-Saving."


def get_line_sentiment(chat_model, chat_log, tweet):
    try:
        messages = chat_log + [{"role": "user", "content": tweet}]
        res = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=messages
        )
        chat_log.append({"role": "user", "content": tweet})
        chat_log.append({"role": "assistant", "content": res["choices"][0]["message"]["content"]})
        return res["choices"][0]["message"]["content"], chat_log
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'obtention du sentiment de la ligne : {e}")
        return None, chat_log

def process_row(row):
  global chat_model
  global chat_log
  importance = row[1]  # Utilisation de la colonne "importance"
  sentiment, chat_log = get_line_sentiment(chat_model, chat_log, importance)
  if sentiment is None:
    sentiment = "Erreur lors de l'obtention du sentiment"
  print(sentiment)
  return row + [sentiment]



# Création du parseur d'arguments
parser = argparse.ArgumentParser(description='Traite un certain nombre de lignes d\'un fichier CSV.')
parser.add_argument('--num_lignes', type=int, default=10000, help='Le nombre de lignes à traiter')

# Analyse des arguments passés au script
args = parser.parse_args()

# Utilisation de l'argument dans le code 
with open('/Users/robertbadinter/DoomsdayIndex/ai/testdata.csv', 'r') as input_file, open('/Users/robertbadinter/DoomsdayIndex/ai/first_output.csv', 'w', newline='') as output_file:
  try:
    reader = csv.reader(input_file)
    next(reader, None)

    writer = csv.writer(output_file)
    writer.writerow(['Headline', 'Importance', 'Sentiment'])

    chat_model = "gpt-4-1106-preview"
    chat_log = [{"role": "system", "content": contents}]

    for row in tqdm(list(reader)[:args.num_lignes]):
      writer.writerow(process_row(row))
  except Exception as e:
    print(f"Une erreur s'est produite lors du traitement du fichier CSV : {e}")


"""
# Ouverture du fichier CSV d'entrée et du fichier CSV de sortie
with open('filtred_news_no_zero_importance.csv', 'r') as input_file, open('output.csv', 'w', newline='') as output_file:
  try:
    reader = csv.reader(input_file)
    next(reader, None)

    writer = csv.writer(output_file)
    writer.writerow(['Headline', 'Importance', 'Sentiment'])

    chat_model = "gpt-4-1106-preview"
    chat_log = [{"role": "system", "content": contents}]

    for row in tqdm(list(reader)[:args.num_lignes]):
      writer.writerow(process_row(row))
  except Exception as e:
    print(f"Une erreur s'est produite lors du traitement du fichier CSV : {e}")
"""