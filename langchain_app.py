# from datetime import datetime
# import time
import streamlit as st
from streamlit_chat import message
# import pandas as pd
# import numpy as np
# import json
import os
from dotenv import load_dotenv
import openai
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.vectorstores import FAISS
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate


def init_db_and_langchain(data_source="uploaded_data"):

    # Load environment variables (set OPENAI_API_KEY and OPENAI_API_BASE in .env)
    load_dotenv()

    openai.api_type = "azure"
    openai.api_version = "2023-03-15-preview"
    openai.api_base = os.getenv('OPENAI_API_BASE')
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Init LLM and embeddings model
    llm = AzureChatOpenAI(deployment_name="gpt_35_turbo_AG", temperature=0, openai_api_version="2023-03-15-preview")
    embeddings = OpenAIEmbeddings(model="MB_Embedding_Model", chunk_size=1)

    # load documents from data directory
    loader = DirectoryLoader('../data/'+data_source+'/', glob="*.txt", loader_cls=TextLoader)
    documents = loader.load()

    # split docs into chunks of 1000 tokens
    text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    # ingest docs into faiss to efficiently query embeddings
    db = Chroma.from_documents(docs, embeddings)

    # from langchain.vectorstores import FAISS
    # db = FAISS.from_documents(documents=docs, embedding=embeddings)

    # set prompt format and create chain for qna with history
    CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template("""Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

    Chat History:
    {chat_history}
    Follow Up Input: {question}
    Standalone question:""")

    qa = ConversationalRetrievalChain.from_llm(llm=llm,
                                            retriever=db.as_retriever(),
                                            condense_question_prompt=CONDENSE_QUESTION_PROMPT,
                                            return_source_documents=True,
                                            verbose=False) 
    return qa


# Function to get the user's input
def get_query():
    query = st.text_input("Enter your query here:", key="input")
    return query

# function to generate bot response
def generate_response(qa, chat_history, query):
    vectordbkwargs = {"search_distance": 0.5}
    query = query+"\nRespond exactly 'Knowledge Base data is insufficient to answer this question' if you don't have sufficient information in given documents context to answer. Do not use general knowledge."
    result = qa({"question": query, "chat_history": chat_history, "vectordbkwargs": vectordbkwargs})
    response = result['answer']
    return response
    

st.title("Document Search Chatbot")
# user uploads their docs for the db
files = st.file_uploader("Please enter your knowledgebase files here:",
                         accept_multiple_files=True)
# once the Submit button is clicked, the files are saved to the folder path
if st.button("Submit"):
    folder = '../data/uploaded_data'
    for i, file in enumerate(files):
        file_name = file.name # f"uploaded_doc_{i}.txt"
        file_path = os.path.join(folder, file_name)
        with open(file_path, 'wb') as f:
            f.write(file.getbuffer())

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

# keep track of chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# init qa chain
qa = init_db_and_langchain()

# get initial user query
query = get_query()

if query:
    try:
        # get a response from the query
        response = generate_response(qa, st.session_state['chat_history'], query)
        # store the output 
        st.session_state.past.append(query)
        st.session_state.generated.append(response)
        st.session_state['chat_history'].append((query, response))
    except Exception as e:
        st.error(f"An error occurred: {e}")

# display chat
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
    # for i in range(0, len(st.session_state['generated'])-1, 1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        
    

# def init_db_and_langchain(data_source="qna"):

#     import os
#     import openai
#     from dotenv import load_dotenv
#     from langchain.chat_models import AzureChatOpenAI
#     from langchain.embeddings import OpenAIEmbeddings
#     from langchain.embeddings.openai import OpenAIEmbeddings
#     from langchain.vectorstores import Chroma
#     from langchain.text_splitter import CharacterTextSplitter
#     from langchain.llms import OpenAI
#     from langchain.chains import ConversationalRetrievalChain

#     # Load environment variables (set OPENAI_API_KEY and OPENAI_API_BASE in .env)
#     load_dotenv()

#     openai.api_type = "azure"
#     openai.api_version = "2023-03-15-preview"
#     openai.api_base = os.getenv('OPENAI_API_BASE')
#     openai.api_key = os.getenv("OPENAI_API_KEY")

#     # Init LLM and embeddings model
#     llm = AzureChatOpenAI(deployment_name="gpt_35_turbo_AG", temperature=0, openai_api_version="2023-03-15-preview")
#     embeddings = OpenAIEmbeddings(model="MB_Embedding_Model", chunk_size=1)

#     from langchain.document_loaders import DirectoryLoader
#     from langchain.document_loaders import 
#     from langchain.text_splitter import TokenTextSplitter

#     loader = DirectoryLoader('../data/'+data_source+'/', glob="*.txt", loader_cls=TextLoader)

#     documents = loader.load()
#     text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)
#     docs = text_splitter.split_documents(documents)

#     db = Chroma.from_documents(docs, embeddings)

#     # from langchain.vectorstores import FAISS
#     # db = FAISS.from_documents(documents=docs, embedding=embeddings)

#     from langchain.chains import ConversationalRetrievalChain
#     from langchain.prompts import PromptTemplate

#     # Adapt if needed
#     CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template("""Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

#     Chat History:
#     {chat_history}
#     Follow Up Input: {question}
#     Standalone question:""")

#     qa = ConversationalRetrievalChain.from_llm(llm=llm,
#                                             retriever=db.as_retriever(),
#                                             condense_question_prompt=CONDENSE_QUESTION_PROMPT,
#                                             return_source_documents=True,
#                                             verbose=False)
    
#     return db,qa


# ### Function to encompass a query search
# def get_result(db,qa,chat_history,query):
    
#     vectordbkwargs = {"search_distance": 0.5}
    
#     query=query+".\n Respond exactly 'Knowledge Base data is insufficient to answer this question' if you don't have sufficient information in given documents context to answer."
    
#     # if(chat_history!=[]):
#     #     query=".\n".join(chat_history[0])+query
    
#     # docs = db.similarity_search_with_score(query)
#     # print("score",docs[0][-1])
#     # if docs[0][-1]<0.4:
#     # print("Document source:",docs[0])

#     result = qa({"question": query, "chat_history": chat_history,"vectordbkwargs":vectordbkwargs})
    
#     # result = qa({"question": query, "chat_history": chat_history})
#     chat_history_new= [(query, result["answer"])]
    
#     # print("Question:", query)
#     # print("Answer:", result["answer"])
    
#     return result["answer"],chat_history_new
    
#     # else:
#     #     error_res="Knowledge Base data is insufficient to answer this question, please try again with another question or upload new documents to the knowledge base"
#     #     # print(error_res)   
#     #     return error_res,chat_history