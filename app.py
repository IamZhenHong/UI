import streamlit as st
import requests

# Title of the app
st.title("恋爱分析")

# Initialize session state for the target and results
if "target_id" not in st.session_state:
    st.session_state.target_id = None
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "strategy_result" not in st.session_state:
    st.session_state.strategy_result = None
if "reply_options_flow_result" not in st.session_state:
    st.session_state.reply_options_flow_result = None

# Form to create a target
st.markdown("### 创建或选择目标")
with st.form("create_target_form"):
    name = st.text_input("目标姓名", placeholder="输入目标的姓名")
    gender = st.text_input("性别", placeholder="输入目标的性别")
    relationship_context = st.text_input("关系背景", placeholder="例如：朋友，同事")
    relationship_perception = st.text_input("关系感知", placeholder="例如：亲密，疏远")
    relationship_goals = st.text_input("关系目标", placeholder="例如：结婚，约会")
    relationship_goals_long = st.text_input("长期关系目标", placeholder="例如：生活在一起，结婚")
    personality = st.text_input("性格", placeholder="例如：外向，内向")
    language = st.text_input("语言", placeholder="例如：英语，西班牙语")
    
    create_target_button = st.form_submit_button("创建目标")

# Create target logic
if create_target_button:
    if name:
        try:
            response = requests.post(
                "https://poc2-168m.onrender.com/targets/",
                json={
                    "name": name,
                    "gender": gender,
                    "relationship_context": relationship_context,
                    "relationship_perception": "",
                    "relationship_goals": "",
                    "relationship_goals_long": "",
                    "personality": personality,
                    "language": language,
                },
            )
            if response.status_code == 200:
                target_data = response.json()
                st.session_state.target_id = target_data["id"]
                st.session_state.name = target_data["name"]
                st.success(f"目标创建成功！ID: {st.session_state.target_id}")
            else:
                st.error(f"错误: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"请求失败: {e}")
    else:
        st.warning("请提供目标的姓名。")

# Display the current target_id
st.markdown("### 当前目标")
if st.session_state.target_id and st.session_state.name:
    st.success(f"目标ID: {st.session_state.target_id}")
    st.info(f"姓名: {st.session_state.name}")
else:
    st.warning("尚未选择或创建目标。")

# Input for the current conversation
current_convo = st.text_area("当前对话", placeholder="输入当前的对话内容...")

# Button to submit the love analysis
if st.button("分析恋爱状况"):
    if current_convo and st.session_state.target_id:
        try:
            response = requests.post(
                "https://poc2-168m.onrender.com/love_analysis/",
                json={"convo": current_convo, "target_id": st.session_state.target_id,},
            )
            if response.status_code == 200:
                st.session_state.analysis_result = response.json()
                st.success("恋爱分析成功完成！")
            else:
                st.error(f"错误: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"请求失败: {e}")
    else:
        st.warning("请先创建目标并填写当前对话内容！")

# Button to generate chat strategy
if st.button("生成聊天策略"):
    if st.session_state.target_id:
        try:
            response = requests.post(
                "https://poc2-168m.onrender.com/chat_strategies/",
                json={"target_id": st.session_state.target_id},
            )
            if response.status_code == 200:
                st.session_state.strategy_result = response.json()
                st.success("聊天策略生成成功！")
            else:
                st.error(f"错误: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"请求失败: {e}")
    else:
        st.warning("请先创建目标后再生成聊天策略！")


if st.button("获取回复选项"):
    if current_convo and st.session_state.target_id:
        try:
            response = requests.post(
                "https://poc2-168m.onrender.com/reply_options_flow/",
                json={"target_id": st.session_state.target_id, "convo": current_convo},
            )
            if response.status_code == 200:
                st.session_state.reply_options_flow_result = response.json()
                st.success("回复选项生成成功！")
            else:
                st.error(f"错误: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"请求失败: {e}")
    else:
        st.warning("请先创建目标并填写当前对话内容后再生成回复选项！")

# Display the analysis result
if st.session_state.analysis_result:
    with st.container():
        st.subheader("恋爱分析结果")
        st.markdown(st.session_state.analysis_result["content"])

# Display the chat strategy result
if st.session_state.strategy_result:
    with st.container():
        st.subheader("聊天策略结果")
        st.markdown(st.session_state.strategy_result["content"])

# Display the reply options flow result with individual rows for options
if st.session_state.reply_options_flow_result:
    with st.container():
        st.subheader("回复选项结果")
        reply_options = st.session_state.reply_options_flow_result
        st.markdown("### 回复选项:")
        for i, option in enumerate(reply_options.values(), 1):
            st.markdown(f"**选项 {i}:** {option}")

# Footer
st.markdown("---")
st.caption("由 FastAPI 和 Streamlit 提供支持")
