import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQAWithSourcesChain, ConversationalRetrievalChain, RetrievalQA
from rich.console import Console

console = Console()

recreate_chroma_db = False
chat_type = "memory_chat"


def get_query_from_user() -> str:
    """
    Solicita una consulta al usuario.

    Returns:
        La consulta ingresada por el usuario.
    """
    try:
        query = input()
        return query
    except EOFError:
        print("Error: Input no esperado. Por favor intenta de nuevo.")
        return get_query_from_user()



def run_conversation(vectorstore_chroma, chat_type, llm):
    console.print(
        "\n[blue]IA:[/blue] Hola! Qué quieres preguntarme sobre los changeLog de DocManager?"
    )

    if chat_type == "qa":
        console.print(
            "\n[green]Estás utilizando el chatbot en modo de preguntas y respuestas. Este chatbot genera respuestas basándose puramente en la consulta actual sin considerar el historial de la conversación.[/green]"
        )
    elif chat_type == "memory_chat":
        console.print(
            "\n[green]Estás utilizando el chatbot en modo de memoria. Este chatbot genera respuestas basándose en el historial de la conversación y en la consulta actual.[/green]"
        )

    retriever_chroma = vectorstore_chroma.as_retriever(search_kwargs={'k': 3})

    chat_history = []

    while True:
        console.print("\n[blue]Tú:[/blue]")
        query = get_query_from_user()

        if query.lower() == "salir":
            break

        if chat_type == "qa":
            response = process_qa_query(query=query, retriever=retriever_chroma, llm=llm)

        elif chat_type == "memory_chat":
            response = process_memory_query(

                query=query, retriever=retriever_chroma, llm=llm, chat_history=chat_history

            )

        console.print(f"[red]IA:[/red] {response}")




def process_memory_query(query, retriever, llm, chat_history):
    conversation = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=retriever, verbose=False
    )
    console.print("[yellow]La IA está pensando...[/yellow]")
    print(f"La historia antes de esta respuesta es: {chat_history}")
    result = conversation.invoke({"question": query, "chat_history": chat_history})
    chat_history.append((query, result["answer"]))
    return result["answer"]


def process_qa_query(query, retriever, llm):

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever, verbose=False
    )
    console.print("[yellow]La IA está pensando...[/yellow]")
    dicionary=qa_chain.invoke(query)
    return dicionary['result']

def main():
    print("Starting...")
    NOMBRE_INDICE_CHROMA = "/home/egarces/chatbot/databases/embeddings-public"

    llm_openIA = ChatOpenAI(openai_api_key='', model_name='gpt-3.5-turbo', temperature=0.2, max_tokens=1000)
    embeddings_st = SentenceTransformerEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    vectorstore_chroma = Chroma(persist_directory=NOMBRE_INDICE_CHROMA, embedding_function=embeddings_st)
    run_conversation(vectorstore_chroma,"memory_chat",llm_openIA)
    print("End")


if __name__=="__main__":
    main()