#this file's purpose is to upload the student's data to Firebase.
#the user doesn't need to login for student (as they can do the papers and LLM when offline)
#but login is a must for teacher (as they only need to fetch data from cloud (Firebase))

import streamlit as st
from menu import menu_with_redirect
from firebase_admin import firestore
db = firestore.client()
# import datetime
import pandas as pd

#redirect to main page if not logged in
menu_with_redirect()

st.title("Upload your data to the cloud")
st.markdown("Upload the analysis data from all the papers you have done today.")



if "student_data" in st.session_state:
    for i in st.session_state.student_data:
            st.write(i[0])
            print(i[1])
            df = pd.DataFrame(i[1])
            df.index += 1 
            st.table(df)
            print(i[2])
            
            st.table(i[2])
    
    #put the analysis data to be uploaded here
    # upload_data = {"some-data": st.session_state.student_data}

    if st.button("Upload"):
        # current_time = datetime.datetime.now()
        # formatted_time = f'{current_time.year}-{current_time.month}-{current_time.day}'
        for i in st.session_state.student_data:
            data = {i[0]: (i[1], i[2])}
            db.collection('data').document(st.session_state.id).set(data)
        st.success("Data uploaded!", icon="🎉")
        # del st.session_state.student_data
    if st.button("Delete local data"):
        st.session_state.student_data = None
        del st.session_state["student_data"]
        st.rerun()
else:
    st.write("Sorry, there is no student data stored locally right now.")

