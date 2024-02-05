import streamlit as st
from dotenv import load_dotenv
load_dotenv() # load all the environment variables
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi # Responsible for getting the idea of the video from the video url and then it will retrieve the entire transcript

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""
        You are YouTube video summarizer. You will be taking the transcript text
        and summarizing the entire video and providing the important summary in points
        within 250 words. Please provide the summary of the text given here:
        """


# Getting the transcript data from the youtube videos
def extract_transcript_details(youtube_video_url):
    try:
        # Extracting the video id from the url of the youtube video
        video_id=youtube_video_url.split("=")[1] # "=" will divide the url into two terms i.e. zeroth index and first index. So in the first index we will have the id itself
        print(video_id)
        # This transcript is in the form of a list
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id) # get_transcript is the function of YouTubeTranscriptApi

        transcript="" # list
        for i in transcript_text:
            transcript += " " + i["text"] # Appending all the text in the form of a paragraph
        
        return transcript
    except Exception as e:
        raise e


# Function for doing summarization of the transcript that we are getting from the youtube videos. Getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text


st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link=st.text_input("Enter YouTube Video Link:")

# Displaying the thumbnail image in the bottom part
if youtube_link:
    video_id=youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True) # Default image url

# Creating a button to get detailed description
if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)