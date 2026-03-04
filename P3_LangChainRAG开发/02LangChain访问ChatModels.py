from langchain_community.chat_models.tongyi import ChatTongyi

# 初始化模型
chat = ChatTongyi(model="qwen3-max-2026-01-23")

# 准备消息list
message = [
    # 非简写形式, 需要from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
    # SystemMessage(content="你是一个边塞诗人。"),
    # HumanMessage(content="给我写一首唐诗"),
    # AIMessage(content="锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦。"),
    # HumanMessage(content="按照你上一个回复的格式，再写一首唐诗。")

    # 简写形式
    ("system", "你是一个边塞诗人。"),
    ("human","给我写一首唐诗。"),
    ("ai", "锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦。"),
    ("human", "按照你上一个回复的格式，再写一首唐诗。")
]

# 流式输出
for chunk in chat.stream(input=message):
    print(chunk.content, end="", flush=True)