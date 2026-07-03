# Reasoning Is Not All You Need: Examining LLMs for Multi-Turn Mental Health Conversations

### [[ACL 2026 Paper](https://arxiv.org/abs/2505.20201)]

Code for the article "Reasoning Is Not All You Need: Examining LLMs for Multi-Turn Mental Health Conversations".

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
