from langchain.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import AIMessage

NO_ANSWER_STR = "I'm not sure about this or cannot answer this, could you ask me a different question?"

NO_MATCH_STR = "NO MATCH"

FACT_SELECTION_PROMPT = """\
You are an intelligent agent who is given a QUESTION from a doctor to a patient, \
and a LIST OF MEDICAL FACTS about the patient. Your task is to choose the facts which \
best answer the question, or respond "NO MATCH".

Instructions:
1. Given a LIST OF MEDICAL FACTS about a patient, choose a MAXIMUM of THREE facts from the list that when combined best answers the QUESTION. 
2. If NO fact matches the question, simply respond "NO MATCH" under "FACTS:".
3. If facts are chosen, output them as a list, preserving the numbering from the original list. 
4. First provide a short reasoning under "REASONING:" before listing the facts under "FACTS:".
5. Do not include any other formatting or extra information beyond the REASONING and given FACTS.

Your Task:

QUESTION:
{question}

LIST OF MEDICAL FACTS:
{patient_info}

SOLUTION:
"""

def text_to_sentences(llm_response: AIMessage):
	"""Transform LLM output into sentences."""
	llm_response_text = llm_response.content
	#print(llm_response_text)

	llm_response_text = llm_response_text.split("FACTS:")[1].strip()
	#print(llm_response_text)

	if NO_MATCH_STR.lower() in llm_response_text.lower():
		return []

	sentences = llm_response_text.split('\n')#[1:]
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

def get_fact_selection_chain(llm: AzureChatOpenAI):
	fact_selection_prompt = ChatPromptTemplate([
        ("system", FACT_SELECTION_PROMPT),
    ])
	return fact_selection_prompt | llm | text_to_sentences