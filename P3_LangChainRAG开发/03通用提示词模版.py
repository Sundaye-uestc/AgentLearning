from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate

# zero-shot形式
prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lastname}，刚生了{gender}，你帮我起个名字，简单回答。"
)

model = Tongyi(model="tongyi-xiaomi-analysis-pro")

# # 调用.format方法注入信息
# prompt_text = prompt_template.format(lastname="张", gender="女儿")
#
# res = model.invoke(input=prompt_text)
# print(res)

# LCE表达式
chain = prompt_template | model

res = chain.invoke(input={"lastname": "张", "gender": "女儿"})
print(res)