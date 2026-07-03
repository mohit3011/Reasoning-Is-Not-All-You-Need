from utils.llm_response_getter import get_open_ai_response, get_deep_seek_response
import random

def check_doctor_message_redundancy(candidate_messages, sense_maker_memory, obj_element, max_token, temperature):
    
    candidate_messages_string = ""
    for i in range(len(candidate_messages)):
        candidate_messages_string += str(i+1) + '. ' + candidate_messages[i] + '\n'


    sense_maker_statement_string = ""
    for i in range(len(sense_maker_memory)):
        sense_maker_statement_string += str(i+1) + '. ' + sense_maker_memory[i] + '\n'


    prompt_goal_part = '''You are an expert sense-maker who helps the patients to make sense of their current clinical situation.\
 Given a list of statements already made by you (STATEMENT_MEMORY), and a list of candidate statements (CANDIDATE_STATEMENTS), your task is to identify if there are any redundant statements in the CANDIDATE_STATEMENTS.'''

    prompt_output_part = '''\n\nYour output should strictly follow the format: # <statement> : <'RedundantStatement' or 'RedundantNotStatement'>. Where statement presents one statement from CANDIDATE_STATEMENTS. Output the labels for each statement in CANDIDATE_STATEMENTS and keep the statement text as it is (do not change the words) and always start the line with '#'.'''

    prompt_warning_part = '''\n\nYou should not change the words of the statement, only add the label. Your output should have one statement and its label per line. Below are some additional instructions:\n
1. You should not add any new statement which was not present in the STATEMENT_MEMORY.\n
2. If a new statement in the CANDIDATE_STATEMENTS has a different phrasing but serves a similar context to any of the statements present in the STATEMENT_MEMORY, it should be considered 'RedundantStatement'.\n
3. Classification for each statement in CANDIDATE_STATEMENTS should be independent of other statements in the CANDIDATE_STATEMENTS.'''
    
    
    system_prompt = prompt_goal_part + prompt_output_part + prompt_warning_part
    #print("Message Redundancy Checker System Prompt: ", system_prompt)

    if len(sense_maker_memory) == 0:
        user_prompt = f'''\nCANDIDATE_STATEMENTS:\n{candidate_messages_string}\nSTATEMENT_MEMORY:\nNo statements made by the sense-maker yet.'''
    else:
    
        user_prompt = f'''\nCANDIDATE_STATEMENTS:\n{candidate_messages_string}\nSTATEMENT_MEMORY:\n{sense_maker_statement_string}'''

    #print("Message Redundancy Checker User Prompt: ", user_prompt)



    message_list = []
    message_list.append({'role': 'system', 'content': system_prompt})
    message_list.append({'role': 'user', 'content': user_prompt})
    system_message_llm_redundancy = get_open_ai_response(obj_element, message_list, max_token, obj_element['model-name'], temperature, obj_element['deployment_id'])    
    #print("Sense Maker Redundancy Checker Response: ", system_message_llm_redundancy)
    
    #print(system_message_llm_redundancy)
    # label_list = system_message_llm_redundancy.split("@@@")[1:]
    label_list = system_message_llm_redundancy.split("#")[1:]
    #label_list = re.findall(r'\d+\.\s*(.*?)(?=\s*\d+\.|$)', system_message_llm_redundancy, re.DOTALL)
    #label_list = [item.strip() for item in label_list]

    # print("Label List: ", label_list)
    potential_messages = []
    for i in range(len(label_list)):
        #print("Statement being checked: ", label_list[i])
        corresponding_label = label_list[i]
        if "RedundantNotStatement" in corresponding_label:
            #print(i, corresponding_label, candidate_messages)
            potential_messages.append(candidate_messages[i])

    if len(potential_messages)>0:
        #randomly select one of the potential messages
        selected_message = random.choice(potential_messages)
        return selected_message
    else:
        return "No New Message Generated"