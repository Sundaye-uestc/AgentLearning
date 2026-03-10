from openai import OpenAI

client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

example_data = {  # 实例数据
    "是": [
        ("公司 ABC 发布了季度财报，显示盈利增长。", "财报披露，公司 ABC 利润上升。"),
        ("公司 ITCAST 发布了年度财报，显示盈利大幅度增长。", "财报披露，公司 ITCAST 更赚钱了。")
    ],
    "不是": [
        ("黄金价格下跌，投资者抛售。", "外汇市场交易额创下新高。"),
        ("央行降息，刺激经济增长。", "新能源技术的创新。")
    ]
}
# 提问数据
questions = [
    ("利率上升，影响房地产市场。","高利率对房地产有一定的冲击。"),
    ("油价大幅度下跌，能源公司面临挑战。","未来智能城市的建设趋势越加明显。"),
    ("股票市场今日大涨，投资者乐观。","持续上涨的市场让投资者感到满意。")
]

messages = [
    {"role": "system", "content": f"你帮我完成文本匹配，我给你2个句子，被[]包围，你判断它们是否匹配，回答是或不是，请参考如下示例:"}
]

for key, value in example_data.items():
    for t in value:
        messages.append({"role": "user", "content": f"句子1：[{t[0]}], 句子2：[{t[1]}]"})
        messages.append({"role": "assistant", "content": key})

for q in questions:
    responses = client.chat.completions.create(
        model="qwen3.5-plus",
        messages=messages + [{"role": "user", "content": f"句子1：[{q[0]}]，句子2：[{q[1]}]"}],
        extra_body={"enable_thinking": False},
    )
    print(messages)
    print(responses.choices[0].message.content)