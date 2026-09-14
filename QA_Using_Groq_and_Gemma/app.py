import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROK_API_KEY")
st.title("Gemma Model Document Q&A")

llm = ChatGroq(api_key=groq_api_key, model="openai/gpt-oss-20b")
prompt = ChatPromptTemplate.from_template(
	"""
	Answer the questions based on the provided context only.
	Please provide the most accurate response based on the question
	<context> {context}
	Questions: {input}
	"""
)

def vector_embedding():
	if "vectors" not in st.session_state:
		st.session_state.embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
		st.session_state.loader=PyPDFDirectoryLoader("./us_census")
		st.session_state.docs = st.session_state.loader.load()
		st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap= 200)
		st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs)
		st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)


prompt1 = st.text_input("What you want to ask from documents?")
if st.button("creating vector store"):
	vector_embedding()
	st.write("Vector DB IS Ready")

import time
if prompt1:
	document_chain = create_stuff_documents_chain(llm, prompt)
	retriever = st.session_state.vectors.as_retriever()
	retriever_chain = create_retrieval_chain(retriever, document_chain)
	start = time.process_time()
	response = retriever_chain.invoke({'input':prompt1})
	st.write(response['answer'])

	with st.expander("Document Similarity Search"):
		for i, doc in enumerate(response['context']):
			st.write(doc.page_content)
			st.write("-----------------------------------------------")
