import json

from openai import OpenAI

client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

schema = ['日期', '股票名称', '开盘价', '收盘价', '成交量']

example_data = [    # 实例数据
    {
        "content":"2023-01-10, 股市震荡。股票强大科技 A 股今日开盘价 100 人民币，一度飙升至 105 人民币，随后回落至 98 人民币，最终以 102 人民币收盘，成交量达到 520000。",
        "answers": {
            "日期":"2023-01-10",
            "股票名称":"强大科技 A 股",
            "开盘价":"100 人民币",
            "收盘价":"102 人民币",
            "成交量":"520000"
        }
    },
    {
        "content":"2024-05-16, 股市利好。股票英伟达美股今日开盘价 105 美元，一度飙升至 109 美元，随后回落至 100 美元，最终以 116 美元收盘，成交量达到 3560000。",
        "answers": {
            "日期":"2024-05-16",
            "股票名称":"英伟达美股",
            "开盘价":"105 美元",
            "收盘价":"116 美元",
            "成交量":"3560000"
        }
    }
]
# 提问数据
questions = [
    "2025-06-16, 股市利好。股票传智教育 A 股今日开盘价 66 人民币，一度飙升至 70 人民币，随后回落至 65 人民币，最终以 68 人民币收盘，成交量达到 123000。",
    "2025-06-06, 股市利好。股票黑马程序员 A 股今日开盘价 200 人民币，一度飙升至 211 人民币，随后回落至 201 人民币，最终以 206 人民币收盘。"
]

messages = [
    {"role": "system", "content": f"你帮我完成信息抽取，对我的句子抽取{schema}信息，按JSON字符串输出，如果某些信息不存在，用'原文未提及'回答"}
]

for example in example_data:
    messages.append(
        {"role": "user", "content": example["content"]}
    )
    messages.append(
        {"role": "assistant", "content": json.dumps(example["answers"], ensure_ascii=False)}
    )

for q in questions:
    response = client.chat.completions.create(
        model="qwen3.5-plus",
        messages=messages + [{"role": "user", "content": f"按照上述的示例，现在抽取这个句子的信息：{q}"}],
        extra_body={"enable_thinking": False},
    )
    print(response.choices[0].message.content)