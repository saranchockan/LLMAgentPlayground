import openai


# Load OPENAI_API_KEY from env
OPEN_API_KEY="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"
openai.api_key = OPEN_API_KEY

# Define the prompt and make a request to the model
prompt = "Translate English to French: Hello, how are you?"
response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    max_tokens=50
)

# Access the generated translation
translated_text = response.choices[0].text.strip()
print(translated_text)

prompt = "Translate English to French: Hello, how are you?"
response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    max_tokens=50
)