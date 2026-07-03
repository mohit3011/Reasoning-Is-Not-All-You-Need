from message_to_fact_convertor import convert_message_to_facts, indices_of_matching_facts_count
def check_message_ulitity(current_message, patient_facts, counter, obj_element, max_token, temperature):
    facts = convert_message_to_facts(current_message, obj_element, max_token, temperature)
    matched_facts_indices = indices_of_matching_facts_count(facts, patient_facts, obj_element, max_token, temperature)
    if len(matched_facts_indices)>0:
        for index in matched_facts_indices:
            patient_facts.append(facts[index])
        return patient_facts, counter+1#0
    else:
        return patient_facts, counter+1