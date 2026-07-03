# Code Repository for our ACL 2026 Main paper: *Reasoning Is Not All You Need: Examining LLMs for Multi-Turn Mental Health Conversations*

### [[ACL 2026 Paper](https://aclanthology.org/2026.acl-long.2164/)]

## Citation

```bibtex
@inproceedings{chandra-etal-2026-reasoning,
    title = "Reasoning Is Not All You Need: Examining {LLM}s for Multi-Turn Mental Health Conversations",
    author = "Chandra, Mohit  and
      Sriraman, Siddharth  and
      Khanuja, Harneet Singh  and
      Jin, Yiqiao  and
      De Choudhury, Munmun",
    editor = "Liakata, Maria  and
      Moreira, Viviane P.  and
      Zhang, Jiajun  and
      Jurgens, David",
    booktitle = "Proceedings of the 64th Annual Meeting of the {A}ssociation for {C}omputational {L}inguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2026",
    address = "San Diego, California, United States",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2026.acl-long.2164/",
    doi = "10.18653/v1/2026.acl-long.2164",
    pages = "46648--46682",
    ISBN = "979-8-89176-390-6",
    abstract = "Limited access to mental healthcare, extended wait times, and increasing capabilities of Large Language Models (LLMs) has led individuals to turn to LLMs for fulfilling their mental health needs. However, examining the multi-turn mental health conversation capabilities of LLMs remains under-explored. Existing evaluation frameworks typically focus on diagnostic accuracy and win-rates and often overlook alignment with patient-specific goals, values, and personalities required for meaningful conversations. To address this, we introduce MedAgent, a novel framework for synthetically generating realistic, multi-turn mental health sensemaking conversations and use it to create the Mental Health Sensemaking Dialogue (MHSD) dataset, comprising over 2,200 patient{--}LLM conversations. Additionally, we present MultiSenseEval, a holistic framework to evaluate the multi-turn conversation abilities of LLMs in healthcare settings using human-centric criteria. Our findings reveal that frontier reasoning models yield below-par performance for patient-centric communication and struggle at precise ({''}hard'') diagnostic capabilities with average accuracy of {\textasciitilde}31{\%}. Additionally, we observed variation in model performance based on patient{'}s persona and performance drop with increasing turns in the conversation. Our work provides a comprehensive synthetic data generation framework, a dataset and evaluation framework for assessing LLMs in multi-turn mental health conversations."
}
```

## Installation and Setup

1. Install Python dependencies in a venv.

```bash
pip install pandas openai azure-ai-inference azure-core langchain langchain-openai langchain-core
```

2. Obtain access to the models used by the script.

- For accessing the OpenAI / DeepSeek models, you will need to deploy the models using your account with [Microsoft Azure Foundry](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure?tabs=global-standard&pivots=azure-openai).

3. Use a MedQA case-study CSV file. The script expects the following columns:

- `id`
- `clinical_case_study`
- `mental_health_classification`

Only rows where `mental_health_classification` is `Yes` are used.

## Patient-Sensemaker Conversation Generation

Use `generate_conversation.py` to simulate conversations from clinical case studies. For each case study, it generates and saves conversations across five sampled personality profiles and two medical literacy levels.

### Usage

```bash
python generate_conversation.py \
  --case_study_file ./data/case_studies.csv \
  --start_ind 0 \
  --end_ind 10 \
  --model o1 \
  --openai_api_endpoint "<your-azure-openai-endpoint>" \
  --openai_api_key "<your-azure-openai-api-key>" \
  --deepseek_api_endpoint "<your-azure-deepseek-endpoint>" \
  --deepseek_api_key "<your-deepseek-api-key>" \
  --deepseek_model_name "<your-deepseek-deployment-or-model-name>" \
  --output_file ./outputs/conversations.pkl
```

| Parameter | Meaning |
| --- | --- |
| `--case_study_file` | Input CSV containing clinical case studies. |
| `--start_ind` | First filtered row index to process. |
| `--end_ind` | Stop before this filtered row index. |
| `--model` | Sensemaker generation model. Use `o1` for Azure OpenAI o1; other values use DeepSeek. |
| `--openai_api_endpoint` | Azure OpenAI endpoint for the fixed `gpt-4o` patient/computation models and `o1` generation. |
| `--openai_api_key` | API key for the Azure OpenAI endpoint. |
| `--deepseek_api_endpoint` | Azure AI Foundry / DeepSeek endpoint. |
| `--deepseek_api_key` | API key for the DeepSeek endpoint. |
| `--deepseek_model_name` | DeepSeek deployment/model name used when `--model` is not `o1`. |
| `--output_file` | Pickle file where generated conversations are saved. |
