import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Set your OpenAI API
# Set your OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Function to get response from OpenAI API with streaming
def get_openai_response(input_text, no_words, blog_style):
    # Define the prompt template
    template = f"""
    Write a blog for {blog_style} job profile for a topic {input_text}
    within {no_words} words.
    """

    # Initialize an empty string for the generated text
    generated_text = ""

    # Create a streaming response from the OpenAI API
    stream = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": template}],
        stream=True,
    )

    # Collect the streamed response
    for message in stream:
        generated_text += message['choices'][0]['delta'].get('content', '')

    return generated_text

st.set_page_config(page_title="Generate Blogs",
                   page_icon='🤖',
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.header("Generate Blogs 🤖")

input_text = st.text_input("Enter the Blog Topic")

# Creating two more columns for additional 2 fields
col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.text_input('No of Words')
with col2:
    blog_style = st.selectbox('Writing the blog for',
                              ('Researchers', 'Data Scientist', 'Common People'), index=0)

submit = st.button("Generate")

# Final response
if submit:
    response = get_openai_response(input_text, no_words, blog_style)
    st.write(response)
