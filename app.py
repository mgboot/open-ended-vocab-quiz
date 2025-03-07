import streamlit as st
import json
from main import model, build_prompt_from_name, evaluate_answers

st.title("Vocabulary Quiz")

# Initialize session state variables
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "entities" not in st.session_state:
    st.session_state.entities = None
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "student_answers" not in st.session_state:
    st.session_state.student_answers = []
if "quiz_completed" not in st.session_state:
    st.session_state.quiz_completed = False
if "evaluation_results" not in st.session_state:
    st.session_state.evaluation_results = []
# Initialize quiz parameters
if "quiz_params" not in st.session_state:
    st.session_state.quiz_params = {
        "language": "",
        "level": "",
        "number": ""
    }

# Function to detect if text is primarily RTL
def is_rtl(text):
    # Arabic Unicode block range (0600-06FF)
    rtl_chars = 0
    for char in text:
        if '\u0600' <= char <= '\u06FF' or '\u0750' <= char <= '\u077F' or '\u08A0' <= char <= '\u08FF':
            rtl_chars += 1
    
    # If more than 30% of characters are RTL, consider it an RTL text
    return rtl_chars > (len(text) * 0.3)

# Function to display text with proper directionality
def display_with_direction(text, strong=False):
    if is_rtl(text):
        if strong:
            st.markdown(f'<p dir="rtl"><strong>{text}</strong></p>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p dir="rtl">{text}</p>', unsafe_allow_html=True)
    else:
        if strong:
            st.markdown(f'<p dir="ltr"><strong>{text}</strong></p>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p dir="ltr">{text}</p>', unsafe_allow_html=True)

# Function to start the quiz
def start_quiz():
    # Store quiz parameters in session state
    st.session_state.quiz_params = {
        "language": st.session_state.language,
        "level": st.session_state.level,
        "number": st.session_state.number
    }
    
    vars = st.session_state.quiz_params.copy()
    prompt = build_prompt_from_name("generate_sentences", vars)
    
    with st.spinner("Generating quiz questions..."):
        response = model.invoke(prompt)
        st.session_state.entities = json.loads(response.content)
        st.session_state.quiz_started = True
        st.session_state.current_question = 0
        st.session_state.student_answers = []
        st.session_state.quiz_completed = False
        st.session_state.evaluation_results = []

# Function to submit answer and move to next question
def submit_answer():
    st.session_state.student_answers.append(st.session_state.current_answer)
    st.session_state.current_question += 1
    
    # Check if quiz is complete
    if st.session_state.current_question >= len(st.session_state.entities):
        st.session_state.quiz_completed = True
        evaluate_quiz()

# Function to evaluate all answers at the end
def evaluate_quiz():
    # Use stored quiz parameters instead of direct session state access
    vars = st.session_state.quiz_params.copy()
    evaluation_results = []
    
    with st.spinner("Evaluating your answers..."):
        for entity in st.session_state.entities:
            question_vars = vars.copy()
            question_vars['sentence'] = entity['sentence']
            question_vars['original_answer'] = entity['answer']
            question_vars['student_answer'] = st.session_state.student_answers[entity['id']]

            eval_prompt = build_prompt_from_name("evaluate_answer", question_vars)
            
            response = model.invoke(eval_prompt)
            evaluation_results.append({
                'question': entity['sentence'],
                'correct_answer': entity['answer'],
                'student_answer': st.session_state.student_answers[entity['id']],
                'feedback': response.content
            })
        
        st.session_state.evaluation_results = evaluation_results

# Quiz setup screen
if not st.session_state.quiz_started:
    st.header("Quiz Setup")
    
    st.text_input("Target Language:", key="language")
    st.text_input("Difficulty Level:", key="level")
    st.text_input("Number of Questions:", key="number")
    
    if st.button("Start Quiz"):
        start_quiz()
        st.rerun()

# Quiz in progress
elif st.session_state.quiz_started and not st.session_state.quiz_completed:
    current_entity = st.session_state.entities[st.session_state.current_question]
    
    # Display current quiz parameters
    st.caption(f"Language: {st.session_state.quiz_params['language']}, Level: {st.session_state.quiz_params['level']}")
    
    st.header(f"Question #{current_entity['id']+1}")
    st.write("Supply an appropriate word for the following sentence:")
    
    # Use directional display for the sentence
    display_with_direction(current_entity['sentence'])
    
    # Add container with appropriate direction for input
    is_rtl_lang = is_rtl(st.session_state.quiz_params['language'])
    if is_rtl_lang:
        st.markdown('<div dir="rtl">', unsafe_allow_html=True)
        st.text_input("Your answer:", key="current_answer")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.text_input("Your answer:", key="current_answer")
    
    if st.button("Submit Answer"):
        submit_answer()
        st.rerun()

# Quiz completed, show results
else:
    st.header("Quiz Results")
    
    # Display quiz parameters in results
    st.caption(f"Language: {st.session_state.quiz_params['language']}, Level: {st.session_state.quiz_params['level']}")
    
    for i, result in enumerate(st.session_state.evaluation_results):
        st.subheader(f"Question #{i+1}")
        
        # Use directional display for sentences and answers
        st.write("**Sentence:**")
        display_with_direction(result['question'])
        
        st.write("**Your answer:**")
        display_with_direction(result['student_answer'])
        
        st.write("**Correct answer:**")
        display_with_direction(result['correct_answer'])
        
        st.write("**Feedback:**")
        display_with_direction(result['feedback'])
        
        st.divider()
    
    if st.button("Start New Quiz"):
        st.session_state.quiz_started = False
        st.rerun()
