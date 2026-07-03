from utils.llm_response_getter import get_open_ai_response
import re

def convert_message_to_facts(current_message, obj_element, max_token, temperature):
    #prompt LLM to convert current_message to facts

    
    prompt_goal_part = f'''You are given a message provided by the patient as USER_MESSAGE, you task is to extract explicity stated atomic facts about the patient from the message.\
 Here, an atomic fact is defined as a new information provided by the patient which can increase your holistic understanding of the patient's condition.\
 Each atomic fact should carry an entirely different piece of explicitely stated fact, and should be independent of other atomic facts in the list.'''

    prompt_output_part = '''\n\nYour output should strictly be a list of atomic facts, with each item starting with "# ". Do not include other formatting. Additionaly, each of the atomic facts in the list should be in third person narration.'''

    prompt_warning_part = '''\n\nKeep in mind that each atomic fact is different from other atomic facts in the list. Do not add any new fact which was not present in the USER_MESSAGE.'''

    system_prompt = prompt_goal_part + prompt_output_part + prompt_warning_part
    #print("System Prompt for fact extraction: ", system_prompt)
    
    user_prompt = f'''\n\nUSER_MESSAGE: {current_message}
\nATOMIC_FACTS:
    '''

    message_list = []
    message_list.append({'role': 'system', 'content': system_prompt})
    message_list.append({'role': 'user', 'content': user_prompt})
    system_message_llm_facts = get_open_ai_response(obj_element, message_list, max_token, obj_element['model-name'], temperature, obj_element['deployment_id'])    # print("System Message: ", system_message_llm_facts, flush = True)
    #print("Extracted Facts: ", system_message_llm_facts)
    result = system_message_llm_facts.split("#")[1:]
    #print("Splitted Result: ", result)
    return [j.strip() for j in result]



def indices_of_matching_facts_count(facts, patient_facts, obj_element, max_token, temperature):
    new_fact_indices = []

    prompt_goal_part = f'''You are an expert fact matching agent. You are given a list of NEW_FACTS about a patient, and a list of already present facts in MEMORY_OF_PATIENT_FACTS.\
 Your task is to analyze if facts listed in NEW_FACTS list are 'FactPresent' or 'FactNotPresent' in MEMORY_OF_PATIENT_FACTS. For this task you take each fact from NEW_FACTS list one by one and check if it is present in MEMORY_OF_PATIENT_FACTS or not.\
 For this checking you should look at the facts in terms of their meaning and context and not the exact words. The classification for each NEW FACT should be independent of other NEW_FACTS.'''

    prompt_output_part = '''\n\nYour output should strictly follow the format: # <fact> : <'FactNotPresent' or 'FactPresent'>. Where fact presents one fact from NEW_FACTS. Output the labels for each fact in NEW_FACTS and keep the fact text as it is (do not change the words).'''

    prompt_warning_part = '''\n\nYou should not change the words of the fact, only add the label (either 'FactPresent' or 'FactNotPresent'). Your output should have one fact and its label per line.'''

    system_prompt = prompt_goal_part + prompt_output_part + prompt_warning_part

    #print("System Prompt for fact matching: ", system_prompt)
    #print("Patient Facts: ", patient_facts)

    user_prompt = f'''\nNEW_FACTS:\n'''
    for i in range(len(facts)):
        user_prompt += f'''# {facts[i]}\n'''

    user_prompt += f'''\nMEMORY_OF_PATIENT_FACTS:\n'''
    for i in range(len(patient_facts)):
        user_prompt += f'''{i+1}. {patient_facts[i]}\n'''
    user_prompt += f'''\nANSWER:\n'''

    #print("User Prompt for fact matching: ", user_prompt)

    if len(facts)==0:
        return new_fact_indices
    
    message_list = []
    message_list.append({'role': 'system', 'content': system_prompt})
    message_list.append({'role': 'user', 'content': user_prompt})
    system_message_llm_facts = get_open_ai_response(obj_element, message_list, max_token, obj_element['model-name'], temperature, obj_element['deployment_id'])
    #print("LLM Response for fact matching: ", system_message_llm_facts)
    
    label_list = system_message_llm_facts.split("#")[1:]
    #print("Label List: ", label_list)
    for i in range(len(label_list)):
        #print("Fact being checked: ", facts[i])
        corresponding_label = label_list[i]
        if "FactNotPresent" in corresponding_label:
            new_fact_indices.append(i)
            #print("Index of the fact being added: ", i)
    #print("New Fact Indices: ", new_fact_indices)

    return new_fact_indices