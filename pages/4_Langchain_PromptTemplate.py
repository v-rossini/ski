import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

st.title("🦜🔗 Langchain com templates")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
template = st.sidebar.selectbox(
    "Template",
    ["As an experienced data scientist and technical writer, generate an outline for a blog about",
    "As the CEO of a company, generate .....",
    "balblablablaldb"])


def generate_content(topic):
    # Instantiate LLM model
    llm = OpenAI(model_name="text-davinci-003", openai_api_key=openai_api_key)
    # Prompt
    template = template or ("""As an experienced data scientist and technical writer, 
                generate an outline for a blog about""") + {topic}
    prompt = PromptTemplate(input_variables=["topic"], template=template)
    prompt_query = prompt.format(topic=topic)
    # Run LLM model
    response = llm(prompt_query)
    # Print results
    return st.info(response)


with st.form("myform"):
    topic_text = st.text_input("Topic:", "")
    submitted = st.form_submit_button("Submit")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        generate_content(topic_text)
