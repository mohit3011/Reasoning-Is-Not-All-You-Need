

def get_fostering_relationship_system_prompt(sense_maker_memory_string, patient_facts_string, current_stage_definition, current_stage_examples_string):
    
    fostering_relationship_system_prompt  = ""
    
    prompt_goal_part = f'''You are an expert sense-maker who helps the patients to make sense of their current clinical situation. Keeping the conversation's\
 current stage goal and example messages in mind (given by CURRENT_STAGE_GOAL and CURRENT_STAGE_EXAMPLES), list of facts already known about the patient (PATIENT_FACTS),\
 and the list of statements already made by you (YOUR_MEMORY), and the user's current message (USER_MESSAGE), your goal is to generate three plausible and logical messages to be said to the patient that you have not said yet.\
 You should first generate a reasoning for yourself and then generate the three messages. Your messages can be a question or a statement.'''

    prompt_output_part = f'''\n\nYour output should strictly be in the following format: OUTPUT_REASONING: <your step-by-step reasoning>\nOUTPUT_MESSAGE: <3 plausible messages to the patient each on a new line and starting with "# ">. Do not include other formatting.'''

    prompt_warning_part = f'''\n\nAll the three plausible messages should be different from each other. If you are asking a question in a message, then only ask one question at a time in that message. Your message should be concise and to the point.'''

    prompt_context_part = f'''\nYOUR_MEMORY:\n{sense_maker_memory_string}\nPATIENT_FACTS:\n{patient_facts_string}\nCURRENT_STAGE_GOAL:\n{current_stage_definition}\nCURRENT_STAGE_EXAMPLES:\n{current_stage_examples_string}'''

    fostering_relationship_system_prompt = prompt_goal_part + prompt_output_part + prompt_warning_part + prompt_context_part
    #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    #print("Fostering Relationship System Prompt: ", fostering_relationship_system_prompt)
    #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    return fostering_relationship_system_prompt


def get_gathering_information_system_prompt(sense_maker_memory_string, patient_facts_string, current_stage_definition, current_stage_examples_string):
    
    gathering_information_system_prompt  = ""
    
    prompt_goal_part = f'''You are an expert sense-maker who helps the patients to make sense of their current clinical situation. Keeping the conversation's current stage goal and example messages in mind (given by CURRENT_STAGE_GOAL and CURRENT_STAGE_EXAMPLES),\
 list of facts already known about the patient (PATIENT_FACTS), and the list of statements already made by you (YOUR_MEMORY), your goal is to generate three plausible and logical messages to be said to the patient that you have not said yet.\
 Before generating the message you should generate a step-by-step reasoning taking into account the facts you already know about the patient.\
 In your reasoning you should think about the possible diagnosis hypotheses, and then generate the three messages for the patient that helps in gathering more information to either confirm or reject the diagnosis hypotheses.'''

    prompt_output_part = f'''\n\nYour output should strictly be in the following format: OUTPUT_REASONING: <your step-by-step reasoning>\nOUTPUT_MESSAGE: <3 plausible messages to the patient each on a new line and starting with "# ">. Do not include other formatting.'''
    
    prompt_warning_part = f'''\n\nAll the three plausible messages should be different from each other. If you are asking a question in a message, then only ask one question at a time in that message. Your message should be concise and to the point.'''

    prompt_context_part = f'''\nYOUR_MEMORY:\n{sense_maker_memory_string}\nPATIENT_FACTS:\n{patient_facts_string}\nCURRENT_STAGE_GOAL:\n{current_stage_definition}\nCURRENT_STAGE_EXAMPLES:\n{current_stage_examples_string}'''

    gathering_information_system_prompt = prompt_goal_part + prompt_output_part + prompt_warning_part + prompt_context_part
    #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    #print("Gathering Information System Prompt: ", gathering_information_system_prompt)
    #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    return gathering_information_system_prompt


def get_providing_information_system_prompt(sense_maker_memory_string, patient_facts_string, current_stage_definition, current_stage_examples_string):
    
    providing_information_system_prompt  = ""
    
    prompt_goal_part = f'''You are an expert sense-maker who helps the patients to make sense of their current clinical situation. Keeping the conversation's current stage goal and example messages in mind (given by CURRENT_STAGE_GOAL and CURRENT_STAGE_EXAMPLES),\
 list of facts already known about the patient (PATIENT_FACTS), and the list of statements already made by you (YOUR_MEMORY), your goal is to provide the patient with the diagnosis and its explanation to the patient.\
 Before generating the diagnosis and explanation message you should generate a step-by-step reasoning for yourself taking into account the facts you already know about the patient.'''
    
    prompt_output_part = f'''\n\nYour output should strictly be in the following format: OUTPUT_REASONING: <your step-by-step reasoning>\nOUTPUT_MESSAGE: <3 plausible messages to the patient each on a new line and starting with "# ">. Do not include other formatting.'''

    prompt_warning_part = '''\n\nYou should always provide a diagnosis and if you cannot find a diagnosis your message should strictly be "I apologize but I am unable to diagnose you at the moment."'''

    prompt_context_part = f'''\nYOUR_MEMORY:\n{sense_maker_memory_string}\nPATIENT_FACTS:\n{patient_facts_string}\nCURRENT_STAGE_GOAL:\n{current_stage_definition}\nCURRENT_STAGE_EXAMPLES:\n{current_stage_examples_string}'''

    providing_information_system_prompt = prompt_goal_part + prompt_output_part + prompt_warning_part + prompt_context_part
    #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    #print("Providing Information System Prompt: ", providing_information_system_prompt)
    #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    return providing_information_system_prompt


def get_decision_making_system_prompt(sense_maker_memory_string, patient_facts_string, current_stage_definition, current_stage_examples_string):
    
    decision_making_system_prompt = ""
    
    prompt_goal_part = '''You are an expert sense-maker who helps the patients to make sense of their current clinical situation. Keeping the conversation's current stage goal and example messages in mind (given by CURRENT_STAGE_GOAL and CURRENT_STAGE_EXAMPLES),\
 list of facts already known about the patient (PATIENT_FACTS), and the list of statements already made by you (YOUR_MEMORY), your goal is to generate three plausible and logical messages to be said to the patient that you have not said yet.\
 You should first generate a reasoning for yourself and then generate the three messages. Your messages can be a question or a statement.'''

    prompt_output_part = f'''\n\nYour output should strictly be in the following format: OUTPUT_REASONING: <your step-by-step reasoning>\nOUTPUT_MESSAGE: <3 plausible messages to the patient each on a new line and starting with "# ">. Do not include other formatting.'''

    prompt_warning_part = f'''\n\nAll the three plausible messages should be different from each other. If you are asking a question in a message, then only ask one question at a time in that message. Your message should be concise and to the point.'''

    prompt_context_part = f'''\nYOUR_MEMORY:\n{sense_maker_memory_string}\nPATIENT_FACTS:\n{patient_facts_string}\nCURRENT_STAGE_GOAL:\n{current_stage_definition}\nCURRENT_STAGE_EXAMPLES:\n{current_stage_examples_string}'''

    decision_making_system_prompt = prompt_goal_part + prompt_output_part + prompt_warning_part + prompt_context_part
    #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    #print("Decision Making System Prompt: ", decision_making_system_prompt)
    #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    return decision_making_system_prompt


def get_responding_to_emotions_system_prompt(sense_maker_memory_string, patient_facts_string, current_stage_definition, current_stage_examples_string):
    
    responding_to_emotions_system_prompt  = ""
    
    prompt_goal_part = '''You are an expert sense-maker who helps the patients to make sense of their current clinical situation. Keeping the conversation's current stage goal and example messages in mind (given by CURRENT_STAGE_GOAL and CURRENT_STAGE_EXAMPLES),\
 list of facts already known about the patient (PATIENT_FACTS), and the list of statements already made by you (YOUR_MEMORY), your goal is to generate three plausible and logical messages to be said to the patient that you have not said yet.\
 You should first generate a reasoning for yourself and then generate the three messages.'''

    prompt_output_part = f'''\n\nYour output should strictly be in the following format: OUTPUT_REASONING: <your step-by-step reasoning>\nOUTPUT_MESSAGE: <3 plausible messages to the patient each on a new line and starting with "# ">. Do not include other formatting.'''

    prompt_warning_part = f'''\n\nAll the three plausible messages should be different from each other. If you are asking a question in a message, then only ask one question at a time in that message. Your message should be concise and to the point.'''

    prompt_context_part = f'''\nYOUR_MEMORY:\n{sense_maker_memory_string}\nPATIENT_FACTS:\n{patient_facts_string}\nCURRENT_STAGE_GOAL:\n{current_stage_definition}\nCURRENT_STAGE_EXAMPLES:\n{current_stage_examples_string}'''

    responding_to_emotions_system_prompt = prompt_goal_part + prompt_output_part + prompt_warning_part + prompt_context_part
    #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    #print("Responding to Emotions System Prompt: ", responding_to_emotions_system_prompt)
    #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    return responding_to_emotions_system_prompt


def get_exit_system_prompt(sense_maker_memory_string, patient_facts_string, current_stage_definition, current_stage_examples_string):
    
    exit_system_prompt  = ""
    
    prompt_goal_part = '''You are an expert sense-maker who helps the patients to make sense of their current clinical situation. Keeping the conversation's current stage goal and example messages in mind (given by CURRENT_STAGE_GOAL and CURRENT_STAGE_EXAMPLES),\
 list of facts already known about the patient (PATIENT_FACTS), and the list of statements already made by you (YOUR_MEMORY), your goal is to generate three plausible and logical messages to be said to the patient that you have not said yet.\
 You should first generate a reasoning for yourself and then generate the three messages.'''

    prompt_output_part = f'''\n\nYour output should strictly be in the following format: OUTPUT_REASONING: <your step-by-step reasoning>\nOUTPUT_MESSAGE: <3 plausible messages to the patient each on a new line and starting with "# ">. Do not include other formatting.'''

    prompt_warning_part = f'''\n\nAll the three plausible messages should be different from each other. If you are asking a question in a message, then only ask one question at a time in that message. Your message should be concise and to the point.'''

    prompt_context_part = f'''\nYOUR_MEMORY:\n{sense_maker_memory_string}\nPATIENT_FACTS:\n{patient_facts_string}\nCURRENT_STAGE_GOAL:\n{current_stage_definition}\nCURRENT_STAGE_EXAMPLES:\n{current_stage_examples_string}'''

    exit_system_prompt = prompt_goal_part + prompt_output_part + prompt_warning_part + prompt_context_part
    #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    #print("Exit System Prompt: ", exit_system_prompt)
    #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    return exit_system_prompt