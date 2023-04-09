# News Article Summarizer

This summarizer's goal is to display the brief and precise content of the news article. It uses GPT-3, an autoregressive language model released in 2020 that uses deep learning to produce human-like text.

## How it Works

1. It defines the API Key for the Open AI.
```
openai.api_key = get_api_key()     
```
2. Generate summary using GPT-3 API with the desired configurations.
```
# Generate summary using GPT-3 API using the configurations
summary = ""
max_tokens = 300
model_engine = "text-davinci-002"
prompt = (f"Please summarize the following text in {max_tokens} tokens:"
            f"{text}")
try:
    completions = openai.Completion.create(
        engine=model_engine, prompt=prompt, max_tokens=max_tokens, n=1, stop=None, temperature=0.5)
    summary = completions.choices[0].text
except Exception as e:
    print("Error: ", e)
```
3. Returns the summary (with no double breaklines) for further procedure.
```
return summary.strip()
```
