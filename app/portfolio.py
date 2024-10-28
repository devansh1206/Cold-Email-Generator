import pandas as pd 
import chromadb as cd 
# import uuid
from dotenv import load_dotenv
load_dotenv()
import os
os.environ['USER_AGENT'] = os.getenv('USER_AGENT')

class Portfolio:
    def __init__(self, file_path="app/resource/portfolios.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = cd.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolios")

    def load_portfolio(self):
        if not self.collection.count():
            i=1
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=row['Techstack'],
                    metadatas={'links':row['Links']},
                    ids = [str(i)]
                )
                i+=1
    
    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])