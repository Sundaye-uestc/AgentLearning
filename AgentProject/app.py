"""
使用终端在该目录：D:\Work\26.5 科技厅RAG\RagAgent下运行：
streamlit run app.py
由于路径原因导致各脚本无法单独运行，但可以运行该app.py
如需运行单独脚本，需要脚本第一行添加如下代码：

# agent/tools/agent_tools.py 完整代码（可单独运行）
import sys
import os
# 路径适配：二级子目录，需要 ../../ 回到根目录
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
"""
import time

import streamlit as st

from agent.react_agent import ReactAgent

# 标题
st.title("航空、交通领域边缘侧大模型智能系统")
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
    with st.spinner("思考中..."):
        res_stream = st.session_state["agent"].execute_stream(prompt)

        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)

                for char in chunk:
                    time.sleep(0.01)
                    yield char

        st.chat_message("assistant").write_stream(capture(res_stream, response_msgs))
        st.session_state["message"].append({"role": "assistant", "content": response_msgs[-1]})
        st.rerun()
