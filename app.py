import streamlit as st
import requests
import time

# Define the base URL for the API
BASE_URL = "https://poc2-168m.onrender.com"
# Title of the app
st.title("恋爱分析")

# Initialize session state
if "target_id" not in st.session_state:
    st.session_state.target_id = None
if "targets_list" not in st.session_state:
    st.session_state.targets_list = []  # List to store fetched targets
if "selected_target" not in st.session_state:
    st.session_state.selected_target = None  # Store details of selected target
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "strategy_result" not in st.session_state:
    st.session_state.strategy_result = None
if "reply_options_flow_result" not in st.session_state:
    st.session_state.reply_options_flow_result = None

# Fetch existing targets
def fetch_targets():
    try:
        response = requests.get(f"{BASE_URL}/targets/")
        if response.status_code == 200:
            st.session_state.targets_list = response.json()
        else:
            st.error(f"无法获取目标列表: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"请求失败: {e}")

# Call fetch_targets to populate dropdown
if "targets_list" in st.session_state and not st.session_state.targets_list:
    fetch_targets()

# Dropdown for switching targets
st.markdown("### 选择或创建目标")
target_options = ["创建新目标"] + [f"{target['id']}: {target['name']}" for target in st.session_state.targets_list]
selected_option = st.selectbox("选择目标", target_options)

# Logic for creating or editing a target
if selected_option == "创建新目标":
    st.markdown("#### 创建目标")
    name = st.text_input("目标姓名", placeholder="输入目标的姓名")
    gender = st.text_input("性别", placeholder="输入目标的性别")
    relationship_context = st.text_input("关系背景", placeholder="例如：朋友，同事")
    relationship_perception = st.text_input("关系感知", placeholder="例如：亲密，疏远")
    relationship_goals = st.text_input("关系目标", placeholder="例如：结婚，约会")
    relationship_goals_long = st.text_input("长期关系目标", placeholder="例如：生活在一起，结婚")
    personality = st.text_input("性格", placeholder="例如：外向，内向")
    language = st.text_input("语言", placeholder="例如：英语，西班牙语")
    
    create_target_button = st.button("创建目标")
    if create_target_button:
        if name:
            try:
                response = requests.post(
                    f"{BASE_URL}/targets/",
                    json={
                        "name": name,
                        "gender": gender,
                        "relationship_context": relationship_context,
                        "relationship_perception": relationship_perception,
                        "relationship_goals": relationship_goals,
                        "relationship_goals_long": relationship_goals_long,
                        "personality": personality,
                        "language": language,
                    },
                )
                if response.status_code == 200:
                    target_data = response.json()
                    st.session_state.target_id = target_data["id"]
                    st.success(f"目标创建成功！ID: {st.session_state.target_id}")
                    # Refresh target list
                    fetch_targets()
                else:
                    st.error(f"错误: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"请求失败: {e}")
        else:
            st.warning("请提供目标的姓名。")
else:
    # Extract target ID from selection
    target_id = int(selected_option.split(":")[0])
    st.session_state.target_id = target_id
    st.markdown("#### 编辑目标")
    
    # Fetch and display target details
    selected_target = next(target for target in st.session_state.targets_list if target["id"] == target_id)
    name = st.text_input("目标姓名", value=selected_target["name"])
    gender = st.text_input("性别", value=selected_target["gender"])
    relationship_context = st.text_input("关系背景", value=selected_target["relationship_context"])
    relationship_perception = st.text_input("关系感知", value=selected_target["relationship_perception"])
    relationship_goals = st.text_input("关系目标", value=selected_target["relationship_goals"])
    relationship_goals_long = st.text_input("长期关系目标", value=selected_target["relationship_goals_long"])
    personality = st.text_input("性格", value=selected_target["personality"])
    language = st.text_input("语言", value=selected_target["language"])
    
    update_target_button = st.button("更新目标")
    if update_target_button:
        try:
            response = requests.put(
                f"{BASE_URL}/targets/{target_id}",
                json={
                    "name": name,
                    "gender": gender,
                    "relationship_context": relationship_context,
                    "relationship_perception": relationship_perception,
                    "relationship_goals": relationship_goals,
                    "relationship_goals_long": relationship_goals_long,
                    "personality": personality,
                    "language": language,
                },
            )
            if response.status_code == 200:
                st.success("目标更新成功！")
                # Refresh target list
                fetch_targets()
            else:
                st.error(f"错误: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"请求失败: {e}")

# Input for the current conversation
current_convo = st.text_area("当前对话", placeholder="输入当前的对话内容...")

# Remaining logic stays unchanged for generating analysis, strategy, and reply options

# Unified button to handle the full flow
if st.button("生成恋爱分析、聊天策略和回复选项"):
    if current_convo and st.session_state.target_id:
        start_time = time.time()  # Start the timer
        try:
            # Step 1: Love Analysis
            st.info("正在生成恋爱分析...")
            love_analysis_response = requests.post(
                f"{BASE_URL}/love_analysis/",
                json={"convo": current_convo, "target_id": st.session_state.target_id},
            )
            if love_analysis_response.status_code == 200:
                st.session_state.analysis_result = love_analysis_response.json()
                st.success("恋爱分析成功完成！")
            else:
                st.error(f"恋爱分析失败: {love_analysis_response.status_code} - {love_analysis_response.text}")
                st.stop()

            # Step 2: Chat Strategy
            st.info("正在生成聊天策略...")
            chat_strategy_response = requests.post(
                f"{BASE_URL}/chat_strategies/",
                json={"target_id": st.session_state.target_id},
            )
            if chat_strategy_response.status_code == 200:
                st.session_state.strategy_result = chat_strategy_response.json()
                st.success("聊天策略生成成功！")
            else:
                st.error(f"聊天策略生成失败: {chat_strategy_response.status_code} - {chat_strategy_response.text}")
                st.stop()

            # Step 3: Reply Options
            st.info("正在生成回复选项...")
            reply_options_response = requests.post(
                f"{BASE_URL}/reply_options_flow/",
                json={"target_id": st.session_state.target_id, "convo": current_convo},
            )
            if reply_options_response.status_code == 200:
                st.session_state.reply_options_flow_result = reply_options_response.json()
                st.success("回复选项生成成功！")
            else:
                st.error(f"回复选项生成失败: {reply_options_response.status_code} - {reply_options_response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"请求失败: {e}")

        # Stop the timer and calculate the elapsed time
        end_time = time.time()
        elapsed_time = end_time - start_time
        st.info(f"生成完成！总耗时: {elapsed_time:.2f} 秒")
    else:
        st.warning("请先创建目标并填写当前对话内容！")

# Display the results
if st.session_state.analysis_result:
    with st.container():
        st.subheader("恋爱分析结果")
        st.markdown(st.session_state.analysis_result["content"])

if st.session_state.strategy_result:
    with st.container():
        st.subheader("聊天策略结果")
        st.markdown(st.session_state.strategy_result["content"])

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
