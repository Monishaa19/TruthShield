import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

# Download VADER lexicon if not already available
nltk.download('vader_lexicon')

# Initialize the VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Function to analyze sentiment
def analyze_sentiment(comment):
    sentiment_score = sia.polarity_scores(comment)
    return sentiment_score['compound']

# Path to your text file
file_path = '"C:\Users\prart\OneDrive\Desktop\comments.txt"'  # Update with your actual file path

comments = []  # Initialize comments variable

try:
    # Read the text file and split into comments
    with open(file_path, 'r', encoding='utf-8') as file:
        comments = file.readlines()
    # Debugging: Print the first few comments to verify file reading
    print(f"Read {len(comments)} comments from the file.")
except FileNotFoundError:
    print(f"Error: The file at path {file_path} was not found.")
except IOError as e:
    print(f"Error reading the file: {e}")

# Proceed if comments were successfully read
if comments:
    # Create DataFrame from comments
    df = pd.DataFrame(comments, columns=['comments'])

    # Analyze sentiment for each comment
    df['sentiment_score'] = df['comments'].apply(analyze_sentiment)
    df['sentiment'] = df['sentiment_score'].apply(lambda x: 'Negative' if x < -0.5 else 'Positive')

    # Print results
    print(df)

    # Report negative comments
    negative_comments = df[df['sentiment'] == 'Negative']
    print("Negative Comments Report:")
    print(negative_comments)
else:
    print("No comments to process.")