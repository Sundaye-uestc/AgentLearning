from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

model = ChatTongyi(model="qwen3-max-2026-01-23")

first_prompt = PromptTemplate.from_template(
    "我的邻居姓{lastname}，刚生了{gender}，你帮我起个名字，并封装为JSON格式返回，"
    "要求key是name，value是取得名字。请严格遵守格式。"
)

second_prompt = PromptTemplate.from_template(
    "姓名：{name}，请帮我解析含义。"
)

chain = first_prompt | model | json_parser | second_prompt | model | str_parser

for chunk in chain.stream({"lastname":"张", "gender":"女儿"}):
    print(chunk, end="", flush=True)
