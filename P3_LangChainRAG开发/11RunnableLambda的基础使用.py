from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

str_parser = StrOutputParser()

model = ChatTongyi(model="qwen3-max-2026-01-23")

first_prompt = PromptTemplate.from_template(
    "我的邻居姓{lastname}，刚生了{gender}，帮我取个名字。仅输出名字即可，不要输出其他任何额外信息。"
)

second_prompt = PromptTemplate.from_template(
    "姓名：{name}，请帮我解析含义。"
)

# 函数的入参：AIMessage -> dict ({"name":"XXX"})
my_func = RunnableLambda(lambda ai_msg: {"name": ai_msg.content})

chain = first_prompt | model | my_func | second_prompt | model | str_parser

for chunk in chain.stream({"lastname":"冯", "gender":"女儿"}):
    print(chunk, end="", flush=True)
