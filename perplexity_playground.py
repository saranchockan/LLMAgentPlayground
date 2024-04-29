import requests

COMPANY_NAME = "Benchling"
EXTRACT_COMPANY_CAREER_PAGE_URL_PROMPT = f"""Can you output the URL that is the 
official careers page for a tech company called {COMPANY_NAME}? 
Remember, YOUR OUTPUT SHOULD ONLY BE THE URL and NOTHING ELSE."""

PERPLEXITY_API_TOKEN = "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"

url = "https://api.perplexity.ai/chat/completions"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {PERPLEXITY_API_TOKEN}",
}


def call_perpexity_llm(prompt: str) -> str:
    payload = {
        "model": "sonar-small-online",
        "messages": [
            {
                "role": "system",
                "content": """You are a website crawler. You will be given the name of a company. 
You should output the URL of the company's career page. 
Remember, YOUR OUTPUT SHOULD ONLY BE THE URL and NOTHING ELSE""",
            },
            {"role": "user", "content": prompt},
        ],
    }
    response = requests.post(url, json=payload, headers=headers).json()

    return response["choices"][0]["message"]["content"]
