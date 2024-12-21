import streamlit as st
#the purpose of this file is to generate a paper
#it should call paper.py with all the relevant arguments when complete

#this array should call from William's Topics Table.xlsx file, to obtain all the topics
TOPICS = ["Number System", "Percentages", "Functions and Graphs", "Exponential and Logarithmic Functions", "More about Polynomials", "More about Equations", "Rate, Ratio and Variations", "Sequences", "Inequalities and Linear Programming", "Mensuration", "Permutation and Combination", "More about Probability", "Measures of Dispersion", "Plane Geometry", "Locus", "Coordinates Geometry", "Trigonometry"]
selected = {}
st.session_state.record = False
st.session_state.video = False
st.session_state.difficulty = -1
st.session_state.topic = None
st.session_state.test_length = -1

st.title("Generate a paper")

with st.form("paper_form"):
    with st.container():
        st.header("Select topics")
        for i in TOPICS:
            selected[i] = st.checkbox(i)
        st.write("\n") 
    st.session_state.difficulty = st.slider("Difficulty", 0, 100)
    st.session_state.test_length = st.selectbox("Number of questions", [10, 15, 30])
    st.session_state.record = st.checkbox("Record Emotions") 
    st.session_state.video = st.checkbox("Save Video") 
    if st.form_submit_button("Begin"):
        st.switch_page("pages/paper.py")