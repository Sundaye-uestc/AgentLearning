from langchain_community.llms.tongyi import Tongyi

# qwen-max是大语言模型
model = Tongyi(model="qwen-max")

# # 调用invoke向模型提问
# res = model.invoke(input="你是谁呀能做什么？")
#
# print(res)
#
# 调用stream方法进行流式提问
res = model.stream(input="如何评价Dream Theater？", enable_thinking=False)

for chunk in res:
    print(chunk, end="", flush=True)
