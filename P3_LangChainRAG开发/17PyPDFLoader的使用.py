from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(
    file_path="./data/dive-into-llm.pdf",
    mode='page',        # 读取模式，page是默认模式。
                        # single模式：不管多少页，只返回一个Document对象
    # password=""       # 密码，非必选

)
i = 0
for doc in loader.lazy_load():
    i += 1
    print(doc)
    print("="*20, i)