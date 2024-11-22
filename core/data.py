import chromadb
from chromadb.utils import embedding_functions

chroma_client = chromadb.Client()
client_persistent = chromadb.PersistentClient(path='/home/egarces/chatbot/databases/embeddings-public')
