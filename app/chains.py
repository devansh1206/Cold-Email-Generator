import os
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.exceptions import OutputParserException

from dotenv import load_dotenv
load_dotenv()
import os 
os.environ['USER_AGENT'] = os.getenv("USER_AGENT")


class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.1-70b-versatile",
            temperature = 0,
            groq_api_key = os.getenv("GROQ_API_KEY"),
        )

    def extract_jobs(self, cleaned_text):
        prompt_template = PromptTemplate.from_template(
            '''
            ### scrap text from website:
            {page_data}
            ### Instruction:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys:
            `role`, `experience`, `skill`, and `description`.
            Only return the valid JSON.
            Also ignore suggested job roles, only include the main one
            ### Valid JSON (no preamble)
            '''
        )
        chain_extract = prompt_template | self.llm
        response = chain_extract.invoke(input={'page_data':cleaned_text})
        try:
            json_parser = JsonOutputParser()
            json_output = json_parser.parse(response.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse job.")
        return json_output if isinstance(json_output, list) else [json_output]

    def write_email(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
                {job_description}
                
                ### INSTRUCTION:
                You are Mohan, a business development executive at AtliQ. AtliQ is an AI & Software Consulting company dedicated to facilitating
                the seamless integration of business processes through automated tools. 
                Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
                process optimization, cost reduction, and heightened overall efficiency. 
                Your job is to write a cold email to the client regarding the job mentioned above describing the capability of AtliQ 
                in fulfilling their needs.
                Also add the most relevant ones from the following links to showcase Atliq's portfolio: {link_list}
                Remember you are Mohan, BDE at AtliQ. 
                Do not provide a preamble.
                ### EMAIL (NO PREAMBLE):
            """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": job, "link_list": links})
        return res.content

