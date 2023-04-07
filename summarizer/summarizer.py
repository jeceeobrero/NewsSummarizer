import openai
from news import settings

def generate_summary(text):
    openai.api_key = settings.OPENAI_SECRET_KEY
    
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
    return summary.strip()
