from openai import OpenAI
import os
client = OpenAI(
    base_url="stealth/ox-alpha",
    api_key=os.environ["sk-y2BYnIDDk6GgIyPxZcrWPUv5QkFTkpeaxP69UqceJD32CZeb"],
)

response = client.chat.completions.create(
    model="stealth/ox-alpha",
    messages=[{"role": "user", "content": "Summarize the request."}],
)
print(response.choices[0].message.content)