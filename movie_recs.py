import pymongo
import requests
import os
from dotenv import load_dotenv
load_dotenv()


client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = client.sample_mflix
collection = db.movies



hf_token = os.getenv("HUGGINGFACE_API_KEY2")
print(hf_token)
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

def gerenate_embeddings(text: str) -> list[float]:
    response = requests.post(
       embedding_url,
       headers={"Authorization": f"Bearer {hf_token}"},
       json={"inputs": text}
    )
    if response.status_code != 200:
        print(response.json())
        raise ValueError("API request failed")
    return response.json()


# for doc in collection.find({'plot': {'$exists': True}}):
#     doc['embedding'] = gerenate_embeddings(doc['plot'])
#     collection.replace_one({"_id": doc["_id"]}, doc)
    
    

    
# print("Done")
query = "imafinary characters from outer space at war"

results = collection.aggregate([
    {"$vectorSearch":{
        "queryVector": gerenate_embeddings(query),
        "path": "embedding",
        "numCandidates": 50,
        "limit": 3,
        "index":"PlotSemanticSearch ",
    }}
])


for res in results:
    print(res)

