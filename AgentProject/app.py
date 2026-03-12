# 第一步：先配置 Python 模块搜索路径
import sys
import os

# 获取 app.py 所在的目录（即 AgentProject 根目录）
project_root = os.path.dirname(os.path.abspath(__file__))
# 将根目录插入到 sys.path 最前面（最高优先级）
sys.path.insert(0, project_root)

import streamlit as st

from agent.react_agent import ReactAgent

# 标题
st.title("智能机器人智能客服")
st.divider()

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

if "message" not in st.session_state:
    st.session_state["message"] = []

for msg in st.session_state["message"]:
    st.chat_message(msg["role"]).write(msg["content"])

# 用户输入提示词
prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    response_msgs = []
    with st.spinner("智能客服思考中..."):
        res_stream = st.session_state["agent"].execute_stream(prompt)

        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk

        st.chat_message("assistant").write_stream(capture(res_stream, response_msgs))
        st.session_state["message"].append({"role": "assistant", "content": response_msgs[-1]})

