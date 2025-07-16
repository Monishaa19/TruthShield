import os
import streamlit as st
import pandas as pd
import subprocess
import streamlit.components.v1 as components
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langchain_google_genai import GoogleGenerativeAI  # Assuming correct import path
from deep_translator import GoogleTranslator
import requests
import time


# Twitter API Bearer Token (replace with your actual token)
bearer_token = "AAAAAAAAAAAAAAAAAAAAAD8DxQEAAAAArZD%2BZVW742qV0nWAovSFvqQY22Y%3DHVnnohnIT2wuZaJAiV42a7oSnxGYOHPTl6AiZDY1LdmemybncQ"  # replace with your token

# Predefined username
username = "SumaM659565"

# Configure Google Generative AI
GEMINI_API_KEY = "AIzaSyBRqRIkLoQX2MAdQ-AvPo_fPOXBxKni3a0"
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

generation_config = {
    "temperature": 0.2,   # Lower temperature for more conservative and precise outputs
    "top_p": 1.0,         # Set top_p to 1.0 for deterministic outputs based on probability
    "top_k": 0,           # Disable top_k sampling for strict adherence to probabilities
    "max_output_tokens": 8192,   # Maximum number of output tokens to generate
    "response_mime_type": "text/plain",  # Output format type
}

llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GEMINI_API_KEY)
# Initialize NLTK Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Define PromptTemplate class
class PromptTemplate:
    def __init__(self, input_variables, template):
        self.input_variables = input_variables
        self.template = template

    def format(self, **kwargs):
        return self.template.format(**kwargs)

# Streamlit App Configuration for "TruthShield AI Guard"
st.set_page_config(page_title="TruthShield AI Guard", page_icon="🛡", layout="wide")
st.title("TruthShield AI Guard")

# Function to fetch user ID by username using Twitter API v2
def get_user_id(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        user_data = response.json()
        return user_data['data']['id']
    elif response.status_code == 429:  # Rate limit error
        st.write("Rate limit exceeded. Waiting for reset.")
        return None
    else:
        st.error(f"Error fetching user ID: {response.status_code} - {response.text}")
        return None

# Function to fetch the latest tweet from the user timeline
def get_latest_tweet(user_id):
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tweets = response.json()
        if "data" in tweets and len(tweets["data"]) > 0:
            return tweets["data"][0]["text"]
        else:
            return "No tweets available."
    elif response.status_code == 429:  # Rate limit error
        st.write("Rate limit exceeded while fetching tweets. Waiting for reset.")
        return None
    else:
        st.error(f"Error fetching tweets: {response.status_code} - {response.text}")
        return None

# Function to check the rate limit status and handle waiting
def check_rate_limit():
    url = "https://api.twitter.com/1.1/application/rate_limit_status.json"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        rate_limit_data = response.json()
        remaining = rate_limit_data['resources']['statuses']['/statuses/user_timeline']['remaining']
        reset_time = rate_limit_data['resources']['statuses']['/statuses/user_timeline']['reset']
        return remaining, reset_time
    else:
        st.error(f"Error fetching rate limit: {response.status_code} - {response.text}")
        return 0, 0

# Function to generate responses using Langchain (GoogleGenerativeAI)
def generate_langchain_response(input_text):
    quest = f"I want to get more information about this particular statement: {input_text}. Strictly generate URLs, and provide a short explanation of about 200 words based on credible sources such as government-related websites or known news platforms."
    response = llm.invoke(quest)
    return response


def read_html_file(file_path):
    with open(file_path, 'r') as file:
        html_content = file.read()
    return html_content

# Render the HTML file
def render_html(html_content):
    components.html(html_content, height=600, scrolling=True)

# Function to run comparison subprocess
def run_comparison(post_input, content_variable):
    command = ['python', 'compare_credible.py', post_input, content_variable]
    st.write("Running subprocess2...")

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        subprocess_output = result.stdout.strip()
        st.write(f"Subprocess output: {subprocess_output}")
        st.session_state.comparison_result = subprocess_output  # Store comparison result in session state
    except Exception as e:
        st.error(f"Error running subprocess: {e}")

# Function to analyze sentiment of comments
def analyze_sentiment(comment):
    sentiment_score = sia.polarity_scores(comment)
    return sentiment_score['compound']

# Function to run sentiment analysis
def run_sentiment_analysis(comments):
    try:
        # Create DataFrame from comments
        df = pd.DataFrame({'comments': comments})

        # Analyze sentiment for each comment
        df['sentiment_score'] = df['comments'].apply(analyze_sentiment)
        df['sentiment'] = df['sentiment_score'].apply(lambda x: 'Negative' if x < -0.2 else 'Positive')

        # Report negative comments
        negative_comments = df[df['sentiment'] == 'Negative']
        st.subheader("Negative Comments Report:")
        st.dataframe(negative_comments)

        # Display warning for sensitive content
        if len(negative_comments) > 0:
            st.warning("Warning: There are sensitive comments that may require attention.")

    except Exception as e:
        st.error(f"Error running sentiment analysis: {e}")

def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        st.error(f"Translation error: {e}")
        return text  # Return original text if translation fails


# Main Streamlit App code for "TruthShield AI Guard"
def main():
    html_file_path = "Homepage1.html"

    # Read and render the HTML file
    try:
        html_content = read_html_file(html_file_path)
        render_html(html_content)
    except Exception as e:
        st.error(f"Error reading or rendering HTML file: {e}")
 
    html_file_path = os.path.join("Homepage2.html")

# Check if the file exists before displaying
    if os.path.exists(html_file_path):
        with open(html_file_path, "r") as f:
            html_content = f.read()
            st.markdown(html_content, unsafe_allow_html=True)
    else:
        st.error("Page not found: Homepage2.html")

    st.title("Real-Time Twitter Feed with Langchain Integration")
    st.write(f"Fetching live tweets for @{username}:")
    tweet_placeholder = st.empty()  # Placeholder for the live tweet content

# Fetch user ID
    user_id = get_user_id(username)

    if user_id:
            remaining, reset_time = check_rate_limit()

            if remaining == 0:  # If we're at the rate limit
                reset_in = reset_time - int(time.time())  # Calculate time until reset
                st.write(f"Rate limit exceeded. Waiting for {reset_in} seconds...")
                time.sleep(reset_in)  # Wait until the rate limit resets

            tweet = get_latest_tweet(user_id)
            if tweet:
                tweet_placeholder.text_area("Latest Tweet", tweet, height=200)
            
            # Now call Langchain for the tweet's topic
                langchain_response = generate_langchain_response(tweet)
                st.write("Langchain Response:")
                st.write(langchain_response)
    post_input = st.text_area("Write your post:", max_chars=10000)

    if st.button("Start Fact Checking"):
        if post_input:
            # Translate the input text to English
            post_input_english = translate_to_english(post_input)
            st.write(f"Translated text to English: {post_input_english}")

            command = ['python', 'research_llm.py', post_input_english]
            st.write("Running subprocess1...")

            # Run the subprocess and capture the output
            result = subprocess.run(command, capture_output=True, text=True)
            subprocess_output = result.stdout.strip()
            st.write(f"Subprocess1 output: {subprocess_output}")

            # Define the prompt template
            quest = """
            Separate the given text into two parts: the main content and a list of URLs. Format the output as follows:

            Content: <main content>

            URLs: <list of URLs>

            Text: {your_text}
            """
            prompt_template = PromptTemplate(input_variables=["your_text"], template=quest)
            prompt = prompt_template.format(your_text=post_input_english)

            # Assuming llm is initialized correctly somewhere
            llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GEMINI_API_KEY)
            response = llm.invoke(prompt)

            # Split the generated text into content and URLs
            content_split = response.split("URLs:")
            content = content_split[0].replace("Content:", "").strip()
            urls_section = content_split[1].strip() if len(content_split) > 1 else "No URLs found."

            # Store content in a variable
            content_variable = content

            st.write("Your information is backed by a strong credible and reliable source of information. Few of these domains containing related content to your post are:")

            # Store state to prevent page reload
            st.session_state.post_input = post_input_english
            st.session_state.content_variable = content_variable

    # Check if post_input and content_variable are in session state to continue
    if hasattr(st, 'session_state') and "post_input" in st.session_state and "content_variable" in st.session_state:
        if st.button("Continue with comparison"):
            run_comparison(st.session_state.post_input, st.session_state.content_variable)

        if st.button("Check Sensitivity"):
            if "comparison_result" in st.session_state:
                run_sentiment_analysis([st.session_state.comparison_result])
                command = ['python', 'sentimental_analysis.py', st.session_state.post_input]
                st.write("Running subprocess3...")

                # Run the subprocess and capture the output
                result = subprocess.run(command, capture_output=True, text=True)
                subprocess_output = result.stdout.strip()
                st.write(f"Subprocess3 output: {subprocess_output}")

            else:
                st.warning("Please perform comparison before checking sensitivity.")

    else:
        st.warning("Please write a post and start fact checking before continuing.")

if __name__ == "__main__":
    main()
