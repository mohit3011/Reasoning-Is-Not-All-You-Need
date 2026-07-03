from utils.llm_response_getter import get_open_ai_response, get_deep_seek_response
from stage_info import stage_number_to_name_dict, stage_definition_dict, stage_examples_dict
from utils.message_generation_system_prompts import *


def get_doctor_message(current_stage, current_message, patient_facts, sense_maker_memory, obj_element, max_token, temperature):
    current_stage_name = stage_number_to_name_dict[current_stage]
    current_stage_definition = stage_definition_dict[current_stage_name]
    current_stage_examples = stage_examples_dict[current_stage_name]

    sense_maker_memory_string = ""
    for i in range(len(sense_maker_memory)):
        sense_maker_memory_string += f'''{str(i+1)}. {sense_maker_memory[i]}\n'''

    patient_facts_string = ""
    for i in range(len(patient_facts)):
        patient_facts_string += f'''{str(i+1)}. {patient_facts[i]}\n'''

    current_stage_examples_string = ""
    for i in range(len(current_stage_examples)):
        current_stage_examples_string += f'''{str(i+1)}. {current_stage_examples[i]}\n'''

    if current_stage_name == 'Fostering the Relationship':
        system_prompt = get_fostering_relationship_system_prompt(sense_maker_memory_string, patient_facts_string, current_stage_definition, current_stage_examples_string)
    elif current_stage_name == 'Gathering Information':
        system_prompt = get_gathering_information_system_prompt(sense_maker_memory_string, patient_facts_string, current_stage_definition, current_stage_examples_string)
    elif current_stage_name == 'Providing Information':
        system_prompt = get_providing_information_system_prompt(sense_maker_memory_string, patient_facts_string, current_stage_definition, current_stage_examples_string)
    elif current_stage_name == 'Decision Making':
        system_prompt = get_decision_making_system_prompt(sense_maker_memory_string, patient_facts_string, current_stage_definition, current_stage_examples_string)
    elif current_stage_name == 'Responding to Emotions':
        system_prompt = get_responding_to_emotions_system_prompt(sense_maker_memory_string, patient_facts_string, current_stage_definition, current_stage_examples_string)
    elif current_stage_name == 'Exit':
        system_prompt = get_exit_system_prompt(sense_maker_memory_string, patient_facts_string, current_stage_definition, current_stage_examples_string)


    user_prompt = f'''USER_MESSAGE: {current_message}'''
    
    message_list = []
    message_list.append({'role': 'system', 'content': system_prompt})
    message_list.append({'role': 'user', 'content': user_prompt})
    if 'deepseek' in obj_element['model-name']:
        system_message_llm = get_deep_seek_response(obj_element, message_list, max_token, obj_element['model-name'], temperature, obj_element['deployment_id'])
    else:
        system_message_llm = get_open_ai_response(obj_element, message_list, max_token, obj_element['model-name'], temperature, obj_element['deployment_id'])    # print("System Message Stage: ", system_message_llm)
    # print("System Message: ", system_message_llm_facts, flush = True)
    #system_message_llm = system_message_llm.split('OUTPUT_MESSAGE:')[-1].strip()

    #print("System Message: ", system_message_llm)

    '''if current_stage_name == 'Providing Information':
        responses = [system_message_llm.split('DIAGNOSIS:')[-1].strip()]
        return responses'''
    responses = ' '.join(system_message_llm.split('OUTPUT_MESSAGE:')[1:])
    responses = responses.split('#')[1:]
    final_messages = []
    for response in responses:
        message = response.strip()
        final_messages.append(message)
    
    return final_messages