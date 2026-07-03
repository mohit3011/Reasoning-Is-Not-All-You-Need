from langchain.prompts import ChatPromptTemplate

PATIENT_INTENT_VIGNETTES = {
    'interpreting medical information from a patient perspective':
    {'definition': 'Patient aims to use LLMs to simplify complex medical terminology and concepts so that patients can more easily understand diagnoses, procedures, and general health information.',
    'patterns': ['patient can provide their symptoms and past medical history to recieve lay-person friendly explanations of their condition.',
                'patients can ask questions about their condition and receive clear, concise answers.',
                'patients can receive personalized advice on how to manage their health.',
                'patients can understand the importance of following their treatment plan.',
                'patients can feel more confident in their ability to make informed decisions about their health.'
    ]
    },
    'providing lifestyle recommendations and improving health literacy':
    {'definition': 'Patient aims to use LLMs to seek lifestyle change recommendations and debunking myths about health and wellness.',
    'patterns': ['patients can ask questions about lifestyle changes and receive recommendations.',
                'patients can query about the myths surrounding health and wellness.',
                'patients can ask about self-management techniques.',
                'patients can ask about the latest health trends.'
    ]
    },
    'personalizing healthcare journeys':
    {'definition': 'Patient aims to use LLMs to tailor educational content and recommendations based on individual patient data (e.g., health history, preferences), resulting in more relevant and actionable advice.',
    'patterns': ['Patients enter personal health goals (like weight loss or improved mobility), prompting LLMs to generate targeted tips.',
                'Patients provide feedback on what they do or do not understand, and LLMs adjusts explanations accordingly.',
                'Patients ask about specific health topics, and LLMs offers personalized advice based on their data.'
    ]}
}

VIGNETTES = ""
count = 1
for vignette_name in PATIENT_INTENT_VIGNETTES:
    VIGNETTES += f'''
{count}. VIGNETTE_NAME: {vignette_name}
VIGNETTE_DEFINITION: {PATIENT_INTENT_VIGNETTES[vignette_name]['definition']}
VIGNETTE_PATTERNS:'''
    for pattern in PATIENT_INTENT_VIGNETTES[vignette_name]['patterns']:
        VIGNETTES += f'''\n* {pattern}'''
    VIGNETTES += '\n'
    count += 1

PATIENT_INTENT_PROMPT = """\
You are an expert psychiatrist/psychologist/psychotherapist. Given a patient case study, your task is to pick the most appropriate motivation for that patient to consult an LLM. You are given a case study (provided as CASE_STUDY) and a list of patient conversation intent vignettes in the format (VIGNETTE_NAME, VIGNETTE_DEFINITION, VIGNETTE_PATTERNS). \
You need to pick the most approapriate vignette for the given case study.
Think step by step and first provide your rationale (under "RATIONALE:") and then at the last output the VIGNETTE_NAME for the most logical vignette for the given case study. 
{vignettes}
CASE_STUDY: {case_study}

Strictly follow the format: <ASSIGNED_VIGNETTE_NAME: VIGNETTE_NAME>. Use the exact vignette name and nothing else.
"""

def process_intent_vignette_res(llm_response):
    llm_response_text = llm_response.content
    v = llm_response_text.split("ASSIGNED_VIGNETTE_NAME: ")[1].strip()
    v = v.rstrip('.').rstrip('>').rstrip('.>').rstrip('>.').rstrip('*').rstrip('*')
    return v

def get_patient_intent_chain(patient_llm):
    patient_intent_prompt = ChatPromptTemplate([
        ("user", PATIENT_INTENT_PROMPT),
    ])
    return patient_intent_prompt | patient_llm | process_intent_vignette_res

def attach_patient_intent(patient_data, patient_llm):
    patient_intent_chain = get_patient_intent_chain(patient_llm)
    v = patient_intent_chain.invoke({
        "vignettes": VIGNETTES,
        "case_study": patient_data
    })
    return [PATIENT_INTENT_VIGNETTES[v]['definition']]


PATIENT_GOAL_VIGNETTES = {
    "maximize comfort and avoid suffering": {"definition": "Patient’s goal is to maximize comfort and avoid suffering. Includes seeking interventions to promote comfort (e.g., pain control) and avoiding interventions that would increase discomfort, even at the expense of decreasing longevity."},
    "maintain or improve cognitive or physical functioning": {"definition": "Patient’s goal is to maintain or improve cognitive or physical functioning by undergoing medical care aimed at preventing or reversing dysfunction, even if that medical care would increase discomfort. However, care that would increase survival/longevity without preservation or improvement in function is generally avoided."},
    "extending longevity or survival": {"definition": "Patient’s goal is to live as long as possible without limitations on care. Extending longevity or survival is prioritized over maximizing function or comfort."}
}

GOAL_VIGNETTES = ""
count = 1
for vignette_name in PATIENT_GOAL_VIGNETTES:
    GOAL_VIGNETTES += f'''
{count}. VIGNETTE_NAME: {vignette_name}
VIGNETTE_DEFINITION: {PATIENT_GOAL_VIGNETTES[vignette_name]['definition']}
'''
    count += 1

PATIENT_GOAL_PROMPT = """\
You are an expert psychiatrist/psychologist/psychotherapist. Given a patient case study, your task is to pick the most appropriate goal for that patient's consultation with an LLM. You are given a case study (provided as CASE_STUDY) and a list of patient conversation goal vignettes in the format (VIGNETTE_NAME, VIGNETTE_DEFINITION, VIGNETTE_PATTERNS). \
You need to pick the most approapriate vignette for the given case study.
Think step by step and first provide your rationale (under "RATIONALE:") in around 30 words and then at the last output the VIGNETTE_NAME for the most logical vignette for the given case study. 
{vignettes}
CASE_STUDY: {case_study}

Strictly follow the format: <ASSIGNED_VIGNETTE_NAME: VIGNETTE_NAME>. Use the exact vignette name and nothing else.
"""

def process_goal_vignette_res(llm_response):
    llm_response_text = llm_response.content
    v = llm_response_text.split("ASSIGNED_VIGNETTE_NAME: ")[1].strip()
    v = v.rstrip('.').rstrip('>').rstrip('.>').rstrip('>.').rstrip('*').rstrip('*')
    return v

def get_patient_goal_chain(patient_llm):
    patient_goal_prompt = ChatPromptTemplate([
        ("user", PATIENT_GOAL_PROMPT),
    ])
    return patient_goal_prompt | patient_llm | process_goal_vignette_res

def attach_patient_goals(patient_data, patient_llm):
    patient_goal_chain = get_patient_goal_chain(patient_llm)
    #print(GOAL_VIGNETTES)
    v = patient_goal_chain.invoke({
        "vignettes": GOAL_VIGNETTES,
        "case_study": patient_data
    })
    return [PATIENT_GOAL_VIGNETTES[v]['definition']]