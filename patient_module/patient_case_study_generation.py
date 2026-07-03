from langchain.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import AIMessage
from typing import List


PATIENT_DECOMP_PROMPT = """\
You are an assistant that is given information about a patient.

Break the following patient information into a list of independent atomic \
facts, with one piece of information in each statement. Each fact should \
only include the smallest unit of information, but should be self-contained.

Criteria:
1. Only extract medical facts that would be relevant in a conversation with a health-care provider.
2. First, list out facts related to a patient's vitals (ONLY temperature, blood pressure, pulse, respiratory rate) under "PATIENT VITAL FACTS:".
3. If there are no PATIENT VITAL FACTS just leave the section empty. 
4. List out the remaining medical atomic facts under the section "PATIENT FACTS:".

Patient Information:
"{patient_data}"

Respond with the list of atomic facts for each section "PATIENT VITAL FACTS:" and "PATIENT FACTS:" (no formatting) and nothing else, prepend each fact with a '- '. No sub-lists are allowed.
"""

def process_text_to_sentences_block(text: str) -> List[str]:
	if text == "":
		return []
	
	sentences = text.split('- ')[1:]
	sentences = [
		sent[:sent.find('\n')] if '\n' in sent else sent
		for sent in sentences
	]
	sentences = [
		sent.strip()[:-1] if sent.strip()[-1] == '\n' else sent.strip()
		for sent in sentences
	]

	if sentences:
		if sentences[-1][-1] != '.':
			sentences[-1] = sentences[-1] + '.'
	else:
		sentences = []

	return sentences	

def process_patient_facts(llm_response: AIMessage):
	llm_response_text = llm_response.content
	#print(llm_response_text)

	patient_facts_str = llm_response_text.split("PATIENT FACTS:")[1].strip()
	patient_facts = process_text_to_sentences_block(patient_facts_str)

	patient_vitals_raw = llm_response_text.split("PATIENT VITAL FACTS:")[1].strip()
	patient_vitals_facts_str = patient_vitals_raw.split("PATIENT FACTS:")[0].strip()
	patient_vitals_facts = process_text_to_sentences_block(patient_vitals_facts_str)

	return patient_facts, patient_vitals_facts

def get_patient_decomp_chain(llm: AzureChatOpenAI):
	patient_decomp_prompt = ChatPromptTemplate([
        ("user", PATIENT_DECOMP_PROMPT),
    ])
	return patient_decomp_prompt | llm | process_patient_facts

START_MESSAGE_GEN_PROMPT = """\
You are an intelligent agent who is given a LIST OF MEDICAL FACTS about a patient, \
who is going to have a conversation with an AI healthcare provider. Your task is to construct a start message \
with the most important facts in first person, as if you are simulating the patient's persona and literacy while talking to the AI.

To aid in this process, Big 5 personality traits are defined as:

1. Openness:
Openness (also referred to as openness to experience) emphasizes imagination and insight the most out of all five \
personality traits. People who are high in openness tend to have a broad range of interests. They are curious \
about the world and other people and are eager to learn new things and enjoy new experiences. People who are high \
in this personality trait also tend to be more adventurous and creative. Conversely, people low in this personality \
trait are often much more traditional and may struggle with abstract thinking.

2. Conscientiousness:
Conscientiousness is defined by high levels of thoughtfulness, good impulse control, and goal-directed behaviors. \
Highly conscientious people tend to be organized and mindful of details. They plan ahead, consider how their \
behavior affects others, and are conscious of deadlines. If a person scores low on this personality trait, it \
might mean they are less structured and organized. They may procrastinate when it comes to getting things done, \
sometimes missing deadlines completely.

3. Extraversion:
Extraversion (or extroversion) is a personality trait characterized by excitability, sociability, talkativeness, \
assertiveness, and high amounts of emotional expressiveness.1 People high in extraversion are outgoing and tend \
to gain energy in social situations. Being around others helps them feel energized and excited. People who are low \
in this personality trait (or introverted) tend to be more reserved. They have less energy in social settings, \
and social events can feel draining. Introverts often require a period of solitude and quiet to "recharge."

4. Agreeableness:
This personality trait includes attributes such as trust, altruism, kindness, affection, and other prosocial behaviors.\
People who are high in agreeableness tend to be more cooperative while those low in this personality trait tend to be \
more competitive and sometimes even manipulative.

5. Neuroticism:
Neuroticism is a personality trait characterized by sadness, moodiness, and emotional instability. \
This trait is generally defined as a negative personality trait that can have detrimental effects on \
a person's life and well-being. Individuals who are high in neuroticism tend to experience mood swings, \
anxiety, irritability, and sadness. People who are low in this personality trait tend to be more \
stable and emotionally resilient.

Instructions:
1. Given a LIST OF MEDICAL FACTS about a patient, choose a MAXIMUM of TWO relevant facts from the list to construct a starting message as a patient to an AI healthcare provider.
2. The start message should be in first person, using the emotions, tone, word choice and intensity of a patient who has the levels \
of the Big 5 Personality Traits (on a 2-point Low/High scale) and Medical Literacy Level shown below.
3. ONLY use the medical literacy level and personality definitions as a guide, DO NOT EXPLICITLY integrate any information from it into the answer.
4. First provide a short reasoning under "REASONING:" before writing the start message under "START_MESSAGE:".
5. Do not include quotes, any other formatting, extra information beyond the REASONING and the START_MESSAGE.

Your Task:

LIST OF MEDICAL FACTS:
{patient_info}

Big 5 Personality Traits:
1. Openness: {Openness_score}
2. Conscientiousness: {Conscientiousness_score}
3. Extraversion: {Extraversion_score}
4. Agreeableness: {Agreeableness_score}
5. Neuroticism: {Neuroticism_score}

MEDICAL LITERACY LEVEL:
{medical_literacy_level}

SOLUTION:
"""

def process_start_message_op(llm_response: AIMessage):
	"""Transform LLM output into sentences."""
	llm_response_text = llm_response.content
	#print(llm_response_text)
	
	return llm_response_text.split("START_MESSAGE:")[1].strip().strip("")

def get_start_message_gen_chain(llm: AzureChatOpenAI):
	start_message_gen_prompt = ChatPromptTemplate([
        ("system", START_MESSAGE_GEN_PROMPT),
    ])
	return start_message_gen_prompt | llm | process_start_message_op