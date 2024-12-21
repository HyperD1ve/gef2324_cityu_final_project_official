#a function for teachers
#allows them to select a student then view their data
#TBC if we will use LLM to generate a summary, or just show tabulated data

import streamlit as st
from menu import menu_with_redirect
from firebase_admin import firestore
import time
db = firestore.client()
import pandas as pd

#redirect to main page if not logged in
menu_with_redirect()

st.title("View student data")
with st.form("view_student_form"):
    s_id = st.text_input("Enter desired student ID")
    if st.form_submit_button("Fetch data"):
        student_ref = db.collection('data').document(s_id)
        student_doc = student_ref.get()
        if student_doc.exists:
            display = st.empty()
            student_info = student_doc.to_dict()
            display = st.success("Student data found!")
            time.sleep(1)
            display.empty()
            print(student_info) 
            for key in sorted(student_info):
                st.header(key)
                df = pd.DataFrame(student_info[key][0])
                df.index += 1
                st.table(df)
                st.table(student_info[key][1])
            #display the data / call a function to display the data
            #
            # 
        else:
            st.warning("Student data not found!")
            
#what can be done for data display:
#trend over time?
#strengths and weakness
#common emotion showed (fear? anxiety? doubt?)
#LLM generate a summary on the data?