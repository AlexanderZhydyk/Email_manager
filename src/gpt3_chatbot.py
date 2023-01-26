import openai
import os

from config import conf

completion = openai.Completion()

openai.api_key = os.getenv("OPENAI_KEY", conf.OPENAI_KEY)


def get_reply(question):
    response = completion.create(
        prompt=question, engine="davinci", temperature=0.5,
        top_p=1, frequency_penalty=0.7, presence_penalty=0, best_of=1,
        max_tokens=20)
    answer = response.choices[0].text.strip()
    return answer
