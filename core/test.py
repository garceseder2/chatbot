import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQAWithSourcesChain, ConversationalRetrievalChain, RetrievalQA
from rich.console import Console


print("Starting...")
NOMBRE_INDICE_CHROMA = "/home/egarces/chatbot/databases/embeddings-public"

llm_openIA = ChatOpenAI(openai_api_key='', model_name='gpt-3.5-turbo', temperature=0.2, max_tokens=1000)
embeddings_st = SentenceTransformerEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
vectorstore_chroma = Chroma(persist_directory=NOMBRE_INDICE_CHROMA, embedding_function=embeddings_st)
print(vectorstore_chroma._persist_directory)
query = "Cual es el parametro para configurar el nuevo reporte Pivot?"

docs = vectorstore_chroma.similarity_search_with_score(query, k=3)
print(docs)
##run_conversation(vectorstore_chroma,"qa",llm_openIA)
print("End")