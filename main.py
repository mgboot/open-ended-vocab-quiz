from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
import json
import os
import dotenv


dotenv.load_dotenv()

model = AzureChatOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
    openai_api_version="2023-05-15",
)

def build_prompt_from_name(prompt_name, variables):
    file_path = f"prompts/{prompt_name}"

    system_message = None
    user_message = None

    # Read system message from file
    with open(f"{file_path}/system.txt", 'r') as file:  
        system_message = file.read()    

    # Read user message from file
    with open(f"{file_path}/user.txt", 'r') as file:  
        user_message = file.read()    

    prompt_template = ChatPromptTemplate([
        ("system", system_message),
        ("user", user_message)
    ])
    
    return prompt_template.invoke(variables)

def run_quiz(entities):
    # Sort the entities by their ID number  
    sorted_entities = sorted(entities, key=lambda entity: entity['id'])  

    student_answers = []

    # Loop through the sorted entities and retrieve the sentence  
    for entity in sorted_entities: 
        print(f"Question #{entity['id']+1}")
        x = input(f"Supply an appropriate word for the following sentence:\n\n{entity['sentence']}\n\n")
        student_answers.append(x)
    return student_answers

def evaluate_answers(entities, vars, student_answers):

    print("Evaluating answers...\n")
    
    for entity in entities:
        question_vars = vars
        question_vars['sentence'] = entity['sentence']
        question_vars['original_answer'] = entity['answer']
        question_vars['student_answer'] = student_answers[entity['id']]

        eval_prompt = build_prompt_from_name("evaluate_answer", question_vars)
        
        response = model.invoke(eval_prompt)
        print(response.content)
        print()

    return None

def run_app(vars):

    #vars = {"language": input("Target language: "), "level": input("Difficulty level: "), "number": input("Number of questions: ")}
    prompt = build_prompt_from_name("generate_sentences", vars)

    response = model.invoke(prompt)

    entities = json.loads(response.content)  

    student_answers = run_quiz(entities)

    evaluate_answers(entities, vars, student_answers)

    return None

if __name__ == "__main__":
    vars = {"language": input("Target language: "), "level": input("Difficulty level: "), "number": input("Number of questions: ")}
    run_app(vars)