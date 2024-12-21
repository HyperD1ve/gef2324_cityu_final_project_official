import streamlit as st
import time
import datetime

import cv2
import imageio
import os
# import threading

from emotion_cv.emotion2 import Get_Confidence

#placeholder element, like a div, that holds the video
frame_placeholder = st.empty()

#function that initialises the stream
def webcam_stream(output_file):
    reader = imageio.get_reader('<video0>', 'ffmpeg')
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec for .mp4 files
    if st.session_state.video:
        out = cv2.VideoWriter(output_file, fourcc, 30.0, (640, 480))  # 20 FPS, 640x480 resolution
        return reader, out
    return reader, None



#specify output directory of the file
output_dir = 'pages/recordings'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
output_file = os.path.join(output_dir, f'{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.mp4')  # Output file name

#stop the recording and release the resources
def stop_recording():
    if 'reader' in st.session_state:
        if st.session_state.out:
            st.session_state.out.release()
        st.session_state.reader.close()
        del st.session_state.reader
        del st.session_state.out 
        del st.session_state.record
        del st.session_state.video
# thread = threading.Thread(target=webcam_stream, args=(frame_placeholder, output_file, st.session_state.record if "record" in st.session_state else False))
# thread.start()



st.title("Questions")
#questions stores each question, the options, and the answer index and topic
questions = [("What's 1 + 1?", ["1", "2", "3"], 1, "Number System"),("What's 1 + 2?", ["1", "2", "3"], 2, "Number System"),("What's 2 - 1?", ["1", "2", "3"], 0, "Number System"),]
n = len(questions)

#initialise session variables for a test
if "stu_answers" not in st.session_state:
    st.session_state.stu_answers = [(None, False)] * n
elif len(st.session_state.stu_answers) == 0:
    st.session_state.stu_answers = [(None, False)] * n
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
    # st.session_state.completed = False
if 'confidence_values' not in st.session_state:
    st.session_state.confidence_values = {'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 0, 'sad': 0, 'surprise': 0, 'neutral': 0}
if 'avg_confidence_values' not in st.session_state:
    st.session_state.avg_confidence_values = [] * n


#display one question
def question(question, options, a_index, topic): 
    st.markdown(question)
    q_index = st.session_state.question_index
    answer = st.radio("Your answer", options, index=st.session_state.stu_answers[q_index][0], key = q_index)
    
    buttons = st.empty()
    with buttons.container():
        if answer is not None: 
            answer_index = options.index(answer) 
            st.session_state.stu_answers[q_index] = (answer_index, answer_index == a_index, topic)
            # Call Get_Confidence when navigating questions
            if st.session_state.record:

                emotion = max(st.session_state.confidence_values, key=st.session_state.confidence_values.get)
                

                st.session_state.avg_confidence_values[st.session_state.question_index] = emotion
                st.session_state.confidence_values = {'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 0, 'sad': 0, 'surprise': 0, 'neutral': 0}
                print(st.session_state.confidence_values)

        if q_index > 0 and st.button("Back", key = f'{q_index}_b'):
            st.session_state.question_index -= 1
            st.rerun()
            return 1
        elif q_index < n - 1 and st.button("Next", key = f'{q_index}_n'):
            st.session_state.question_index += 1
            st.rerun()
            return 2
        elif q_index == n - 1 and st.button("Submit", key = f'{q_index}_n'):
            buttons.empty() 
            st.session_state.question_index += 1
            st.rerun()
            return 3 
    return 0
            

# Main logic to display questions one by one
if st.session_state.question_index < n:
    current_question = questions[st.session_state.question_index]
    completed = question(current_question[0], current_question[1], current_question[2],current_question[3])
    print(st.session_state.question_index)

        
#if you have completed all questions 
if st.session_state.question_index >= n:
    #store questions for results page
    st.session_state.questions = questions
    st.write("You have completed all the questions!")
    stop_recording()
    placeholder = st.empty()
    placeholder.progress(0, "loading")
    time.sleep(0.6)
    placeholder.progress(50, "loading")
    time.sleep(0.3)
    placeholder.progress(100, "loading")
    st.switch_page("pages/paper_results.py")


#calling the recording function
if 'reader' not in st.session_state:
    if st.session_state.record:
        st.session_state.reader, st.session_state.out = webcam_stream(output_file)

#display and update the video
while st.session_state.record:
    try: 
        # Read a frame from the webcam
        frame = st.session_state.reader.get_next_data()

        emotion,conf = Get_Confidence(frame)

        st.session_state.confidence_values[emotion] += conf

        # If frame is read correctly

        # Convert the frame from BGR to RGB (Streamlit uses RGB)
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Display the frame in the Streamlit app
        frame_placeholder.image(frame, channels="RGB", width=200, use_container_width=False)
        if st.session_state.video:
            st.session_state.out.write(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        time.sleep(0.05)
        if st.session_state.question_index >= n:
            print("end recording")
            stop_recording()
            break
    except Exception as e:
        print(f'error: {e}')
        st.warning(f'Error incurred: {e}')