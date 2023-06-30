from typing import Dict
import json
from langchain.llms import PromptLayerOpenAI
import promptlayer
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
import os
from dotenv import load_dotenv
load_dotenv()


PROMPT_LAYER_API_KEY= os.environ['PROMPT_LAYER_API_KEY']
OPEN_API_KEY=os.environ['OPEN_AI_KEY']
FILE_PATH='./qa_5star_feedback_data.json'

def get_prompts(question:str,correct_answer:str,new_answer:str):
    human_message_prompt = f'''Rate how similar these two answers are. Correct_answer:{correct_answer}, New_answer:{new_answer} .'''
    system_message_prompt = f'''
Compare the two answers provided for this question: {question} and provide output in this json format.

Follow these instructions while providing output.
1. Provide a rating out of five for how similar the two answers are.
2. Output should be in this json format - 
---
    {{
    "answer_similarity": "Rate how similar provided new answer is to provided answer",
    "reason": "Reason for rating the similarity."
    }}
----
'''
    return {'human_message_prompt':human_message_prompt,'system_message_prompt':system_message_prompt}



def get_data_from_file(file_path) -> Dict:
    with open(file_path, 'r') as file:
        json_data = json.load(file)

    json_object = json_data
    # Now you can work with the JSON object
    print(json_object)
    return json_object

def rate_similarity():
    promptlayer.api_key = PROMPT_LAYER_API_KEY
    chat = PromptLayerOpenAI(temperature=0.2, openai_api_key=OPEN_API_KEY,verbose=True,
                            streaming=False, pl_tags=["answer-similarity"])
    file_data=[]
    json_object = get_data_from_file(FILE_PATH)
    correct_answer = json_object[0]['answer']
    question = json_object[0]['question']
    new_answer ="""DES stands for Data Encryption Standard. It is a symmetric key algorithm used for encrypting and decrypting data. DES was developed by IBM in the 1970s and was adopted as a federal standard in the United States. It uses a 56-bit key to encrypt data in blocks of 64 bits.

DES operates through a series of rounds, each consisting of several steps including permutation, substitution, and XOR operations. These steps are repeated multiple times to ensure the security of the encrypted data.

Despite its historical significance, DES is now considered to be relatively weak due to advances in computing power. It is vulnerable to brute-force attacks, where an attacker tries all possible keys until the correct one is found. As a result, DES is no longer recommended for use in modern cryptographic systems.

In the late 1990s, the Advanced Encryption Standard (AES) was introduced as a replacement for DES. AES is a more secure and efficient encryption algorithm that has become the de facto standard for encryption in many applications and industries."""

    prompts_content = get_prompts(new_answer=new_answer,correct_answer=correct_answer,question=question)
    print(prompts_content)
    resp = chat.predict_messages([HumanMessage(content=prompts_content['human_message_prompt']),
                                  SystemMessage(content=prompts_content['system_message_prompt']),
                                  AIMessage(content='You are an AI assisstant that compares two answers of given question and rates how similar two answers are. You always provide output in json format ')
                                  ])
    file_single_obj ={
        'question':question,
        'correct_answer':correct_answer,
        'new_answer': new_answer
    }
    # file_single_obj['answer_comparison'] = resp.content
    #
    #
    # file_data.append(file_single_obj)
    print('RESPONSE : ',resp.content)


rate_similarity()