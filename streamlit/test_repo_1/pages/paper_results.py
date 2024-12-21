import streamlit as st
import datetime
import pandas as pd

st.title("Test Results")

#Collect the test results into a pandas DataFrame
answer_structure = {"Topic": [], "Correct": [], "Emotion": []}
n = 3
correct = 0
emotion_count = 0

for i in range(n):
    answer_structure["Topic"].append(st.session_state.stu_answers[i][2])
    answer_structure["Correct"].append(st.session_state.stu_answers[i][1])
    if st.session_state.stu_answers[i][1] == True:
        correct += 1 
    answer_structure["Emotion"].append(st.session_state.confidence_values[i][0])
    emotion_count += st.session_state.confidence_values[i][1] 
    
df = pd.DataFrame(answer_structure)
df.index += 1

summary_statistics = {"Percentage": correct / n, "Average Confidence": emotion_count / n}

#display test results here
st.markdown("test results here")
st.table(df)
st.table(summary_statistics)
if "student_data" not in st.session_state or st.session_state.student_data is None:
    st.session_state.student_data = []

if st.button("Return to user page"):
    st.session_state.student_data.append((datetime.datetime.now().strftime("%Y%m%d_%H%M"), answer_structure, summary_statistics))
    del st.session_state.questions
    del st.session_state.question_index
    # st.session_state.completed = 0
    del st.session_state.stu_answers
    del st.session_state.difficulty
    del st.session_state.topic
    del st.session_state.test_length
    del st.session_state.confidence_values
    st.switch_page("pages/user.py")