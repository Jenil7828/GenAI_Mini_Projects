from dotenv import load_dotenv
load_dotenv()
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chains.question_answering import load_qa_chain
from langchain_core.prompts import PromptTemplate
import os
os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"
import streamlit as st
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

def get_pdf_text(pdf_docs):
	text = ""

	for pdf in pdf_docs:
		pdf_reader = PdfReader(pdf)

		for page in pdf_reader.pages:
			text += page.extract_text() or ""

	return text

def get_text_chunks(text):
	text_splitter=RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
	chunks=text_splitter.split_text(text)
	return chunks

def get_vector_store(text_chunks):
	# embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
	embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
	vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
	vector_store.save_local("faiss_index")

def get_conversational_chain():
	prompt_template = """
    Answer the question as detailed as possible from the provided context.
    If the answer is not available in the provided context, say:
    "answer is not available in the context"

    Do not provide information that is not present in the context.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
	model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
	prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
	chain = prompt | model
	# chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
	return chain


def user_input(user_question):
	# embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
	embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
	nex_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
	docs = nex_db.similarity_search(user_question)
	chain = get_conversational_chain()
	context = "\n\n".join(doc.page_content for doc in docs)
	response = chain.invoke(
		{"context":context, "question": user_question}
		# return_only_outputs=True
	)
	# print(response)
	st.write("Reply: ", response.content)
	# ["output_text"])


def main():
	st.set_page_config("Chat With Multiple PDF")
	st.header("Chat with multiple PDF using Gemini.....")
	user_question = st.text_input("Ask a Question from the PDF Files", key="user_question")
	if user_question:
		user_input(user_question)
	with st.sidebar:
		st.title("Menu:")
		pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process", type=["pdf"], accept_multiple_files=True)

		if st.button("Submit & Process"):
			for pdf in pdf_docs:
				st.write("Name:", pdf.name)
				st.write("Type:", type(pdf))
			# 	st.write("Size:", len(pdf))
			with st.spinner("Processing...", show_time=True):
				raw_text = get_pdf_text(pdf_docs)
				text_chunks = get_text_chunks(raw_text)
				get_vector_store(text_chunks)
				st.success("Done")


if __name__ == "__main__":
	main()