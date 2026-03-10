from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

model = ChatTongyi(model="qwen3-max-2026-01-23")
prompt = PromptTemplate.from_template(
    "我的邻居姓{lastname}，刚生了{gender}，你帮我起个名字，简单回答。"
)

parser = StrOutputParser()  # 如果没有将无法正确识别
chain = prompt | model | parser | model | parser

res = chain.invoke({"lastname":"张", "gender":"女儿"})
print(res)