import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"
)

messages=[
    {
        "role":"system",
        "content":"你是一个 Python 入门教学助手"
    }
]

def chat(question):
    messages.append({
        "role": "user",
        "content": question
    })

    response = client.chat.completions.create(
    model="deepseek-flash",
    messages=messages,
    extra_body={"thinking": {"type": "disabled"}}
    )

    answer = response.choices[0].message.content or ""

    if answer:
        messages.append({
            "role":"assistant",
            "content":answer
    })

    return response
while True:
    question = input("请输入你的问题：")
    if question == "" or question.lower() in ("exit","quit","q"):
        print("再见！")
        break
    response = chat(question)
    #print(response.model_dump_json(indent=2)) #查看完整re
    print("AI回复:")
    print(response.choices[0].message.content)
    print("对话轮数：",(len(messages)-1)//2)
    if response.usage:
        print("输入Token：",response.usage.prompt_tokens)
        print("输出Token：",response.usage.completion_tokens)
        print("total Token：",response.usage.total_tokens)