import sys
import os
import traceback
project_root = os.path.abspath("./doctor_module/")
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from langchain_openai import AzureChatOpenAI
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
import pandas as pd
import argparse

from next_stage_determination import next_stage_determination
from message_generator import get_doctor_message
from message_redundancy_checker import check_doctor_message_redundancy
from stage_info import stage_number_to_name_dict

from patient_module.patient_answer_generation import get_answer_gen_chain, get_unknown_answer_gen_chain
from patient_module.patient_fact_selection import get_fact_selection_chain
from patient_module.patient_module import get_patient_answer_v2, process_patient_case_study, get_patient_start_message

# for patient LLM
os.environ["OPENAI_MAX_RETRIES"] = "5"
os.environ["OPENAI_RETRY_MIN_SECONDS"] = "60"       
os.environ["OPENAI_RETRY_MAX_SECONDS"] = "300"       

def simulate_conversation(
    patient_info_facts,
    patient_info_vital_facts,
    intent_facts, 
    goal_facts, 
    sampled_mll, 
    sampled_personality,
    patient_llm,
    sensemaker_generation_llm,
    sensemaker_computation_llm,
    start_message="Hi, I'm here to get some advice regarding my health situation.",
    threshold=3,
    temperature=0.0,
    max_token_generation=1000,
    max_token_computation=500,
    verbose=True
):

    patient_fact_selection_chain = get_fact_selection_chain(patient_llm)
    patient_answer_gen_chain = get_answer_gen_chain(patient_llm)
    patient_unknown_answer_gen_chain = get_unknown_answer_gen_chain(patient_llm)

    doctor_memory = list(patient_info_vital_facts)
    patient_facts = []

    current_stage = 1
    counter = 0

    patient_fact_memory = {}
    next_stage = ""

    conversation = []
    for ind in range(100):

        if ind == 0:
            current_message = start_message
        else:
            current_message = get_patient_answer_v2(
                patient_fact_selection_chain,
                patient_answer_gen_chain,
                patient_unknown_answer_gen_chain,
                doctor_message, 
                current_stage, 
                patient_fact_memory, 
                patient_info_facts, 
                intent_facts, 
                goal_facts, 
                sampled_mll, 
                sampled_personality
            )

        if current_message == "exit":
            break
        
        if verbose:
            print("Patient:", current_message)
            print()
        ############################################### Stage Determination ###############################################

        if verbose:
            print("Current Stage", stage_number_to_name_dict[current_stage])
        if stage_number_to_name_dict[current_stage] == 'Providing Information':
            next_stage += 1
        else:
            if stage_number_to_name_dict[current_stage] != 'Exit':
                next_stage, counter, patient_facts = next_stage_determination(current_stage, current_message, patient_facts, doctor_memory, counter, sensemaker_computation_llm, sensemaker_generation_llm, max_token_computation, temperature, threshold)
            else:
                next_stage = current_stage

        if verbose:
            print("Next Stage", stage_number_to_name_dict[next_stage])
            print()

        ############################################### Message Generation ###############################################  

        candidate_messages = get_doctor_message(next_stage, current_message, patient_facts, doctor_memory, sensemaker_generation_llm, max_token_generation, temperature)
        new_sense_maker_message = check_doctor_message_redundancy(candidate_messages, doctor_memory, sensemaker_computation_llm, max_token_computation, temperature)

        if new_sense_maker_message == "No New Message Generated":
            if verbose:
                print("(no new message)")

            conversation.append({
                "role": "sense_maker",
                "message": "NO_NEW_MESSAGE_GENERATED",
                "stage": stage_number_to_name_dict[next_stage]
            })
            
            next_stage += 1
            if next_stage >= list(stage_number_to_name_dict.keys())[-1]:
                if verbose:
                    print('Exiting because reached', current_stage)
                break

            if verbose:
                print("Next Stage:", stage_number_to_name_dict[next_stage])
                print()

            candidate_messages = get_doctor_message(next_stage, current_message, patient_facts, doctor_memory, sensemaker_generation_llm, max_token_generation, temperature)
            new_sense_maker_message = check_doctor_message_redundancy(candidate_messages, doctor_memory, sensemaker_computation_llm, max_token_computation, temperature)
        
        doctor_message = new_sense_maker_message

        ############################################### Conversation History Update ###############################################

        doctor_memory.append(new_sense_maker_message)

        conversation.append({
            "role": "patient",
            "message": current_message,
            "stage": stage_number_to_name_dict[current_stage]
        })

        conversation.append({
            "role": "sense_maker",
            "message": new_sense_maker_message,
            "stage": stage_number_to_name_dict[next_stage]
        })

        current_stage = next_stage

        if verbose:
            print("Sensemaker:", new_sense_maker_message)
            print()

        if current_stage == list(stage_number_to_name_dict.keys())[-1]:
            if verbose:
                print('Exiting because reached', current_stage)
            break

    return conversation

def get_convo_string(conversation):
    conv = ""
    for c in conversation:
        conv += 'Stage: ' + c['stage'] + '\n'
        conv += c['role'].replace('_', '').capitalize() + ': ' + c['message'] + '\n\n'
    return conv

SAMPLED_PERSONALITIES = [
    {
        'Openness_score': 'HIGH', 
        'Conscientiousness_score': 'LOW', 
        'Extraversion_score': 'LOW', 
        'Agreeableness_score': 'LOW', 
        'Neuroticism_score': 'LOW'
    },
    {
        'Openness_score': 'LOW', 
        'Conscientiousness_score': 'HIGH', 
        'Extraversion_score': 'LOW', 
        'Agreeableness_score': 'LOW', 
        'Neuroticism_score': 'LOW'
    },
    {
        'Openness_score': 'LOW', 
        'Conscientiousness_score': 'LOW', 
        'Extraversion_score': 'HIGH', 
        'Agreeableness_score': 'LOW', 
        'Neuroticism_score': 'LOW'
    },
    {
        'Openness_score': 'LOW', 
        'Conscientiousness_score': 'LOW', 
        'Extraversion_score': 'LOW', 
        'Agreeableness_score': 'HIGH', 
        'Neuroticism_score': 'LOW'
    },
    {
        'Openness_score': 'LOW', 
        'Conscientiousness_score': 'LOW', 
        'Extraversion_score': 'LOW', 
        'Agreeableness_score': 'LOW', 
        'Neuroticism_score': 'HIGH'
    }
]

SAMPLED_MLL = [
    "Basic",
    "Advanced"
]

###############################################################################################
# CONFIGS

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--case_study_file', type=str, default='./data/medqa_filtering_for_mental_health_diagnosis_cases - medqa_filtering_for_mental_health_diagnosis_cases.csv',
                        help='Path to the case study CSV file')
    parser.add_argument('--start_ind', type=int, help='Start index')
    parser.add_argument('--end_ind', type=int, help='End index')
    parser.add_argument('--model', type=str, default='o1', help='Model name')
    parser.add_argument('--openai_api_endpoint', type=str, help='OpenAI API endpoint')
    parser.add_argument('--openai_api_key', type=str, help='OpenAI API key')
    parser.add_argument('--deepseek_api_endpoint', type=str, help='DeepSeek API endpoint')
    parser.add_argument('--deepseek_api_key', type=str, help='DeepSeek API key')
    parser.add_argument('--deepseek_model_name', type=str, help='DeepSeek model name')
    parser.add_argument('--output_file', type=str, help='Output file')

    return parser.parse_args()

args = parse_args()

CASE_STUDY_FILE = args.case_study_file
START_IND = args.start_ind
END_IND = args.end_ind
MODEL = args.model
OPENAI_API_ENDPOINT = args.openai_api_endpoint
OPENAI_API_KEY = args.openai_api_key
DEEPSEEK_API_ENDPOINT = args.deepseek_api_endpoint
DEEPSEEK_API_KEY = args.deepseek_api_key
DEEPSEEK_MODEL_NAME = args.deepseek_model_name
OUTPUT_FILE = args.output_file #f'./data/mh_conversations_o1_0_1_test.pkl'
SAVE_INTERVAL = 1

print("Running configuration:")
print(vars(args))
print(f"Saving output to {OUTPUT_FILE}")

###############################################################################################

azure_openai_llm_client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=OPENAI_API_ENDPOINT,
    api_key=OPENAI_API_KEY,
)

sensemaker_generation_o1_llm = {
    "openai_obj": azure_openai_llm_client,
    "deployment_id": "o1",
    "model-name": "o1",
}

sensemaker_computation_llm = {
    "openai_obj": azure_openai_llm_client,
    "deployment_id": "gpt-4o",
    "model-name": "gpt-4o",
}

azure_deepseek_llm_client = ChatCompletionsClient(
    endpoint=DEEPSEEK_API_ENDPOINT,
    credential=AzureKeyCredential(DEEPSEEK_API_KEY)
)

sensemaker_generation_deepseek_r1_llm = {
    "deep_seek_obj": azure_deepseek_llm_client,
    "deployment_id": DEEPSEEK_MODEL_NAME,
    "model-name": DEEPSEEK_MODEL_NAME,
}

patient_llm = AzureChatOpenAI(
    deployment_name="gpt-4o",
    model="gpt-4o",
    api_version="2024-12-01-preview",
    api_key=OPENAI_API_KEY,
    azure_endpoint=OPENAI_API_ENDPOINT,
    temperature=0,
    max_tokens=400,
    max_retries=5
)

if MODEL == 'o1':
    SENSEMAKER_GENERATION_LLM = sensemaker_generation_o1_llm
else:
    SENSEMAKER_GENERATION_LLM = sensemaker_generation_deepseek_r1_llm

threshold = 3
temperature = 0.0
max_token_generation = 15000
max_token_computation = 1000

patient_case_study_df = pd.read_csv(CASE_STUDY_FILE)
patient_case_study_df = patient_case_study_df[(patient_case_study_df['mental_health_classification'] == 'Yes')].reset_index(drop=True)

conv_objs = []

print("Starting conversation generation..")

for i, patient_case_study_obj in patient_case_study_df.iloc[START_IND:END_IND, :].iterrows():

    try:

        print("It:", i, "Case Study ID:", patient_case_study_obj['id'], flush=True)
        patient_data = patient_case_study_obj['clinical_case_study']

        patient_info_facts, patient_info_vital_facts, intent_facts, goal_facts = \
            process_patient_case_study(patient_data, patient_llm)

        for ind_personality, sampled_personality in enumerate(SAMPLED_PERSONALITIES, 1):
            print(f"\tPers: {ind_personality}/5", flush=True)
            for ind_mll, sampled_mll in enumerate(SAMPLED_MLL, 1):
                print(f"\t\tMLL: {ind_mll}/2", flush=True)
                start_message = get_patient_start_message(
                    patient_info_facts, 
                    intent_facts, 
                    sampled_personality, 
                    sampled_mll, 
                    patient_llm
                )

                conversation = simulate_conversation(
                    patient_info_facts,
                    patient_info_vital_facts,
                    intent_facts, 
                    goal_facts,
                    sampled_mll, 
                    sampled_personality,
                    patient_llm,
                    SENSEMAKER_GENERATION_LLM,
                    sensemaker_computation_llm,
                    start_message=start_message,
                    threshold=threshold,
                    temperature=temperature,
                    max_token_generation=max_token_generation,
                    max_token_computation=max_token_computation,
                    verbose=False
                )

                conv_df_obj = {
                    'id': patient_case_study_obj['id'],
                    'clinical_case_study': patient_data,
                    'patient_info_facts': patient_info_facts,
                    'patient_info_vital_facts': patient_info_vital_facts,
                    'intent_facts': intent_facts,
                    'goal_facts': goal_facts,
                    'sampled_personality_Openness_score': sampled_personality['Openness_score'],
                    'sampled_personality_Conscientiousness_score': sampled_personality['Conscientiousness_score'],
                    'sampled_personality_Extraversion_score': sampled_personality['Extraversion_score'],
                    'sampled_personality_Agreeableness_score': sampled_personality['Agreeableness_score'],
                    'sampled_personality_Neuroticism_score': sampled_personality['Neuroticism_score'],
                    'sampled_mll': sampled_mll,
                    'conversation_obj': conversation,
                }

                conv_objs.append(conv_df_obj)

                if len(conv_objs) % SAVE_INTERVAL == 0:
                    conv_df = pd.DataFrame(conv_objs)
                    conv_df.to_pickle(OUTPUT_FILE)

                print(flush=True)
        print(flush=True)

    except Exception as e:
        print("Error in conversation generation for Case Study ID:", patient_case_study_obj['id'], flush=True)
        print(e, flush=True)
        traceback.print_exc()

        conv_df_obj = {
            'id': patient_case_study_obj['id'],
            'clinical_case_study': patient_data,
            'patient_info_facts': patient_info_facts,
            'patient_info_vital_facts': patient_info_vital_facts,
            'intent_facts': intent_facts,
            'goal_facts': goal_facts,
            'sampled_personality_Openness_score': sampled_personality['Openness_score'],
            'sampled_personality_Conscientiousness_score': sampled_personality['Conscientiousness_score'],
            'sampled_personality_Extraversion_score': sampled_personality['Extraversion_score'],
            'sampled_personality_Agreeableness_score': sampled_personality['Agreeableness_score'],
            'sampled_personality_Neuroticism_score': sampled_personality['Neuroticism_score'],
            'sampled_mll': sampled_mll,
            'conversation_obj': conversation,
        }

        conv_objs.append(conv_df_obj)

        if len(conv_objs) % SAVE_INTERVAL == 0:
            conv_df = pd.DataFrame(conv_objs)
            conv_df.to_pickle(OUTPUT_FILE)