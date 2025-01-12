import sys
import pysqlite3
sys.modules['sqlite3'] = pysqlite3

import chromadb
from chromadb.config import Settings
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle



# Initialize client with persistence
persist_directory = "/workspaces/SchemeSaathi/Model/chroma.sqlite3"  # Directory to store persistent data
client = chromadb.Client(Settings(persist_directory = persist_directory))


collection_name = "scheme_data_collection"
data_collection = client.get_or_create_collection(name=collection_name)

data = pd.read_csv("/workspaces/SchemeSaathi/Model/query_classification_with_additional_queries.csv")

# Add data to the collection
meta = []
docu = []
ids = []

for i in range(len(data)):
    meta.append({"category": f"{data['scheme_name'][i]}"})
    docu.append(f"{data['combined_text'][i]}")
    ids.append(str(i))

data_collection.add(
    documents=docu,
    metadatas=meta,
    ids=ids
)


with open("/workspaces/SchemeSaathi/Model/scheme_embeddings.pkl", "rb") as f:
    saved_data = pickle.load(f)

scheme_embeddings = saved_data["embeddings"]
x = saved_data["items"]
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')



def find_closest_match(query, embeddings, items, threshold=0.1):
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
    scheme_match, scheme_similarity = find_closest_match(question, scheme_embeddings, x)
    return scheme_match

def search(query):
  t = ["Central"]
  t.append(process_query(query))
  print(t)
  result_for_state = []
  all_results = []
  for i in range(len(t)) :
    results = data_collection.query(
        query_texts=[query],
        n_results=10,
        where_document={"$contains":t[i]},

    )
    if(i==1):
        ids = results['ids'][0]
        distances = results['distances'][0]  
        filtered_ids = [[id_ for id_, dist in zip(ids, distances) if dist < 1]]
        all_results.append(filtered_ids)
    else:
      all_results.append(results["ids"])
  final_result = []
  for i in all_results:
    for j in i :
      for k in j:
        final_result.append(int(k))
  return final_result

def check_elements(x, y):
  not_in_y = []
  for element in y:
    if element not in x:
      not_in_y.append(element)
  return not_in_y

def For_Recommedation_Suggestion(Details , Documents):
  query = Details
  from_user = Documents
  results = search(query)
  send_from_server = [[],[]]
  # print(results)
  for idx in results:
      list_ = check_elements([li.strip() for li in from_user.split(',')] ,[li.strip() for li in data['documents_required'][idx].split(',')])
      if list_ == []:
        print(f"Recommended:{data['ID'][idx]}, Scheme Name: {data['scheme_name'][idx]}")
        send_from_server[0].append(idx)
      else:
        print(f"sugested : ID: {data['ID'][idx]}, Scheme Name: {data['scheme_name'][idx]} , Missing Document : {list_}")
        send_from_server[1].append({idx:list_})
  return send_from_server

query = "Student from Punjab"
from_user = "Aadhaar card,PAN card,Birth certificate or age certificate,Community certificate,Caste certificate (SC/ST/OBC/EWS),Disability certificate or proof,Income certificate , Ration card"
for_recommender = For_Recommedation_Suggestion(query , from_user)


