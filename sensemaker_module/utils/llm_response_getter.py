from openai import AzureOpenAI
from typing import Union
import time
import traceback

def get_open_ai_response(open_ai_object, message_list:list, max_tokens: int, model: str, temperature: float, deployment_id: Union[None, str] = None) -> str:
    messages = []

    for retry_ind in range(5):
        try:
            if deployment_id is None:
                response = AzureOpenAI.chat.completions.create(
                    messages=messages,
                    deployment_id=deployment_id,
                    model=model,
                    Temperature=0,
                )
            else:
                if model == "o1":
                    response = open_ai_object["openai_obj"].chat.completions.create(
                        messages=message_list,
                        model=deployment_id,
                        max_completion_tokens=15000,
                    )
                else:
                    response = open_ai_object["openai_obj"].chat.completions.create(
                        messages=message_list,
                        model=deployment_id,
                        max_tokens=max_tokens,
                        temperature=temperature
                    )    
            if response.choices[0].finish_reason == 'stop' and response.choices[0].message.content is not None and len(response.choices[0].message.content) > 20:
                return response.choices[0].message.content
            else:
                print("Invalid LLM Response:", flush=True)
                print("Full API Response Object", response, flush=True)
                print(f"Retry attempt {retry_ind + 1}", flush=True)
                time.sleep(5)

        except Exception as e:
            print()
            traceback.print_exc()
            print("Error: ", e, flush=True)
            print("Sleeping for 1 minute", flush=True)
            print(f"Retry attempt {retry_ind + 1}", flush=True)
            time.sleep(60)
    
def get_deep_seek_response(deep_seek_object, message_list:list, max_tokens: int, model: str, temperature: float, deployment_id: Union[None, str] = None) -> str:

    for retry_ind in range(5):
        try:
            response = deep_seek_object["deep_seek_obj"].complete(
                messages=message_list,
                max_tokens=15000,
                model=deployment_id
            )

            if response.choices[0].finish_reason != 'stop':
                print("Invalid LLM Response:", flush=True)
                print("Full API Response Object", response, flush=True)
                print(f"Retry attempt {retry_ind + 1}", flush=True)
                time.sleep(5)
                continue

            if "</think>" in response.choices[0].message.content:
                filtered_response = response.choices[0].message.content.split("</think>")[1].strip()
            else:
                filtered_response = response.choices[0].message.content

            if filtered_response is not None and filtered_response != "" and len(filtered_response) > 20:
                return filtered_response
            else:
                print("Invalid LLM Response:", flush=True)
                print("Full API Response Object", response, flush=True)
                print(f"Retry attempt {retry_ind + 1}", flush=True)
                time.sleep(5)
        except Exception as e:
            print()
            traceback.print_exc()
            print("Error: ", e, flush=True)
            print("Sleeping for 1 minute", flush=True)
            print(f"Retry attempt {retry_ind + 1}", flush=True)
            time.sleep(60)