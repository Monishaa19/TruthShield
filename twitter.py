[5:09 pm, 29/11/2024] Yashu: import requests
import time
import streamlit as st
from langchain_google_genai import GoogleGenerativeAI

# Twitter API Bearer Token (replace with your actual token)
bearer_token = "AAAAAAAAAAAAAAAAAAAAAIMAxQEAAAAA2XovS%2FfPFvAEFjq5C83ZalG4jJU%3DOnkaffDiazav44i5PDVDnsPOgM0BmeFT8s8r713ZZf7zOVx625"  # replace with your token

# Predefined username
username = "YashashwiniS__"
GEMINI_API_KEY = "AIzaSyBRqRIkLoQX2MAdQ-AvPo_fPOXBxKni3a0"

generation_config = {
    "temperature": 0.2,   # Lower temperature for more conservative and precise outputs
    "top_p": 1.0,         # Set top_p to 1.0 for deterministic outputs based on probability
    "top_k": 0,           # Disable top_k sampling for strict adherence to probabilities
    "max_output_tokens": 8192,   # Maximum number of output tokens to generate
    "response_mime_type": "text/plain",  # Output format type
}

# Initialize Langchain's GoogleGenerativeAI
llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GEMINI_API_KEY)

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

# Streamlit app
st.title("Real-Time Twitter Feed with Langchain Integration")
st.write(f"Fetching live tweets for @{username}:")
tweet_placeholder = st.empty()  # Placeholder for the live tweet content

# Fetch user ID
user_id = get_user_id(username)

if user_id:
    while True:  # Continuously fetch and update tweets
        # Check the rate limit status
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
        
        # Adjust the sleep time to reduce rate of requests
        time.sleep(30)  # Reduce frequency to 30 seconds to avoid rate limit issues
[5:14 pm, 29/11/2024] Yashu: import requests
import time
import streamlit as st
from langchain_google_genai import GoogleGenerativeAI

# Twitter API Bearer Token (replace with your actual token)
bearer_token = "AAAAAAAAAAAAAAAAAAAAEEEDxQEAAAAAyI588G50%2BN66kAiww4gRjmD88ZY%3DfjehksYBfHZ6LAkQCh7ROteQVuyCZuCYqMjXckcOS9hqgPBxCV"  # replace with your token

# Predefined username
username = "PriyankaTR19403"  # replace with the new username
GEMINI_API_KEY = "AIzaSyBRqRIkLoQX2MAdQ-AvPo_fPOXBxKni3a0"

generation_config = {
    "temperature": 0.2,   # Lower temperature for more conservative and precise outputs
    "top_p": 1.0,         # Set top_p to 1.0 for deterministic outputs based on probability
    "top_k": 0,           # Disable top_k sampling for strict adherence to probabilities
    "max_output_tokens": 8192,   # Maximum number of output tokens to generate
    "response_mime_type": "text/plain",  # Output format type
}

# Initialize Langchain's GoogleGenerativeAI
llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GEMINI_API_KEY)

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

# Streamlit app
st.title("Real-Time Twitter Feed with Langchain Integration")
st.write(f"Fetching live tweets for @{username}:")
tweet_placeholder = st.empty()  # Placeholder for the live tweet content

# Fetch user ID
user_id = get_user_id(username)

if user_id:
    while True:  # Continuously fetch and update tweets
        # Check the rate limit status
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
        
        # Adjust the sleep time to reduce rate of requests
        time.sleep(30)  # Reduce frequency to 30 seconds to avoid rate limit issues