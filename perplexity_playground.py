import requests


PERPLEXITY_API_TOKEN = "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"

SONAR_SMALL_ONLINE_MODEL = "sonar-small-online"
MIXTRAL_8X7B_INSTRUCT_MODEL = "mixtral-8x7b-instruct"

url = "https://api.perplexity.ai/chat/completions"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {PERPLEXITY_API_TOKEN}",
}


def call_perpexity_llm(sys_prompt: str, user_prompt: str, model: str) -> str:
    payload = {
        "model": "sonar-small-online",
        "messages": [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    response = requests.post(url, json=payload, headers=headers).json()

    return response["choices"][0]["message"]["content"]
