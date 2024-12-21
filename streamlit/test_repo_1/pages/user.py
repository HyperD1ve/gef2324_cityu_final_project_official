import streamlit as st
from menu import menu_with_redirect
import pandas as pd

#redirect to main page if not logged in
menu_with_redirect()

username = st.session_state.user

st.title("User Information")
st.markdown(f"Hello, {username}!")
if st.session_state.role == "Student":
    st.header("Your performance")
    if "student_data" in st.session_state and st.session_state.student_data is not None:
        print(st.session_state.student_data)
        for i in st.session_state.student_data:
            st.write(i[0])
            print(i[1])
            df = pd.DataFrame(i[1])
            df.index += 1 
            st.table(df)
            print(i[2])
            
            st.table(i[2])
    else:
        st.write("Currently no local data stored!")
#display user data
#
#This could be in the same format as view.py,
#only difference is that the student can only view their own data, while teacher can pick any student.
