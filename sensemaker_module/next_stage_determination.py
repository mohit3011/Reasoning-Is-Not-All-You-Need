from message_utility_checker import check_message_ulitity
from stage_info import *
from utils.llm_response_getter import get_open_ai_response, get_deep_seek_response
from message_to_fact_convertor import convert_message_to_facts, indices_of_matching_facts_count

def next_stage_determination(current_stage, current_message, patient_facts, doctor_memory, counter, fact_obj_element, stage_obj_element, max_token, temperature, threshold):
    current_stage_iteration = counter
    MAX_ITERATIONS = 4
    current_stage_name = stage_number_to_name_dict[current_stage]
    potential_next_stage_name = stage_number_to_name_dict[current_stage+1]

    message_facts = convert_message_to_facts(current_message, fact_obj_element, max_token, temperature)
    matched_facts_indices = indices_of_matching_facts_count(message_facts, patient_facts, fact_obj_element, max_token, temperature)
    if len(matched_facts_indices)>0:
        for index in matched_facts_indices:
            patient_facts.append(message_facts[index])
    
    next_stage_determination_system_prompt  = ""

    system_prompt =  f'''
Task: 
Given the current patient message (PATIENT_MESSAGE) a list of facts about the patient (PATIENT_FACTS) and a list of statements previously made by you (YOUR_MEMEORY). Determine whether the conversation should remain in the current stage ({current_stage_name}) or transition to the next stage ({potential_next_stage_name}).\
If you decide to stay in the current stage then your OUTPUT_STAGE should be 'STAYCURRENTSTAGE' and if you determine to transition to the next stage then your output should be 'MOVENEXTSTAGE'.

Return Format:
OUTPUT_REASONING: <your reasoning for the stage determination>
OUTPUT_CONFIDENCE: <your confidence score to transition to the next stage>
OUTPUT_STAGE: <MOVENEXTSTAGE or STAYCURRENTSTAGE>

Guidelines:
- Refer to POTENTIAL_NEXT_STAGE_REASONING and then reach your conclusion.
- Before determining if you should stay in the same stage or transition to the next stage, you should generate a step-by-step reasoning (OUTPUT_REASONING) for your conclusion.
- You should also generate a score between 1 and 10 (OUTPUT_CONFIDENCE) indicating your confidence in transitioning to the next stage, if the score is between 1 and 3, you should definately stay in the current stage, if the score is between 4 and 6, then you should stay in the stage for one or two more turns, and if the score is 7 or above then you should move to the next stage.  
- The conversation should remain in the current stage if the user has not yet fully engaged with or completed its objectives.
- The conversation should move to the next stage only when the current stage has been meaningfully completed, ensuring a natural transition.

Warnings:
- Do not keep the conversation stuck in the same stage for multiple iterations unless necessary. If progression is unclear, consider whether the user is engaging sufficiently before deciding.'''
    
    next_stage_reasoning = {1: "The next stage would be 'Gathering Information' because an intial relationship between you and the patient has been established. Move on when the 'Fostering the Relationship' stage has provided a welcoming space and the patient starts to openly describe their concerns, feelings, or challenges. If they seem hesitant or reserved, stay in 'Fostering the Relationship' longer to encourage sharing.",
                                2: "The next stage would be 'Providing Information' only when you have received enough information from the patient about their current condition and symptoms for you to make a diagnosis. If you feel you need more time to gather information to make a confident diagnosis, stay in 'Gathering Information' longer.",
                                3: "You should move to the next stage which is 'Decision Making', NO MATTER WHAT.",
                                4: "The next stage would be 'Responding to Emotions' because the patient has understood the lifestyle and non-clinical suggestions made by you to alleviate their current condition. Move forward from the 'Decision Making' stage when the patient has acknowledged your suggestions. If their responses suggest they still need more clarity or direction, stay in 'Decision Making' to provide additional support.",
                                5: "The next stage would be 'exit' because the conversation has reached its end. Move forward from the 'Responding to Emotions' when you validated their emotions with an empathtic reponse and the patient has replied with an affirmative message. Do not focus on coping mechanisms in this stage."
                            }
    
    user_prompt = f'''POTENTIAL_NEXT_STAGE_REASONING: {next_stage_reasoning[current_stage]}
PATIENT_MESSAGE: {current_message}
PATIENT_FACTS: {patient_facts}
YOUR_MEMORY: {doctor_memory}'''

    next_stage_determination_system_prompt = system_prompt + user_prompt
    message_list = []
    message_list.append({'role': 'system', 'content': next_stage_determination_system_prompt})
    
    if 'deepseek' in stage_obj_element['model-name']:
        system_message_llm = get_deep_seek_response(stage_obj_element, message_list, max_token, stage_obj_element['model-name'], temperature, stage_obj_element['deployment_id'])
    else:  
        system_message_llm = get_open_ai_response(stage_obj_element, message_list, max_token, stage_obj_element['model-name'], temperature, stage_obj_element['deployment_id'])    
    #print("System Message: ", system_message_llm, flush = True)
   
    response = system_message_llm.split('OUTPUT_STAGE:')[-1].strip()
    
    if current_stage_iteration == MAX_ITERATIONS:
        counter = 0
        return current_stage+1, counter, patient_facts
    if response.startswith('MOVENEXTSTAGE'):
        counter = 0
        return current_stage+1, counter, patient_facts
    elif response.startswith('STAYCURRENTSTAGE'):
        counter+=1
        return current_stage, counter, patient_facts
    else:
        print("Invalid Response from Next Stage Determination:", response)
        print("Full LLM Response:", system_message_llm)