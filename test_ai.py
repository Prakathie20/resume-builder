import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
print(f"API Key loaded: {bool(openai_api_key)}")
print(f"API Key length: {len(openai_api_key) if openai_api_key else 0}")

if openai_api_key:
    openai.api_key = openai_api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'Hello World'"}
            ],
            max_tokens=10
        )
        print("✅ OpenAI API is working!")
        print(f"Response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"❌ OpenAI Error: {e}")
else:
    print("❌ No API key found in .env file")