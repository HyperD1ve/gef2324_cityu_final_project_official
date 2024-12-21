# Install transformers from source - only needed for versions <= v4.34
# pip install git+https://github.com/huggingface/transformers.git
# pip install accelerate

import torch
from transformers import pipeline

if torch.cuda.is_available():
    device = torch.device("cuda")
    print("Using GPU:", torch.cuda.get_device_name(0))
else:
    device = torch.device("cpu")
    print("GPU not available, using CPU.")
prompt = """
You are an expert in creating practice questions based on study materials.

Your goal is to prepare students for their HKDSE Mathematics (Compulsary) exams. Below is a sample of real HKDSE Math (Compulsory) MCQ:

------------

Question: In a company, 37.5% of the employees are female. If 60% of the male employees and 80% of the female employees are married, 
then the percentage of married employees in the company is 

Choices (Layout: ‘A;B;C;D’): 32.5%;45%;55%;67.5% 

Option: D

Answer: 67.5%

Explanation: 
There are female and male employees in the company. Percentage of married female employees = (37.5%)*(80%) = 30%. 
Percentage of married male employees = (1-37.5%)*(60%) = 37.5%. So, the percentage of married employees in the company is 67.5%.

------------

Create questions that will prepare the student for their exam. Make sure not to lose any important information.

Make sure there is only one correct choice and it is in the format [choice_A;choice_B;choice_C;choice_D].

Topic: [Number system, percentages]
Difficulty (1-100): 50
Number of questions: 5

Generate a string of response in the following format: 
\'Question: {generated_question}\nChoices: {generated_choices_for_question}\n
Correct option: \n{generated_correct_option}\nAnswer: {generated_answer}\nExplanation: {generated_explanation}\'
"""
# We use the tokenizer's chat template to format each message - see https://huggingface.co/docs/transformers/main/en/chat_templating




pipe = pipeline("text-generation", model="HuggingFaceH4/zephyr-7b-alpha", torch_dtype=torch.bfloat16, device_map="auto")
messages = [
    {
        "role": "system",
        "content": "You are a helpful math learning assistant",
    },
    {"role": "user", "content": prompt},
]
prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
outputs = pipe(prompt, max_new_tokens=8192, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
print(outputs[0]["generated_text"])




# <|system|>
# You are a friendly chatbot who always responds in the style of a pirate.</s>
# <|user|>
# How many helicopters can a human eat in one sitting?</s>
# <|assistant|>
# Ah, me hearty matey! But yer question be a puzzler! A human cannot eat a helicopter in one sitting, as helicopters are not edible. They be made of metal, plastic, and other materials, not food!
