from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template("我的邻居是：{lastname}")
res = template.format(lastname="张大明", hobby="钓鱼")
print(res, type(res))

res2 = template.invoke({"lastname": "周杰伦", "hobby": "唱歌"})
print(res2, type(res2))