from langchain_community.embeddings import DashScopeEmbeddings

# 初始化嵌入模型对象，其默认使用模型是：text-embedding-v1
embed = DashScopeEmbeddings()

# 测试
print(embed.embed_query("我喜欢你"))
print(embed.embed_documents(['我喜欢你', '我稀饭你', '晚上吃啥']))