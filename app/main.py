import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

from dotenv import load_dotenv
load_dotenv()
import os
os.environ['USER_AGENT'] = os.getenv('USER_AGENT')



def create_streamlit_app(llm, portfolio, clean_text):
    st.title("Cold Email Generator")
    url_input = st.text_input("Enter a URL: ", value="https://jobs.paloaltonetworks.com/en/job/-/-/47263/71837933584?jvs=LinkedIn&sid=2d92f286-613b-4daf-9dfa-6340ffbecf73")
    submit_button = st.button("Submit")


    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            page_content = clean_text(loader.load().pop().page_content)
            
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(page_content)

            for job in jobs:
                skills = job.get("skill", [])
                links = portfolio.query_links(skills)
                email = llm.write_email(job,links)
                st.code(email, language='markdown')
        
        except Exception as e:
            st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout='wide', page_title='Cold Email Generator', page_icon="$")
    create_streamlit_app(chain, portfolio, clean_text)
