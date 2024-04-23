import os
from dotenv import load_dotenv
import openai

from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.vectorstores import Chroma
from langchain.text_splitter import TokenTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

load_dotenv()
VECTOR_STORE_PATH: str = "data/storage/"


# Original Langchain code:
# class DocumentQueryEngine:
#     """
#     An engine based on llama index VectorStoreIndex that can query a specified
#     set of documents with natural language.
#     """
#     def __init__(self,
#                  openai_api_type='azure',
#                  openai_api_version='2023-03-15-preview'):
        
#         load_dotenv()
#         openai.api_type = openai_api_type
#         openai.api_version = openai_api_version
#         openai.api_base = os.getenv('OPENAI_API_BASE')
#         openai.api_key = os.getenv("OPENAI_API_KEY")

#         # Init LLM and embeddings model
#         self.llm = AzureChatOpenAI(deployment_name="gpt-35-turbo", 
#                                 temperature=0, 
#                                 openai_api_key="69d18204baae47f0b36bb41c869f9c42",
#                                 openai_api_base="https://azr-oai-dai-ibm-gpt-003.openai.azure.com/",
#                                 openai_api_version="2023-03-15-preview")

#         self.embeddings = OpenAIEmbeddings(model="text-embedding-ada-002",
#                                       deployment="rasiv-ai",
#                                       openai_api_key="69d18204baae47f0b36bb41c869f9c42",
#                                       openai_api_base="https://azr-oai-dai-ibm-gpt-003.openai.azure.com/",
#                                       openai_api_type="azure",
#                                       openai_api_version="2023-03-15-preview",
#                                       chunk_size=1)

#         self.summary_template = """
                                
#                                 Please write a concise summary of 75 words on the following text:


#                                 {text}
#                                 """

#         self.summary_prompt = PromptTemplate (
#                                 input_variables=["text"],
#                                 template=self.summary_template
#         )

#         self.keywords_template = """       
#                                  Please provide a comma separated list of at least 5 top keywords from this text:


#                                  {text}
#                                  """
#         self.keywords_prompt = PromptTemplate(
#                                 input_variables=["text"],
#                                 template=self.keywords_template
#                             )
        
    
#     def _load_docs(self, data_source="data/original"):
#         """
#         Given a path where docus are stores, loads these docs and prepares them
#         for ingestion to vectordb.
#         """
#         # load documents from data directory
#         loader = PyPDFDirectoryLoader(data_source)# DirectoryLoader(data_source, glob="**/*.*")
#         documents = loader.load()

#         # split docs into chunks of 1000 tokens
#         text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)
#         docs = text_splitter.split_documents(documents)
#         # set id to integer and when new docs come, compare docs with the existing vecordb's docs
#         # and take only the ids that have not alreayd been used
#         return docs


#     def _init_db(self, new_files):
#         """
#         Initializes a vectordb store for the embeddings of the provided docs.
#         If new_files is True, then we have to update the existing vectordb with the new files
#         """
#         # load the documents retrieved to local from Azure blob storage and their ids
#         docs = self._load_docs()

#         # check if an existing vectordb already exists
#         if not os.path.isdir("./vectorstores/chromadb/index"):
#             # if an existing one isn't there, create and save it
#             # ingest docs into vector store to efficiently query embeddings
#             self.vectordb = Chroma.from_documents(documents=docs, 
#                                                   embedding=self.embeddings,
#                                                   persist_directory='./vectorstores/chromadb')
#             # save the db to disk
#             self.vectordb.persist()

#         # otherwise, if a vectordb already exists and there are new files to embed,
#         # load the existing vectordb and update it with the new files
#         elif new_files:
#             self.vectordb = Chroma(embedding_function=self.embeddings,
#                               persist_directory="./vectorstores/chromadb")
#             # only add the documents that are already in the vectordb
#             existing_docs = set([doc['source'] for doc in self.vectordb.get()['metadatas']])
#             docs_to_add = [doc for doc in docs if doc.metadata['source'] not in existing_docs]
#              # if there are any new docs to add to the embeddings, update the vectordb and save it
#             if len(docs_to_add) > 0:
#                 self.vectordb.add_documents(docs_to_add)
#             self.vectordb.persist()
        
#         # if there are no new files to embed, just load the existing vectordb
#         else:
#             self.vectordb = Chroma(embedding_function=self.embeddings,
#                                    persist_directory="./vectorstores/chromadb")
    

#     def _init_qa(self):
#         """
#         Initializes a QA chain based on defined message templates.
#         """
#         # define the system and user message templates
#         system_template="""Use the following pieces of context to answer the users question.
#                         If you don't know the answer, just say that "The answer cannot be found in the provided documents. If you have additional documents, please upload them above.", don't try to make up an answer.
#                         ----------------
#                         {summaries}"""
#         messages = [
#         SystemMessagePromptTemplate.from_template(system_template),
#         HumanMessagePromptTemplate.from_template("{question}")
#         ]
#         # combine into one prompt
#         prompt = ChatPromptTemplate.from_messages(messages)
        
#         # init a document QA chain
#         chain_type_kwargs = {'prompt': prompt}
#         self.qa = RetrievalQAWithSourcesChain.from_chain_type(self.llm, 
#                                          chain_type='stuff', 
#                                          retriever=self.vectordb.as_retriever(),  #search_kwargs={"k":1}
#                                          chain_type_kwargs=chain_type_kwargs,
#                                          return_source_documents=True)
        

#     def init_qa_chain(self, new_files):
#         """
#         Updates the vectordb store and the qa chain.
#         """
#         self._init_db(new_files=new_files)
#         self._init_qa()
    

#     def _generate_summary(self, text):
#         """
#         Takes text (str) from a source document and summarizes it.
#         """
#         messages = [
#         HumanMessagePromptTemplate.from_template(self.summary_template),
#         ]
#         prompt = ChatPromptTemplate.from_messages(messages)

#         response = self.llm(prompt.format_prompt(text=text).to_messages())
#         return response.content
    

#     def extract_keywords(self, text):
#         """
#         Takes text (str) from a source document and extracts keywords from it.
#         """
#         messages = [
#         HumanMessagePromptTemplate.from_template(self.keywords_template),
#         ]
#         prompt = ChatPromptTemplate.from_messages(messages)

#         response = self.llm(prompt.format_prompt(text=text).to_messages())
#         return response.content


#     def get_response(self, query):
#         """
#         Given a user query, sends the query to the index query engine and receives a 
#         generated answer based on the source documents.

#         Returns the answer from the LLM as a str and the sources from the documents as
#         a list of dictionaries, where each dict has 'page_label', 'file_name', 'summary',
#         and 'keywords' keys.
#         """
#         # send the query through the QA chain
#         result = self.qa({'question': query})
#         # identify the answer and the sources
#         answer = result['answer']

#         # if the answer is not found, return empty list for sources
#         if "the answer cannot be found in the provided documents" in answer.lower():
#             sources = []
#             return answer, sources

#         # sources will be a dict of dicts: each key is a file name, and paired
#         # are dicts with page number, summary, and keywords keys
#         sources = dict()
#         # loop through the source nodes from the response (each node is a document)
#         for source in result['source_documents']:
#             # this accesses a dictionary with "page_number" and "file_name" for this source
#             metadata = source.metadata
#             # this accesses the text str associated with that file/page for this source
#             source_text = source.page_content
#             # summarize this text
#             summary = self._generate_summary(source_text)
#             # extract keywords from the text
#             keywords = self.extract_keywords(source_text)

#             file_name = metadata['source']
#             # check if this document already exists
#             if file_name not in sources.keys():
#                 # if it doesn't exist, create an empty dict for this file
#                 sources[file_name] = dict()
#                 # add entries for file name, page number and keywords
#                 sources[file_name]['source'] = file_name
#                 sources[file_name]['page_number'] = [metadata['page']]
#                 sources[file_name]['keywords'] = keywords.split(", ")[:5]
#                 sources[file_name]['page_content'] = [source_text]
#                 sources[file_name]['summary'] = [summary]
#             else:
#                 # append page number and keywords to existing entry
#                 sources[file_name]['page_number'].append(metadata['page'])
#                 sources[file_name]['keywords'].extend(keywords.split(", "))  
#                 sources[file_name]['keywords'] = list(set(sources[file_name]['keywords']))
#                 # take just the top 5 keywords
#                 sources[file_name]['keywords'] = sources[file_name]['keywords'][:5]
#         # return the answer and a list of each dict for each unique file
#         return answer, [v for k, v in sources.items()]
    

#     def update_prompt_response(self, query, response, feedback):
#         """
#         Sends user feedback as part of the prompt to the model along with the original query and response.
#         Returns the model's updated response along with the sources.
#         """
#         # define the system and user message templates
#         system_template="""You are a search engine that provides concise answers to queries without pleasantries or apologies. Below are a previous query from the user, a response to it, and the context provided to answer it. You will receive feedback on the answer from the user; please use it to generate an improved answer. Do not apologize or include any other content other than the updated answer.
#                         ----------------
#                         Context: {summaries}""" + f"""\nQuery: {query} \nAnswer: {response}"""

#         messages = [
#         SystemMessagePromptTemplate.from_template(system_template),
#         HumanMessagePromptTemplate.from_template("{question}")
#         ]
#         # combine into one prompt
#         prompt = ChatPromptTemplate.from_messages(messages)
        
#         # init a document QA chain
#         chain_type_kwargs = {'prompt': prompt}
#         qa = RetrievalQAWithSourcesChain.from_chain_type(self.llm, 
#                                          chain_type='stuff', 
#                                          retriever=self.vectordb.as_retriever(),  #search_kwargs={"k":1}
#                                          chain_type_kwargs=chain_type_kwargs,
#                                          return_source_documents=True)
#         result = qa({'question': feedback})
#         answer = result['answer']
#         return answer



# Original llamaindex code:
# import os
# from dotenv import load_dotenv
# import openai


# from langchain import PromptTemplate
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.llms import AzureOpenAI
# from langchain.vectorstores import FAISS, VectorStore
# from llama_index import VectorStoreIndex, SimpleDirectoryReader, LLMPredictor, ServiceContext, LangchainEmbedding
# load_dotenv()
# VECTOR_STORE_PATH: str = "data/storage/"


# class DocumentQueryEngine:
#     """
#     An engine based on llama index VectorStoreIndex that can query a specified
#     set of documents with natural language.
#     """
#     def __init__(self,
#                  openai_api_type='azure',
#                  openai_api_version='2023-03-15-preview'):
        
#         # # Load environment variables (set OPENAI_API_KEY and OPENAI_API_BASE in .env)
#         # load_dotenv()
#         # openai.api_type = openai_api_type
#         # openai.api_version = openai_api_version
#         # openai.api_base = os.getenv('OPENAI_API_BASE')
#         # openai.api_key = os.getenv("OPENAI_API_KEY")

#         self.llm = None
#         self.service_context = None
#         self.query_engine = self._create_index_query()

#         self.summary_template = """
                                
#                                 Please write a concise summary of 75 words on the following text:


#                                 {text}
#                                 """

#         self.summary_prompt = PromptTemplate (
#                                 input_variables=["text"],
#                                 template=self.summary_template
#         )

#         self.keywords_template = """
                                            
#                                  Please extract and list at least 5 top keywords from this text:


#                                  {text}
#                                  """
#         self.keywords_prompt = PromptTemplate(
#                                 input_variables=["text"],
#                                 template=self.keywords_template
#                             )      


#     def _init_service_context(self,
#                               llm_deployment_name="text-davinci-003",
#                               llm_model_name="text-davinci-003",
#                               embedding_model="text-embedding-ada-002",
#                               embedding_deployment="rasiv-ai"):
#         """
#         Initializes an LLM predictor that is used to generate natural language responses to queries
#         and an embeddings model that is used to generate vector embeddings of the text.
#         Encapsulates both into a ServiceContext, which will be used to run queries and create indexes.
#         """
#         # Init LLM and embeddings model
#         self.llm = AzureOpenAI(deployment_name="gpt-35-turbo", 
#                                 temperature=0, 
#                                 openai_api_version="2023-03-15-preview")
#         # self.llm = AzureOpenAI(deployment_name=llm_deployment_name, 
#         #                 model_name=llm_model_name,
#         #                 temperature=0,
#         #                 openai_api_version="2023-05-15"#openai.api_version,
#         #                 model_kwargs={"api_key": "https://azr-akv-dai-ibm-gpt-001.vault.azure.net/secrets/azr-oai-dai-IBM-GPT-001-key/4d8972e773bc4b519ef9b14dd73bed0c" #openai.api_key,
#         #                                 "api_base": openai.api_base,
#         #                                 "api_type": openai.api_type,
#         #                                 "api_version": openai.api_version})
#         llm_predictor = LLMPredictor(llm=self.llm)

#         embeddings = LangchainEmbedding(OpenAIEmbeddings(model="text-embedding-ada-002",
#                                       deployment="rasiv-ai",
#                                       openai_api_key="c5c731a5d2424b17b7604713625b7db9",
#                                       openai_api_base="https://azr-oai-dai-ibm-gpt-002.openai.azure.com/",
#                                       openai_api_type="azure",
#                                       openai_api_version="2023-03-15-preview",
#                                       chunk_size=1),
#             # OpenAIEmbeddings(model=embedding_model,
#             #                                             deployment=embedding_deployment,
#             #                                             openai_api_key= openai.api_key,
#             #                                             openai_api_base=openai.api_base,
#             #                                             openai_api_type=openai.api_type,
#             #                                             openai_api_version=openai.api_version),
#                                         embed_batch_size=1)

#         # create service context to encapsulate llm model and embeddings
#         service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor,
#                                                     embed_model=embeddings)
#         return service_context
    

#     def _create_index_query(self, input_dir="data/original"):
#         """
#         Loads the documents from the data directory and indexes them.
#         Creates and returns an engine to query the documents stored in the vector index.
#         """
        
#         self.service_context = self._init_service_context()
#         # load documents and index them
#         documents = SimpleDirectoryReader(input_dir, filename_as_id=True).load_data()
#         vector_index = VectorStoreIndex.from_documents(documents, service_context=self.service_context)

#         """vector_store: VectorStore = FAISS.from_documents(
#         documents=documents, embedding=vector_index
#     )
#         vector_store.save_local(folder_path=VECTOR_STORE_PATH)
#         print("Embeddings saved to " + VECTOR_STORE_PATH) """

#         # create a query engine to query documents
#         query_engine = vector_index.as_query_engine()
#         return query_engine
    

#     def _generate_summary(self, text):
#         """
#         Takes text (str) from a source document and summarizes it.
#         """
#         summary_prompt = self.summary_prompt.format(text=text)
#         return self.llm(summary_prompt) 
    

#     def extract_keywords(self, text):
#         """
#         Takes text (str) from a source document and extracts keywords from it.
#         """
#         keywords_prompt = self.keywords_prompt.format(text=text)
#         return self.llm(keywords_prompt) 


#     def get_response(self, query):
#         """
#         Given a user query, sends the query to the index query engine and receives a 
#         generated answer based on the source documents.

#         Returns the answer from the LLM as a str and the sources from the documents as
#         a list of dictionaries, where each dict has 'page_label' and 'file_name' keys.
#         """
#         # send the query to the engine
#         response = self.query_engine.query(query)
#         # identify the answer and the sources
#         answer = response.response

#         # sources will be a dict of dicts: each key is a file name, and paired
#         # are dicts with page number, summary, and keywords keys
#         sources = dict()
#         # loop through the source nodes from the response (each node is a document)
#         for source in response.source_nodes:
#             # this accesses a dictionary with "page_number" and "file_name" for this source
#             metadata = source.node.extra_info
#             # this accesses the text str associated with that file/page for this source
#             source_text = source.node.text
#             # summarize this text
#             summary = self._generate_summary(source_text)
#             # extract keywords from the text
#             keywords = self.extract_keywords(source_text)

#             file_name = metadata['file_name']
#             # check if this document already exists
#             if file_name not in sources:
#                 # if it doesn't exist, create an empty dict for this file
#                 sources[file_name] = dict()
#                 # add entries for file name, page number and keywords
#                 sources[file_name]['file_name'] = file_name
#                 sources[file_name]['page_number'] = [metadata['page_label']]
#                 sources[file_name]['keywords'] = [keywords]
#             else:
#                 # append page number and keywords to existing entry
#                 sources[file_name]['page_number'].append(metadata['page_label'])
#                 sources[file_name]['keywords'].append(keywords)        
#         # return the answer and a list of each dict for each unique file
#         return answer, [v for k, v in sources.items()]
    


    

    
        


