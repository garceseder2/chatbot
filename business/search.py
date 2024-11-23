from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


from config import get_config
config = get_config()
vdb_config = config.vectorial_database

embeddings_st = HuggingFaceEmbeddings(model_name=vdb_config['model'])
vectorstore_chroma = Chroma(persist_directory=vdb_config['path'], embedding_function=embeddings_st)

def search_key(query):
    retriever_chroma = vectorstore_chroma.as_retriever(search_kwargs={'k': 5})
    return  retriever_chroma.invoke(query)