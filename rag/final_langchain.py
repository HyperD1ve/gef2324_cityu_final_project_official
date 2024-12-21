import streamlit as st
import tempfile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
# from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Replicate
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import torch
import os
import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../private')))
# from keys import * #never mind the warning, this code works. the sys code is to join the private folder to this directory in order to fetch the keys.py file. 

# Authenticate with Hugging Face Hub
from huggingface_hub import login
login("your_key_here")  # Replace with your token if not already logged in
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline, AutoModelForCausalLM,Trainer, TrainingArguments


load_dotenv()

os.environ['TRANSFORMERS_CACHE'] = "./my_custom_cache"

class MC:
    def __init__(self, question, choices, option,answer):
        self.question = question
        self.choices = choices
        self.option = option
        self.answer = answer


# Example usage
docs_question_pre = [
    MC(
        question="Mary sold two bags for $240 each. She gained 20% on one and lost 20% on the other. After the two transactions, Mary",
        choices="lost $20.;gained $10.;gained $60.;had no gain and no loss.",
        option="A",
        answer="lost $20."
    ),
    MC(
        question="Peter invests $P at the beginning of each month in a year at an interest rate of 6% per annum, compounded monthly. If he gets $10 000 at the end of the year, find P correct to 2 decimal places.",
        choices="806.63;829.19;833.33;882.18",
        option="A",
        answer="806.63"
    ),
    MC(
        question="John buys a vase for $1600. He then sells the vase to Susan at a profit of 20%. At what price should Susan sell the vase in order to have a profit of 20%? ",
        choices="$2240;$2304;$2400;$2500 ",
        option="B",
        answer="$2304"
    ),
    MC(
        question="In a company, 37.5% of the employees are female. If 60% of the male employees and 80% of the female employees are married, then the percentage of married employees in the company is ",
        choices="32.5%;45%;55%;67.5% ",
        option="D",
        answer="67.5% "
    ),
    MC(
        question="Susan sells two cars for $80 080 each. She gains 30% on one and loses 30% on the other. After the two transactions, Susan ",
        choices="loses $15840;gains $5544;gains $10296;has no gain and no loss",
        option="A",
        answer="loses $15840"
    ),
    MC(
        question="A sum of $50 000 is deposited at an interest rate of 8% per annum for 1 year, compounded monthly. Find the interest correct to the nearest dollar. ",
        choices="$4000;$4122;$143;$4150 ",
        option="D",
        answer="$4150 "
    ),
]

# prompt_template_questions = """
# You are an expert in creating practice questions based on study material.
# Your goal is to prepare a student for their exam. You do this by asking questions about the text below:

# ------------
# {text}
# ------------

# Create questions that will prepare the student for their exam. Make sure not to lose any important information.

# QUESTIONS:
# """

# PROMPT_QUESTIONS = PromptTemplate(template=prompt_template_questions, input_variables=["text"])

# refine_template_questions = """
# You are an expert in creating practice questions based on study material.
# Your goal is to help a student prepare for an exam.
# We have received some practice questions to a certain extent: {existing_answer}.
# We have the option to refine the existing questions or add new ones.
# (only if necessary) with some more context below.
# ------------
# {text}
# ------------

# Given the new context, refine the original questions in English.
# If the context is not helpful, please provide the original questions.

# QUESTIONS:
# """

# REFINE_PROMPT_QUESTIONS = PromptTemplate(
#     input_variables=["existing_answer", "text"],
#     template=refine_template_questions,
# )

fprompt = """
You are an expert in creating practice questions based on study material.
Your goal is to prepare a student for their exam. You do this by asking questions about the text below:

------------

"""
sprompt = """

------------

Create questions that will prepare the student for their exam. Make sure not to lose any important information.

Make sure there is only one correct choice and it is in the format [choice_A;choice_B;choice_C;choice_D].

Generate a string of response in the following format: \'Question: {generated_question}\nChoices: {generated_choices_for_question}\nCorrect option: {generated_correct_option}\nAnswer: {generated_answer}\'
"""

# Initialize Streamlit app
st.title('Question Answering Generator:books:')
st.markdown('<style>h1{color: orange; text-align: center;}</style>', unsafe_allow_html=True)
st.subheader('Built for Professionals,Teachers, Students')
st.markdown('<style>h3{color: pink;  text-align: center;}</style>', unsafe_allow_html=True)

# File upload widget
uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])

# Set file path
file_path = None

if torch.cuda.is_available():
    device = torch.device("cuda")
    print("Using GPU:", torch.cuda.get_device_name(0))
else:
    device = torch.device("cpu")
    print("GPU not available, using CPU.")

# functions
def load_question_generation_pipeline(data):
    docs_question_gen = data

    # Load the language model and tokenizer for question generation
    model_name = "meta-llama/Llama-3.2-3B"
    tokenizer = AutoTokenizer.from_pretrained(model_name,token=HUGGING_FACE_KEY)
    model = AutoModelForCausalLM.from_pretrained(model_name,token=HUGGING_FACE_KEY)
    model.to(device)
    # Set up the model pipeline for LangChain
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, temperature=0.01, top_p=1,max_new_tokens=500,truncation=True)
    # Save the model with safe_serialization=True
    model.save_pretrained("path_to_save_model", is_main_process=True, save_function=True, safe_serialization=True)
    # Run the question generation pipeline
    questions = []
    for doc in docs_question_gen:
        context = f"Question: {doc.question}\nChoices (Layout: ‘A;B;C;D’): {doc.choices}\nOption: {doc.option}\nAnswer: {doc.answer}"
        prompt = fprompt+context+sprompt
        generated_question = pipe(prompt)
        questions.append(generated_question)

    return questions

def generate_answers_using_transformers(docs_question_gen):
    # Initialize the question-answering pipeline
    model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    model.to(device)
    qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)
    # Save the model with safe_serialization=True
    model.save_pretrained("path_to_save_model", is_main_process=True, save_function=True, safe_serialization=True)
    # Initialize a list to store the generated answers
    generated_answers = []
    # Loop through the provided documents for answer generation
    for doc in docs_question_gen:
        # Extract the question from the document
        question = doc.question
        context = f"Choices (Layout: ‘A;B;C;D’): {doc.choices}\nOption: {doc.option}\nAnswer: {doc.answer}"

        # Generate answer using the question-answering pipeline
        answer = qa_pipeline(question=question, context=context)

        # Append the generated answer to the list
        generated_answers.append(answer)

    return generated_answers


# Check if a file is uploaded
if uploaded_file:
    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        file_path = temp_file.name

# Check if file_path is set
if file_path:
    # Load data from the uploaded PDF
    loader = PyPDFLoader(file_path)
    data = loader.load()

    # Combine text from Document into one string for question generation
    questions = load_question_generation_pipeline(docs_question_pre)

    # Initialize retrieval chain for answer generation
    answer_gen_chain = generate_answers_using_transformers(docs_question_pre)
    
     # Split generated questions into a list of questions
    # Answer each question and save to a file
    for q in question_list:
        st.write("Question: ", q)
        answer = "no answer" #answer_gen_chain[p]
        print(answer)
        st.write("Answer: ", answer)
        st.write("--------------------------------------------------\n\n")
        p+=1

    # Create a directory for storing answers
    answers_dir = os.path.join(tempfile.gettempdir(), "answers")
    os.makedirs(answers_dir, exist_ok=True)

    # Create a single file to save questions and answers
    qa_file_path = os.path.join(answers_dir, "questions_and_answers.txt")
    p = 0
    with open(qa_file_path, "w") as qa_file:
        # Answer each question and save to the file
        for idx, question in enumerate(question_list):
            answer = "no answer" #answer_gen_chain[p]
            qa_file.write(f"Question {idx + 1}: {question}\n")
            qa_file.write(f"Answer {idx + 1}: {answer}\n")
            qa_file.write("--------------------------------------------------\n\n")
            p+=1

    # Create a download button for the questions and answers file
    st.markdown('### Download Questions and Answers')
    st.download_button("Download Questions and Answers", qa_file_path)

# Cleanup temporary files
if file_path:
    os.remove(file_path)