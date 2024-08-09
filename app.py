import streamlit as st
import openai
from openai import OpenAI
import os
import PyPDF2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
        print(text)

    return text

def convert_to_tweets(text):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that converts educational content into short, tweet-sized explanations."},
            {"role": "user", "content": f"Convert this text into a series of educational tweets explaining the content. Each tweet should be no longer than 280 characters:\n{text}"}
        ]
    )
    # Access the content directly from the message object
    return response.choices[0].message.content.split('\n')

def display_tweet(tweet):
    tweet_html = f"""
    <div style="border: 1px solid #ccc; border-radius: 10px; padding: 10px; margin-bottom: 10px;">
        <img src="https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png" style="width: 48px; height: 48px; border-radius: 50%; float: left; margin-right: 10px;">
        <div style="margin-left: 58px;">
            <strong>Educational Bot</strong> <span style="color: #657786;">@EduTweetBot</span>
            <p>{tweet}</p>
        </div>
    </div>
    """
    st.markdown(tweet_html, unsafe_allow_html=True)

st.title("PDF to Educational Tweets Converter")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    if st.button("Convert to Tweets"):
        with st.spinner("Extracting text from PDF..."):
            pdf_text = extract_text_from_pdf(uploaded_file)
        
        with st.spinner("Generating educational tweets..."):
            tweets = convert_to_tweets(pdf_text)
        
        st.subheader("Generated Educational Tweets:")
        for tweet in tweets:
            if tweet.strip():  # Check if the tweet is not empty
                display_tweet(tweet)

# Add some information about the app
