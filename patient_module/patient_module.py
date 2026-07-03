import random
from patient_module.patient_motive_generation import *
from patient_module.patient_case_study_generation import get_patient_decomp_chain, get_start_message_gen_chain
from patient_module.patient_answer_generation import INSTRUCTION_LIST_ALL, INSTRUCTION_LIST_DECISION_MAKING

MEDICAL_LITERACY_DEFS = {
"Basic":
"""* Struggles to understand basic medical terms and body parts.
* Rarely describes symptoms beyond "pain" or "sick".
* May use vague or informal terms instead of specific symptoms.
* Often cannot follow written medical instructions.
* May avoid seeking medical care due to communication barriers.""",

"Functional":
"""* Can describe basic symptoms and their duration.
* Understands meaning of common medical terms like "fever" or "allergic reaction".
* Able to follow simple medical instructions.
* Can fill out basic medical forms.
* Knows basic body systems and common conditions.""",

"Advanced":
"""* Can provide detailed symptom descriptions including onset and triggers.
* Can describe subtle symptom variations and patterns.
* Understands complex medical terminology.
* Able to discuss medication effects and interactions.
* Able to research and evaluate health information from reliable sources.
* Maintains personal health records effectively."""
}


BIG_5_TRAITS = [
    "Openness",
    "Conscientiousness",
    "Extraversion",
    "Agreeableness",
    "Neuroticism"
]

MEDICAL_LITERACY_LEVELS = [
    "Basic",
    "Functional",
    "Advanced"
]

def process_patient_case_study(patient_data, patient_llm):

    patient_decomp_chain = get_patient_decomp_chain(patient_llm)

    patient_info_facts, patient_info_vital_facts = patient_decomp_chain.invoke({
        "patient_data": patient_data
    })
    intent_facts = attach_patient_intent(patient_data, patient_llm)
    goal_facts = attach_patient_goals(patient_data, patient_llm)

    return patient_info_facts, patient_info_vital_facts, intent_facts, goal_facts

def get_patient_start_message(patient_info_facts, intent_facts, sampled_personality, sampled_mll, patient_llm):
    start_message_gen_chain = get_start_message_gen_chain(patient_llm)
    return start_message_gen_chain.invoke({
        "patient_info": intent_facts + patient_info_facts 
    }
    | sampled_personality
    | {
        "medical_literacy_level": MEDICAL_LITERACY_DEFS[sampled_mll]
    })

def filter_facts(chosen_facts, fact_memory):
    filtered_facts = []

    for f in chosen_facts:
        if f not in fact_memory:
            filtered_facts.append(f)
            fact_memory[f] = 1
            continue

        fact_memory[f] += 1
        if random.random() < (1 / fact_memory[f]) ** 0.5:
            filtered_facts.append(f)

    return filtered_facts

def get_patient_answer_v2(
    fact_selection_chain,
    answer_gen_chain,
    unknown_answer_gen_chain,
    question, 
    current_stage, 
    fact_memory, 
    patient_facts,
    intent_facts,
    goal_facts,
    sampled_mll,
    sampled_personality
):

    # Decision making and responding to emotions
    if current_stage >= 4:
        all_facts = goal_facts + patient_facts
    else:
        all_facts = intent_facts + patient_facts

    #print("Facts", all_facts)

    chosen_facts = fact_selection_chain.invoke({
        "patient_info": "\n".join([f'{i}. {fact}' for i, fact in enumerate(all_facts, 1)]),
        "question": question
    })

    # print("Chosen facts:")
    # print("\n".join(chosen_facts))
    # print()

    if len(chosen_facts) == 0:
        # return NO_ANSWER_STR
        return unknown_answer_gen_chain.invoke(
            {
                "question": question
            }
            | sampled_personality
            | {
                "medical_literacy_level": MEDICAL_LITERACY_DEFS[sampled_mll]
            }
        )

    #filtered_facts = filter_facts(chosen_facts, fact_memory)
    filtered_facts = chosen_facts

    #print("Filtered facts:")
    #print("\n".join(filtered_facts))
    #print()

    instruction_list = INSTRUCTION_LIST_ALL
    if current_stage >= 4:
        instruction_list = INSTRUCTION_LIST_DECISION_MAKING

    v = answer_gen_chain.invoke(
        {
            "patient_info": "\n".join(filtered_facts),
            "question": question,
            "instruction_list": instruction_list
        }
        | sampled_personality
        | {
            "medical_literacy_level": MEDICAL_LITERACY_DEFS[sampled_mll]
        }
    )
    return v.content