
import os
from openai import OpenAI

client = OpenAI(
    api_key ="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"
)

stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "write a small 30 word love story"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")