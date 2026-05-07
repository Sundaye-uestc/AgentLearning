import time

import streamlit as st
import streamlit.components.v1 as components

from agent.react_agent import ReactAgent

st.set_page_config(page_title="航空、交通领域边缘侧大模型智能系统")

st.markdown("""
<style>
.thinking-text {
    font-style: italic;
    color: #888888;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

st.title("航空、交通领域边缘侧大模型智能系统")
st.divider()

def scroll_to_bottom():
    # 方式1：st.markdown 注入脚本（脚本在 Streamlit app 的 DOM 内执行）
    st.markdown(
        """
        <script>
            (function() {
                var el = document.querySelector('.main') ||
                         document.querySelector('[data-testid="stAppViewContainer"]') ||
                         document.querySelector('.stApp');
                if (el) { el.scrollTop = el.scrollHeight; }
                var m = document.getElementById('bottom-marker');
                if (m) { m.scrollIntoView({block: 'end'}); }
            })();
        </script>
        """,
        unsafe_allow_html=True,
    )
    # 方式2：components.html 注入脚本（从子 iframe 访问父级 Streamlit app DOM）
    components.html(
        """
        <script>
            (function() {
                var doc = window.parent.document;
                var el = doc.querySelector('.main') ||
                         doc.querySelector('[data-testid="stAppViewContainer"]') ||
                         doc.querySelector('.stApp');
                if (el) { el.scrollTop = el.scrollHeight; }
                var m = doc.getElementById('bottom-marker');
                if (m) { m.scrollIntoView({block: 'end'}); }
            })();
        </script>
        """,
        height=0,
        width=0,
    )

def stop_generation():
    st.session_state["_stop_requested"] = True

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

if "message" not in st.session_state:
    st.session_state["message"] = []

# 处理中止生成：将已流式输出的部分内容作为截断回答保存
if st.session_state.get("_stop_requested") and st.session_state.get("_stream_chunks") is not None:
    chunks = st.session_state["_stream_chunks"]
    if chunks:
        if len(chunks) > 1:
            thinking = "".join(chunks[:-1])
            answer = chunks[-1]
        else:
            thinking = ""
            answer = chunks[0]
        answer += "\n\n*[已中止]*"
    else:
        thinking = ""
        answer = "*[已中止]*"

    st.session_state["message"].append({
        "role": "assistant",
        "content": answer,
        "thinking": thinking,
    })
    # 清理临时状态
    st.session_state["_stop_requested"] = False
    st.session_state["_generating"] = False
    st.session_state.pop("_stream_chunks", None)
    scroll_to_bottom()

# 渲染历史消息
for msg in st.session_state["message"]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        thinking = msg.get("thinking", "")
        with st.chat_message("assistant"):
            if thinking:
                with st.expander("💭 查看思考过程", expanded=False):
                    st.markdown(
                        f'<div class="thinking-text">{thinking}</div>',
                        unsafe_allow_html=True,
                    )
            st.write(msg["content"])

# 当有历史消息时，页面自动滚动到底部
if st.session_state["message"]:
    scroll_to_bottom()

st.markdown('<div id="bottom-marker"></div>', unsafe_allow_html=True)

# 中止按钮：仅在模型生成过程中显示
if st.session_state.get("_generating", False):
    c1, c2, c3 = st.columns([3, 1, 3])
    with c2:
        st.button("⏹ 中止生成", on_click=stop_generation, key="stop_btn", use_container_width=True)

prompt = st.chat_input()

if prompt:
    st.session_state["_stop_requested"] = False
    st.session_state["_generating"] = True
    st.session_state["_stream_chunks"] = []

    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})
    scroll_to_bottom()

    all_chunks = []

    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            stream_placeholder = st.empty()
            res_stream = st.session_state["agent"].execute_stream(prompt)

            for chunk in res_stream:
                all_chunks.append(chunk)
                st.session_state["_stream_chunks"] = all_chunks
                cumulative = "".join(all_chunks)
                stream_placeholder.markdown(
                    f'<div class="thinking-text">{cumulative}</div>',
                    unsafe_allow_html=True,
                )

        stream_placeholder.empty()

        # 分离思考过程与最终答案
        if len(all_chunks) > 1:
            thinking = "".join(all_chunks[:-1])
            answer = all_chunks[-1]
        elif len(all_chunks) == 1:
            thinking = ""
            answer = all_chunks[0]
        else:
            thinking = ""
            answer = ""

        # 思考过程放入折叠框
        if thinking:
            with st.expander("💭 查看思考过程", expanded=False):
                st.markdown(
                    f'<div class="thinking-text">{thinking}</div>',
                    unsafe_allow_html=True,
                )

        # 最终答案逐字符流式输出
        answer_placeholder = st.empty()
        displayed = ""
        for char in answer:
            displayed += char
            answer_placeholder.markdown(displayed)
            time.sleep(0.01)

    st.session_state["_generating"] = False
    st.session_state.pop("_stream_chunks", None)

    st.session_state["message"].append({
        "role": "assistant",
        "content": answer,
        "thinking": thinking,
    })
    st.rerun()
