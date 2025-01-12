import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import os
import google.generativeai as genai
from documents_key import document_keywords

genai.configure(api_key="AIzaSyCfbu9boxtqPch9pR8GHukty8z2bPSXopU")

# Load the CSV data
data = pd.read_csv("/workspaces/SchemeSaathi/Model/query_classification_with_additional_queries.csv" , encoding='latin-1')

scheme_names = data['scheme_name'].unique().tolist()

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
scheme_embeddings = embedding_model.encode(scheme_names)

def find_closest_match_scheme(query, embeddings, items, threshold=0.75):
    """
    Find the closest match to the query from a list of embeddings.
    Returns the closest item and similarity score, or None if below threshold.
    """
    query_embedding = embedding_model.encode(query)
    similarities = np.dot(embeddings, query_embedding) / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding)
    )
    closest_idx = np.argmax(similarities)
    if similarities[closest_idx] >= threshold:
        return items[closest_idx], similarities[closest_idx]
    return None, 0



def process_query(question):
    """Process the user question to extract relevant information."""
    scheme_match, scheme_similarity = find_closest_match_scheme(question, scheme_embeddings, scheme_names)
    return scheme_match


def find_scheme(question):
  return process_query(question)


"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""


# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  safety_settings=safety_settings,
  generation_config=generation_config,
  system_instruction="Your role is to generate a human friendly respose from the content I am giving to you. Use only my content ",
)

chat_session = model.start_chat(
    history=[]
)

def Main_for_query(question):
    scheme = find_scheme(question)
    if scheme is not None:
        print(scheme)
        filtered_data = data[data['scheme_name'] == scheme]
        filtered_data = filtered_data['eligibility_criteria'].iloc[0] + "\n" + filtered_data['documents_required'].iloc[0] + filtered_data['brief_description'].iloc[0]+ 'application_process : '+filtered_data['application_process'].iloc[0]
        prompt = f"""
        "You are a highly concise and precise assistant. Provide a direct answer to the question after taking few lines from question based strictly on the "
        "available context. Avoid filler phrases like 'Based on the provided context.
        Scheme: {scheme},
        Question: {question}, data : {filtered_data}, use the scheme and  the question to generate the answer for the question use to generate the a response like chatbot. Don't add your input."""

        # filtered_data = data[data['scheme_name'] == scheme]
        # result = hf_hub_llm(prompt_template.format(context=filtered_data, question=question))
        # print(f'Bot: {result}')
        response = chat_session.send_message(prompt)
        return response.text
    else:
        # results = rag_query(question)
        # print(f'Bot: {results}')
        prompt = f"""
        "You are a highly knowledgeable assistant. Provide a direct and accurate answer to the question based on the information you possess. Avoid phrases like 'I do not know' and provide plain information about the subject.
        Question: {question}
        """
        response = chat_session.send_message(prompt)
        return response.text
