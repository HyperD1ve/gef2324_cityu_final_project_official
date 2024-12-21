# gef2324_cityu_final_project
The final project of the CityU GEF 2023-2024 GenAI OSALP course

## Streamlit
You may run the app by running
`cd streamlit`
`cd test_repo_1`
`streamlit run app.py`
note that because the JSON file containing the Firebase key is not in this repository, it won't be possible for any user to log in right now.

## RAG Code
It involves test code for question generation.
You can run it by 
`cd rag`
then
`python final_langchain.py` or `python zephur.py`
Note that in final_langchain.py, a Hugging Face model (meta-llama/Llama-3.2-3B) is used, and the Hugging Face API key has been removed. Of course, once the model has been downloaded locally, any subsequent uses no longer require the key, but that has not been done.

final_langchain.py is a half-completed file with separate question generation and answering functions.

and zephur.py is a completed file for question-answer pair generation