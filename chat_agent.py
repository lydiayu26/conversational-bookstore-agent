from dotenv import load_dotenv
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, PyPDFDirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import TokenTextSplitter
from langchain.vectorstores import FAISS
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import openai
import os
import streamlit as st
from streamlit_chat import message


def init_db_and_chain():

    # Load environment variables
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Init LLM and embeddings model
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", chunk_size=1)

    # load documents from data directory (pdfs and txts separately)
    pdf_loader = PyPDFDirectoryLoader('./books/')
    txt_loader = DirectoryLoader('./books/', glob="**/*.txt", loader_cls=TextLoader)
    docs = pdf_loader.load()
    txts = txt_loader.load()
    # consolidate into one list of docs
    docs.extend(txts)

    # split docs into chunks of 1000 tokens
    text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(docs)

    # ingest docs into faiss to efficiently query embeddings
    db = FAISS.from_documents(docs, embeddings)

    # set system prompt for condensing new question with history in case the chat history is very long
    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is."""
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, db.as_retriever(), contextualize_q_prompt
    ) 

    # create system prompt for question answering
    qa_system_prompt = """You are an online bookstore agent for answering customer queries. \
    Use the following pieces of retrieved context to answer the question. \
    If you don't know the answer, say "Sorry, I don't have information on your request."\

    {context}"""
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    # chain for using history and docs to answer questions
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    return rag_chain


# Function to get the user's input
def get_query():
    query = st.text_input("Enter your question here:", key="input")
    return query

# function to generate bot response
def generate_response(rag_chain, chat_history, question):
    ai_msg_1 = rag_chain.invoke({"input": question, "chat_history": chat_history})
    response = ai_msg_1['answer']
    return response
    

st.title("Bookstore Chat")

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

# keep track of chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# init qa chain
qa = init_db_and_chain()

# get initial user query
query = get_query()

if query:
    try:
        # get a response from the query
        response = generate_response(qa, st.session_state['chat_history'], query)
        # store the output 
        st.session_state.past.append(query)
        st.session_state.generated.append(response)
        st.session_state['chat_history'].append((HumanMessage(content=query), response))
    except Exception as e:
        st.error(f"An error occurred: {e}")

# display chat
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
    # for i in range(0, len(st.session_state['generated'])-1, 1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        