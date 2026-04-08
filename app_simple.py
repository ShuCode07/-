import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import base64

# 初始化session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'dormitory' not in st.session_state:
    st.session_state.dormitory = None
if 'class_info' not in st.session_state:
    st.session_state.class_info = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None

# 统一的数据处理函数
def process_uploaded_data(df):
    """处理上传的数据，检测能耗相关列并返回统计信息"""
    result = {
        'data': df.copy(),
        'energy_columns': [],
        'date_columns': [],
        'water_columns': [],
        'gas_columns': [],
        'heat_columns': [],
        'area_columns': [],
        'total_energy': 0,
        'total_water': 0,
        'total_gas': 0,
        'total_heat': 0,
        'data_rows': len(df),
        'available': False
    }
    
    # 常见的能耗相关列名关键词
    energy_keywords = ['能耗', '电量', 'kWh', '用电量', '用电', '电力', 'energy', 'power', 'electricity', '电']
    water_keywords = ['水量', '水', 'water', 'm³', '吨']
    gas_keywords = ['气量', '气', '天然气', 'gas']
    heat_keywords = ['热量', '热', 'heat', 'GJ']
    date_keywords = ['日期', '时间', 'date', 'time', 'datetime']
    area_keywords = ['区域', '建筑', '宿舍', '房间', 'area', 'building', 'dorm']
    
    # 检测列名
    for col in df.columns:
        col_lower = col.lower()
        for keyword in energy_keywords:
            if keyword in col_lower:
                result['energy_columns'].append(col)
                break
        for keyword in water_keywords:
            if keyword in col_lower:
                result['water_columns'].append(col)
                break
        for keyword in gas_keywords:
            if keyword in col_lower:
                result['gas_columns'].append(col)
                break
        for keyword in heat_keywords:
            if keyword in col_lower:
                result['heat_columns'].append(col)
                break
        for keyword in date_keywords:
            if keyword in col_lower:
                result['date_columns'].append(col)
                break
        for keyword in area_keywords:
            if keyword in col_lower:
                result['area_columns'].append(col)
                break
    
    # 计算统计数据
    for energy_col in result['energy_columns']:
        try:
            df[energy_col] = pd.to_numeric(df[energy_col], errors='coerce')
            result['total_energy'] += df[energy_col].sum()
        except:
            pass
    
    for water_col in result['water_columns']:
        try:
            df[water_col] = pd.to_numeric(df[water_col], errors='coerce')
            result['total_water'] += df[water_col].sum()
        except:
            pass
    
    for gas_col in result['gas_columns']:
        try:
            df[gas_col] = pd.to_numeric(df[gas_col], errors='coerce')
            result['total_gas'] += df[gas_col].sum()
        except:
            pass
    
    for heat_col in result['heat_columns']:
        try:
            df[heat_col] = pd.to_numeric(df[heat_col], errors='coerce')
            result['total_heat'] += df[heat_col].sum()
        except:
            pass
    
    # 检查是否有有效数据
    result['available'] = len(result['energy_columns']) > 0 or len(result['water_columns']) > 0 or len(result['gas_columns']) > 0 or len(result['heat_columns']) > 0
    
    return result

# 获取默认模拟数据
def get_default_data():
    """返回默认的模拟数据"""
    date_range = pd.date_range(start='2024-01-10', end='2024-01-31')
    default_data = {
        '日期': [d.strftime('%m月%d日') for d in date_range],
        '日期_full': date_range,
        '电量 (kWh)': [1350, 1320, 1290, 1270, 1260, 1258, 1255, 1250, 1245, 1240, 1235, 1230, 1225, 1220, 1215, 1210, 1205, 1200, 1195, 1190, 1185, 1180],
        '水量 (吨)': [350, 345, 340, 335, 330, 324, 320, 315, 310, 305, 300, 295, 290, 285, 280, 275, 270, 265, 260, 255, 250, 245],
        '气量 (m³)': [170, 168, 165, 162, 158, 156, 154, 152, 150, 148, 146, 144, 142, 140, 138, 136, 134, 132, 130, 128, 126, 124],
        '热量 (GJ)': [950, 940, 930, 920, 905, 892, 885, 880, 875, 870, 865, 860, 855, 850, 845, 840, 835, 830, 825, 820, 815, 810]
    }
    return pd.DataFrame(default_data)

# 模拟用户数据
users = {
    'admin': {'password': '12345678', 'role': '管理者', 'name': '管理员'},
    'zhangshan': {'password': '12345678', 'role': '学生', 'dormitory': '1号楼101', 'name': '张三'},
    'wang': {'password': '12345678', 'role': '老师', 'class_info': '23级财务管理01班,23级财务管理02班', 'name': '王老师'},
    'deng': {'password': '12345678', 'role': '老师', 'class_info': '22级会计01班,22级会计02班', 'name': '邓老师'}
}

# 登录页面
def login_page():
    st.set_page_config(
        page_title="校园能耗监测与智能节能系统 - 登录",
        page_icon="📊",
        layout="centered"
    )
    
    # 使用markdown代替title，以便更好地控制显示
    st.markdown("""
    <div style='text-align: center;'>
        <h1 style='display: inline-flex; align-items: center; gap: 10px;'>
            <span>🔐</span>
            <span>校园能耗监测与智能节能系统登录页面</span>
        </h1>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <h2 style='text-align: center;'>欢迎使用，校园能耗监测与智能节能系统</h2>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div style='background-color: #f0f8ff; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
            <h3 style='margin: 0 0 12px 0; color: #1890ff;'>系统功能</h3>
            <ul style='margin: 0; padding-left: 20px;'>
                <li>水电气热综合监测</li>
                <li>智能节能调控</li>
                <li>碳积分小程序</li>
                <li>AI实时分析</li>
                <li>数据上传与管理</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("用户名")
            password = st.text_input("密码", type="password")
            
            submitted = st.form_submit_button("登录", type="primary")
            
            if submitted:
                if username in users and users[username]['password'] == password:
                    st.session_state.logged_in = True
                    st.session_state.user_role = users[username]['role']
                    st.session_state.username = username
                    st.session_state.dormitory = users[username].get('dormitory')
                    st.session_state.class_info = users[username].get('class_info')
                    st.session_state.user_name = users[username].get('name')
                    st.success("登录成功！正在跳转...")
                    # 刷新页面以显示相应的用户页面
                    st.rerun()
                else:
                    st.error("用户名或密码错误，请检查后重试")
    
    st.markdown("---")
    st.markdown("### 测试账号")
    st.markdown("**管理者**: admin / 12345678")
    st.markdown("**学生**: zhangshan / 12345678")
    st.markdown("**老师**: wang / 12345678 (王老师 - 23级财务管理01班,23级财务管理02班)")
    st.markdown("**老师**: deng / 12345678 (邓老师 - 22级会计01班,22级会计02班)")

# 模拟节能打卡数据
checkin_data = [
    {'日期': '2024-01-15', '学生': '张三', '宿舍': '1号楼101', '班级': '23级财务管理01班', '积分': 10, '行为': '关灯节能'},
    {'日期': '2024-01-14', '学生': '李四', '宿舍': '1号楼102', '班级': '23级财务管理02班', '积分': 10, '行为': '关空调节能'},
    {'日期': '2024-01-13', '学生': '张三', '宿舍': '1号楼101', '班级': '23级财务管理01班', '积分': 10, '行为': '关水龙头'},
    {'日期': '2024-01-12', '学生': '李四', '宿舍': '1号楼102', '班级': '23级财务管理02班', '积分': 10, '行为': '关灯节能'},
    {'日期': '2024-01-11', '学生': '张三', '宿舍': '1号楼101', '班级': '23级财务管理01班', '积分': 10, '行为': '关空调节能'}
]

# 导出功能
def get_csv_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">下载CSV文件</a>'
    return href

# 学生页面
def student_page():
    st.title("🎓 学生个人中心")
    st.markdown(f"## 欢迎回来，{st.session_state.user_name}同学！")
    
    # 初始化连续打卡状态
    if 'checkin_streak' not in st.session_state:
        st.session_state.checkin_streak = 5  # 模拟连续打卡5天
    if 'last_checkin_date' not in st.session_state:
        st.session_state.last_checkin_date = '2024-01-15'  # 模拟最后打卡日期
    
    # 导航栏 - 横排tab
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["个人中心", "寝室能耗", "耗能排名", "节能建议", "节能打卡", "积分兑换"])
    
    # 登出按钮
    if st.button("登出", type="secondary", key="logout"):
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.session_state.username = None
        st.session_state.dormitory = None
        st.session_state.user_name = None
        st.rerun()
    
    with tab1:
        # 个人中心首页
        # 一键打卡快捷入口
        st.subheader("🚀 一键打卡")
        
        # 连续打卡信息
        col1, col2 = st.columns(2, gap="medium")
        
        with col1:
            st.markdown(f"""
            <div style='background-color: #f0f8ff; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #1890ff;'>连续打卡</h4>
                <p style='margin: 0; font-size: 24px; font-weight: bold;'>{st.session_state.checkin_streak} 天</p>
                <p style='margin: 8px 0 0 0; font-size: 14px; color: #52c41a;'>距离额外奖励还需 {7 - st.session_state.checkin_streak} 天</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background-color: #f0f8ff; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #1890ff;'>今日打卡</h4>
                <p style='margin: 0 0 16px 0; font-size: 16px;'>{"已完成" if st.session_state.last_checkin_date == '2024-01-16' else "未完成"}</p>
                <button style='background-color: #1890ff; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-size: 16px;'>
                    {"打卡完成" if st.session_state.last_checkin_date == '2024-01-16' else "立即打卡"}
                </button>
            </div>
            """, unsafe_allow_html=True)
        
        # 打卡日历
        st.subheader("📅 打卡日历")
        
        # 模拟打卡日历数据
        calendar_data = {
            '1月10日': '✓', '1月11日': '✓', '1月12日': '✓', '1月13日': '✓', '1月14日': '✓',
            '1月15日': '✓', '1月16日': ' ', '1月17日': ' ', '1月18日': ' ', '1月19日': ' ',
            '1月20日': ' ', '1月21日': ' ', '1月22日': ' ', '1月23日': ' ', '1月24日': ' '
        }
        
        # 显示打卡日历
        days = list(calendar_data.keys())
        
        # 第一行（7天）
        if len(days) >= 7:
            cols = st.columns(7)
            for i, day in enumerate(days[:7]):
                with cols[i]:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 8px; border-radius: 8px; background-color: {'#e6f7ff' if calendar_data[day] == '✓' else '#f5f5f5'};'>
                        <p style='margin: 0; font-size: 14px;'>{day.split('月')[1]}</p>
                        <p style='margin: 4px 0 0 0; font-size: 18px; font-weight: bold; color: #1890ff;'>{calendar_data[day]}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # 第二行（剩余天数，最多7天）
        if len(days) > 7:
            cols = st.columns(7)
            remaining_days = days[7:14]  # 只取最多7天
            for i, day in enumerate(remaining_days):
                with cols[i]:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 8px; border-radius: 8px; background-color: {'#e6f7ff' if calendar_data[day] == '✓' else '#f5f5f5'};'>
                        <p style='margin: 0; font-size: 14px;'>{day.split('月')[1]}</p>
                        <p style='margin: 4px 0 0 0; font-size: 18px; font-weight: bold; color: #1890ff;'>{calendar_data[day]}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # 个人信息
        st.subheader("👤 个人信息")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='background-color: #f0f8ff; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #1890ff;'>基本信息</h4>
                <p><strong>姓名:</strong> {}</p>
                <p><strong>宿舍:</strong> {}</p>
                <p><strong>角色:</strong> 学生</p>
                <p><strong>年级:</strong> 23级</p>
                <p><strong>班级:</strong> 财务管理01班</p>
                <p><strong>学号:</strong> 20230123</p>
            </div>
            """
            .format(st.session_state.user_name, st.session_state.dormitory), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background-color: #e3f2fd; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #1976D2;'>积分信息</h4>
                <p><strong>当前积分:</strong> 850</p>
                <p><strong>本月获得:</strong> 120</p>
                <p><strong>本月积分排名:</strong> 第3名</p>
                <p><strong>总积分排名:</strong> 第5名</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        # 寝室能耗
        st.subheader("🏠 寝室能耗")
        
        # 时段筛选
        time_period = st.selectbox(
            "选择时段",
            options=["近7天", "近14天", "近30天", "自定义"],
            index=0
        )
        
        # 构建完整的日期数据
        date_range = pd.date_range(start='2024-01-10', end='2024-01-31')
        energy_data = {
            '日期': [d.strftime('%m月%d日') for d in date_range],
            '日期_full': date_range,
            '电量 (kWh)': [5.2, 4.8, 4.5, 4.2, 3.8, 3.5, 3.3, 3.2, 3.0, 2.9, 2.8, 2.7, 2.6, 2.5, 2.4, 2.3, 2.2, 2.1, 2.0, 1.9, 1.8, 1.7],
            '水量 (吨)': [1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.7, 0.6, 0.6, 0.5, 0.5, 0.5, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.1]
        }
        df_energy = pd.DataFrame(energy_data)
        
        # 日期区间筛选
        start_date = None
        end_date = None
        if time_period == "自定义":
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("开始日期", value=pd.to_datetime('2024-01-10'))
            with col2:
                end_date = st.date_input("结束日期", value=pd.to_datetime('2024-01-15'))
        
        # 根据选择的时段过滤数据
        if time_period == "近7天":
            filtered_df = df_energy.head(7)
        elif time_period == "近14天":
            filtered_df = df_energy.head(14)
        elif time_period == "近30天":
            filtered_df = df_energy
        else:  # 自定义
            # 根据选择的日期区间过滤数据
            mask = (df_energy['日期_full'] >= pd.to_datetime(start_date)) & (df_energy['日期_full'] <= pd.to_datetime(end_date))
            filtered_df = df_energy[mask]
        
        # 生成图表标题
        if time_period == "自定义" and start_date and end_date:
            title = f"{st.session_state.dormitory} {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')} 能耗趋势"
        else:
            title = f"{st.session_state.dormitory} {time_period}能耗趋势"
        
        fig_energy = go.Figure()
        fig_energy.add_trace(go.Scatter(x=filtered_df['日期'], y=filtered_df['电量 (kWh)'], mode='lines+markers', name='电量'))
        fig_energy.add_trace(go.Scatter(x=filtered_df['日期'], y=filtered_df['水量 (吨)'], mode='lines+markers', name='水量'))
        fig_energy.update_layout(
            title=title,
            xaxis_title="日期",
            yaxis_title="消耗量",
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig_energy, use_container_width=True)
    
    with tab3:
        # 寝室耗能排名
        st.subheader("📊 寝室能耗排名")
        
        ranking_data = {
            '排名': [1, 2, 3, 4, 5, 6],
            '寝室': ['3号楼301', '1号楼103', '1号楼101', '2号楼202', '1号楼102', '2号楼201'],
            '当日能耗 (kWh)': [2.8, 3.2, 3.5, 3.8, 4.0, 4.2],
            '节能率': [35, 30, 25, 20, 15, 10]
        }
        df_ranking = pd.DataFrame(ranking_data)
        st.dataframe(df_ranking, use_container_width=True, hide_index=True)
    
    with tab4:
        # 节能建议
        st.subheader("💡 节能建议")
        
        suggestions = [
            "建议将空调温度设置在26℃，每提高1℃可节约10%的能耗",
            "离开宿舍时记得关闭所有电器，避免待机能耗",
            "使用节能灯具，可减少照明能耗30%以上",
            "合理安排用水时间，避免长流水",
            "建议在非高峰时段使用大功率电器"
        ]
        
        for i, suggestion in enumerate(suggestions, 1):
            st.markdown(f"**{i}. {suggestion}")
    
    with tab5:
        # 节能打卡
        st.subheader("✅ 节能打卡")
        
        # 添加奖励机制说明
        with st.expander("📝 奖励机制说明"):
            st.markdown("""
            ### 节能打卡奖励机制
            
            **一、基础积分**
            1. **日常打卡奖励**：每日完成节能打卡，即可获得 10 积分 / 天
            2. **连续打卡激励**：连续打卡满 7 天，额外奖励 10 积分
            
            **二、额外积分**
            1. **节能建议打卡**：以宿舍为单位，采纳并落实节能建议、完成对应打卡，即可获得 10 积分 / 次。单宿舍每周最多可获得 2 次奖励。
            2. **节能排名奖励**
               - **排名规则**：按宿舍能耗倒序排名（能耗越低，排名越靠前），公平体现节能成效。
               - **奖励周期**：每 2 周发放 1 次排名奖励，及时兑现节能成果。
               - **阶梯奖励标准**：
                 - 第 1 名宿舍：20 积分
                 - 第 2-3 名宿舍：15 积分
                 - 第 4-10 名宿舍：10 积分
                 - 第 11-20 名宿舍：5 积分
            """)
        
        with st.form("checkin_form"):
            action = st.selectbox("选择节能行为", ["关灯节能", "关空调节能", "关水龙头", "其他节能行为"])
            notes = st.text_area("备注")
            # 添加照片上传功能
            uploaded_file = st.file_uploader("上传照片（可选）", type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                st.image(uploaded_file, caption="上传的照片", width=200)
            submitted = st.form_submit_button("提交打卡", type="primary")
            
            if submitted:
                st.success("打卡成功！获得10积分奖励！")
                st.balloons()
        
        # 打卡记录
        st.subheader("📋 打卡记录")
        df_checkin = pd.DataFrame(checkin_data)
        filtered_checkin = df_checkin[df_checkin['学生'] == st.session_state.user_name]
        st.dataframe(filtered_checkin, use_container_width=True, hide_index=True)
    
    with tab6:
        # 积分兑换
        st.subheader("🎁 积分兑换")
        
        # 量化评分体系
        st.markdown("### 📊 节能量化评分体系")
        score_col1, score_col2, score_col3 = st.columns(3)
        with score_col1:
            st.metric("节能行为评分", "85分", "↑ 12分")
        with score_col2:
            st.metric("参与活动评分", "92分", "↑ 8分")
        with score_col3:
            st.metric("综合评分", "88分", "↑ 10分")
        
        # 评分明细
        st.markdown("#### 📋 评分明细")
        score_detail = {
            '评分项目': ['日常打卡', '能耗下降', '节能建议采纳', '参与活动', '连续打卡奖励', '排名奖励'],
            '得分': [30, 25, 15, 20, 10, 8],
            '满分': [30, 30, 20, 25, 15, 10],
            '说明': ['每日打卡得1分', '能耗下降5%得25分', '建议被采纳得15分', '参与活动得20分', '连续7天得10分', '排名前10得8分']
        }
        df_score = pd.DataFrame(score_detail)
        st.dataframe(df_score, use_container_width=True, hide_index=True)
        
        # 荣誉表彰
        st.markdown("### 🏆 荣誉表彰")
        honor_col1, honor_col2 = st.columns(2)
        
        with honor_col1:
            st.markdown("#### 🎖️ 我的荣誉")
            honors = [
                {"荣誉名称": "节能先锋", "获得时间": "2024-01", "级别": "校级"},
                {"荣誉名称": "环保达人", "获得时间": "2024-02", "级别": "院级"},
                {"荣誉名称": "绿色使者", "获得时间": "2024-03", "级别": "班级"}
            ]
            df_honors = pd.DataFrame(honors)
            st.dataframe(df_honors, use_container_width=True, hide_index=True)
        
        with honor_col2:
            st.markdown("#### 📈 荣誉进度")
            # 荣誉进度条
            st.progress(0.8, text="节能先锋（校级）- 80%")
            st.progress(0.6, text="环保卫士（市级）- 60%")
            st.progress(0.4, text="绿色大使（省级）- 40%")
        
        # 积分兑换商品
        st.markdown("### 🎁 积分兑换商品")
        col1, col2, col3 = st.columns(3, gap="medium")
        
        with col1:
            st.markdown("""
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #333;'>素拓0.1</h4>
                <p style='margin: 0 0 12px 0; font-size: 20px; font-weight: bold;'>300积分</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("兑换", key="exchange_1"):
                st.success("兑换成功！")
        
        with col2:
            st.markdown("""
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #333;'>劳动时长0.5</h4>
                <p style='margin: 0 0 12px 0; font-size: 20px; font-weight: bold;'>200积分</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("兑换", key="exchange_2"):
                st.success("兑换成功！")
        
        with col3:
            st.markdown("""
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #333;'>环保笔记本</h4>
                <p style='margin: 0 0 12px 0; font-size: 20px; font-weight: bold;'>150积分</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("兑换", key="exchange_3"):
                st.success("兑换成功！")
        
        # 积分排行榜
        st.markdown("### 🏅 积分排行榜")
        ranking_col1, ranking_col2 = st.columns(2)
        
        with ranking_col1:
            st.markdown("#### 📊 本周排行")
            weekly_ranking = {
                '排名': ['🥇', '🥈', '🥉', '4', '5'],
                '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
                '积分': [950, 880, 820, 790, 750],
                '班级': ['23级财务管理01班', '23级财务管理02班', '22级会计01班', '22级会计02班', '23级财务管理01班']
            }
            df_weekly = pd.DataFrame(weekly_ranking)
            st.dataframe(df_weekly, use_container_width=True, hide_index=True)
        
        with ranking_col2:
            st.markdown("#### 📊 本月排行")
            monthly_ranking = {
                '排名': ['🥇', '🥈', '🥉', '4', '5'],
                '姓名': ['李四', '张三', '王五', '赵六', '钱七'],
                '积分': [3200, 3100, 2950, 2800, 2700],
                '班级': ['23级财务管理02班', '23级财务管理01班', '22级会计01班', '22级会计02班', '23级财务管理01班']
            }
            df_monthly = pd.DataFrame(monthly_ranking)
            st.dataframe(df_monthly, use_container_width=True, hide_index=True)

# 老师页面
def teacher_page():
    st.title("👨‍🏫 教师管理中心")
    st.markdown(f"## 欢迎回来，{st.session_state.user_name}！")
    
    # 班级信息和筛选
    st.subheader("🏫 班级信息")
    classes = st.session_state.class_info.split(',')
    
    # 初始化会话状态用于存储选中的班级
    if 'selected_classes' not in st.session_state:
        st.session_state.selected_classes = classes
    
    # 班级筛选 - 在每个班级名称后面添加复选框
    st.subheader("🔍 班级筛选")
    selected_classes = []
    
    for cls in classes:
        # 检查该班级是否已在选中列表中
        is_selected = cls in st.session_state.selected_classes
        # 添加复选框
        if st.checkbox(cls, value=is_selected, key=f"class_{cls}"):
            selected_classes.append(cls)
    
    # 更新会话状态
    st.session_state.selected_classes = selected_classes
    
    # 显示选中的班级
    st.subheader("📋 选中的班级")
    if selected_classes:
        for cls in selected_classes:
            st.markdown(f"**管理班级**: {cls}")
    else:
        st.markdown("请至少选择一个班级")
    
    # 班级学生列表
    st.subheader("👥 班级学生列表")
    
    students_data = {
        '学号': ['2021001', '2021002', '2021003', '2021004', '2021005'],
        '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
        '班级': ['23级财务管理01班', '23级财务管理02班', '22级会计01班', '22级会计02班', '23级财务管理01班'],
        '宿舍': ['1号楼101', '1号楼102', '1号楼103', '2号楼201', '2号楼202'],
        '用电量 (kWh)': [3.5, 4.0, 2.8, 3.8, 3.2],
        '用水量 (吨)': [0.7, 0.8, 0.5, 0.9, 0.6],
        '当前积分': [850, 720, 900, 680, 750],
        '本月打卡次数': [12, 10, 15, 8, 11]
    }
    df_students = pd.DataFrame(students_data)
    
    # 根据筛选的班级过滤学生列表
    if selected_classes:
        filtered_students = df_students[df_students['班级'].isin(selected_classes)]
        st.dataframe(filtered_students, use_container_width=True, hide_index=True)
    else:
        st.dataframe(df_students, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # 班级能耗统计
    st.subheader("📊 班级能耗统计")
    
    # 日期区间筛选
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("开始日期", value=pd.to_datetime('2024-01-10'))
    with col2:
        end_date = st.date_input("结束日期", value=pd.to_datetime('2024-01-15'))
    
    # 构建完整的日期数据
    date_range = pd.date_range(start='2024-01-10', end='2024-01-31')
    class_energy_data = {
        '日期': [d.strftime('%m月%d日') for d in date_range],
        '日期_full': date_range,
        '总电量 (kWh)': [25.8, 24.2, 23.5, 22.8, 21.5, 20.8, 20.5, 20.2, 19.8, 19.5, 19.2, 18.8, 18.5, 18.2, 17.8, 17.5, 17.2, 16.8, 16.5, 16.2, 15.8, 15.5],
        '总水量 (吨)': [5.8, 5.5, 5.2, 4.9, 4.6, 4.3, 4.1, 4.0, 3.8, 3.6, 3.5, 3.4, 3.2, 3.1, 3.0, 2.9, 2.8, 2.7, 2.6, 2.5, 2.4, 2.3]
    }
    df_class_energy = pd.DataFrame(class_energy_data)
    
    # 根据选择的日期区间过滤数据
    mask = (df_class_energy['日期_full'] >= pd.to_datetime(start_date)) & (df_class_energy['日期_full'] <= pd.to_datetime(end_date))
    filtered_df = df_class_energy[mask]
    
    fig_class_energy = go.Figure()
    fig_class_energy.add_trace(go.Scatter(x=filtered_df['日期'], y=filtered_df['总电量 (kWh)'], mode='lines+markers', name='总电量'))
    fig_class_energy.add_trace(go.Scatter(x=filtered_df['日期'], y=filtered_df['总水量 (吨)'], mode='lines+markers', name='总水量'))
    fig_class_energy.update_layout(
        title=f"{', '.join(selected_classes) if selected_classes else '所有班级'} {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')} 能耗趋势",
        xaxis_title="日期",
        yaxis_title="消耗量",
        height=400,
        hovermode='x unified'
    )
    st.plotly_chart(fig_class_energy, use_container_width=True)
    
    st.markdown("---")
    
    # 节能打卡记录
    st.subheader("✅ 节能打卡记录")
    df_checkin = pd.DataFrame(checkin_data)
    st.dataframe(df_checkin, use_container_width=True, hide_index=True)
    
    # 导出打卡记录
    if st.button("导出打卡记录"):
        st.markdown(get_csv_download_link(df_checkin, "节能打卡记录.csv"), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 学生积分管理
    st.subheader("🎁 学生积分管理")
    
    points_data = {
        '学生': ['张三', '李四', '王五', '赵六', '钱七'],
        '班级': ['23级财务管理01班', '23级财务管理02班', '22级会计01班', '22级会计02班', '23级财务管理01班'],
        '当前积分': [850, 720, 900, 680, 750],
        '本月获得': [120, 100, 150, 80, 110],
        '累计打卡': [45, 38, 52, 32, 40]
    }
    df_points = pd.DataFrame(points_data)
    st.dataframe(df_points, use_container_width=True, hide_index=True)
    
    # 导出积分表
    if st.button("导出积分表"):
        st.markdown(get_csv_download_link(df_points, "学生积分表.csv"), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 学生信息导入
    st.subheader("📥 学生信息导入")
    st.markdown("请上传包含学生信息的Excel或CSV文件")
    uploaded_file = st.file_uploader("选择文件", type=["xlsx", "csv"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.success("文件上传成功！")
            st.dataframe(df, use_container_width=True)
            if st.button("导入学生信息"):
                st.success("学生信息导入成功！")
        except Exception as e:
            st.error(f"文件读取失败: {str(e)}")

# 管理者页面
def admin_page():
    st.set_page_config(
        page_title="校园能耗监测与智能节能系统",
        page_icon="📊",
        layout="wide"
    )
    st.title("📊 校园能耗监测与智能节能系统")
    st.markdown("## 校园水、电、气、热统一监测，AI实时分析 + 智能节能建议，哪里浪费一目了然！")
    
    # 导航栏
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["系统概览", "能耗监测与分析", "智能调控", "告警中心", "数据接口"])
    
    with tab1:
        # 系统概览
        st.subheader("🏠 系统概览")
        
        # 检查是否有用户上传的数据
        user_data_available = 'energy_df' in st.session_state and st.session_state.energy_df is not None
        
        if user_data_available:
            st.success("✅ 正在使用用户上传的数据进行分析")
            data_info = process_uploaded_data(st.session_state.energy_df)
            df = data_info['data']
        else:
            st.info("📊 使用默认模拟数据进行分析")
            df = get_default_data()
            data_info = process_uploaded_data(df)
        
        # 实时数据卡片
        st.markdown("### 📊 实时数据概览")
        col1, col2, col3, col4 = st.columns(4, gap="medium")
        
        # 显示电量数据
        with col1:
            energy_value = f"{data_info['total_energy']:.0f}" if data_info['total_energy'] > 0 else "1,258"
            st.markdown(f"""
            <div style='background-color: #f0f8ff; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #1890ff;'>总电量</h4>
                <p style='margin: 0; font-size: 24px; font-weight: bold;'>{energy_value} kWh</p>
                <p style='margin: 8px 0 0 0; font-size: 14px; color: #52c41a;'>↓ 12% 较昨日</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 显示水量数据
        with col2:
            water_value = f"{data_info['total_water']:.0f}" if data_info['total_water'] > 0 else "324"
            st.markdown(f"""
            <div style='background-color: #f0f8ff; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #1890ff;'>总水量</h4>
                <p style='margin: 0; font-size: 24px; font-weight: bold;'>{water_value} 吨</p>
                <p style='margin: 8px 0 0 0; font-size: 14px; color: #52c41a;'>↓ 8% 较昨日</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 显示气量数据
        with col3:
            gas_value = f"{data_info['total_gas']:.0f}" if data_info['total_gas'] > 0 else "156"
            st.markdown(f"""
            <div style='background-color: #f0f8ff; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #1890ff;'>总气量</h4>
                <p style='margin: 0; font-size: 24px; font-weight: bold;'>{gas_value} m³</p>
                <p style='margin: 8px 0 0 0; font-size: 14px; color: #52c41a;'>↓ 5% 较昨日</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 显示热量数据
        with col4:
            heat_value = f"{data_info['total_heat']:.0f}" if data_info['total_heat'] > 0 else "892"
            st.markdown(f"""
            <div style='background-color: #f0f8ff; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #1890ff;'>总热量</h4>
                <p style='margin: 0; font-size: 24px; font-weight: bold;'>{heat_value} GJ</p>
                <p style='margin: 8px 0 0 0; font-size: 14px; color: #52c41a;'>↓ 10% 较昨日</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 能耗趋势
        st.subheader("📈 能耗趋势")
        
        # 日期区间筛选
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("开始日期", value=pd.to_datetime('2024-01-10'))
        with col2:
            end_date = st.date_input("结束日期", value=pd.to_datetime('2024-01-15'))
        
        # 根据选择的日期区间过滤数据
        date_col = data_info['date_columns'][0] if data_info['date_columns'] else '日期_full'
        if date_col in df.columns:
            try:
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                mask = (df[date_col] >= pd.to_datetime(start_date)) & (df[date_col] <= pd.to_datetime(end_date))
                filtered_df = df[mask]
            except:
                filtered_df = df
        else:
            filtered_df = df
        
        # 电费趋势
        st.markdown("#### ⚡ 电费趋势")
        fig_energy = go.Figure()
        energy_col = data_info['energy_columns'][0] if data_info['energy_columns'] else '电量 (kWh)'
        if energy_col in filtered_df.columns:
            try:
                filtered_df[energy_col] = pd.to_numeric(filtered_df[energy_col], errors='coerce')
                fig_energy.add_trace(go.Scatter(
                    x=filtered_df.index, 
                    y=filtered_df[energy_col], 
                    mode='lines+markers', 
                    name=energy_col,
                    line=dict(color='#1890ff', width=2),
                    marker=dict(color='#1890ff')
                ))
            except:
                pass
        else:
            date_range = pd.date_range(start='2024-01-10', end='2024-01-31')
            fig_energy.add_trace(go.Scatter(
                x=[d.strftime('%m月%d日') for d in date_range], 
                y=[1350, 1320, 1290, 1270, 1260, 1258, 1255, 1250, 1245, 1240, 1235, 1230, 1225, 1220, 1215, 1210, 1205, 1200, 1195, 1190, 1185, 1180], 
                mode='lines+markers', 
                name='电量',
                line=dict(color='#1890ff', width=2),
                marker=dict(color='#1890ff')
            ))
        
        fig_energy.update_layout(
            title=f"电费趋势",
            xaxis_title="日期/序号",
            yaxis_title="电量 (kWh)",
            height=350,
            hovermode='x unified',
            showlegend=True
        )
        st.plotly_chart(fig_energy, use_container_width=True)
        
        # 水费趋势
        st.markdown("#### 💧 水费趋势")
        fig_water = go.Figure()
        water_col = data_info['water_columns'][0] if data_info['water_columns'] else '水量 (吨)'
        if water_col in filtered_df.columns:
            try:
                filtered_df[water_col] = pd.to_numeric(filtered_df[water_col], errors='coerce')
                fig_water.add_trace(go.Scatter(
                    x=filtered_df.index, 
                    y=filtered_df[water_col], 
                    mode='lines+markers', 
                    name=water_col,
                    line=dict(color='#52c41a', width=2),
                    marker=dict(color='#52c41a')
                ))
            except:
                pass
        else:
            date_range = pd.date_range(start='2024-01-10', end='2024-01-31')
            fig_water.add_trace(go.Scatter(
                x=[d.strftime('%m月%d日') for d in date_range], 
                y=[350, 345, 340, 335, 330, 324, 320, 315, 310, 305, 300, 295, 290, 285, 280, 275, 270, 265, 260, 255, 250, 245], 
                mode='lines+markers', 
                name='水量',
                line=dict(color='#52c41a', width=2),
                marker=dict(color='#52c41a')
            ))
        
        fig_water.update_layout(
            title=f"水费趋势",
            xaxis_title="日期/序号",
            yaxis_title="水量 (吨)",
            height=350,
            hovermode='x unified',
            showlegend=True
        )
        st.plotly_chart(fig_water, use_container_width=True)
        
    with tab2:
        # 能耗监测中心
        st.subheader("🔍 能耗监测中心")
        
        # 检查是否有用户上传的数据
        user_data_available = 'energy_df' in st.session_state and st.session_state.energy_df is not None
        
        if user_data_available:
            st.success("✅ 正在使用用户上传的数据进行分析")
            data_info = process_uploaded_data(st.session_state.energy_df)
            df = data_info['data']
        else:
            st.info("📊 使用默认模拟数据进行分析")
            df = get_default_data()
            data_info = process_uploaded_data(df)
        
        # 显示数据预览
        st.markdown("### 📋 数据预览")
        st.dataframe(df.head(10), use_container_width=True)
        
        # 实时数据采集状态
        st.markdown("### 📡 实时数据采集状态")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("在线设备", "156台", "↑ 3台")
        with col2:
            st.metric("数据更新频率", "5秒/次", "正常")
        with col3:
            st.metric("今日数据量", f"{data_info['data_rows']} 条", "↑ 15%")
        with col4:
            st.metric("数据完整性", "99.8%", "↑ 0.2%")
        
        # 多维度筛选
        st.markdown("### 🎯 多维度数据筛选")
        filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
        with filter_col1:
            time_range = st.selectbox("时间段", ["今日", "本周", "本月", "本季度", "本年", "自定义"])
        with filter_col2:
            if data_info['area_columns']:
                area_col = data_info['area_columns'][0]
                area_type = st.multiselect("区域类型", df[area_col].unique().tolist(), default=df[area_col].unique().tolist()[:2])
            else:
                area_type = st.multiselect("区域类型", ["教学楼", "宿舍楼", "办公楼", "食堂", "图书馆", "公共区域"], default=["教学楼", "宿舍楼"])
        with filter_col3:
            user_type = st.multiselect("用户类型", ["学生", "教职工", "管理人员"], default=["学生", "教职工"])
        with filter_col4:
            energy_type = st.selectbox("能耗类型", ["全部", "电能", "水能", "燃气", "热能"])
        
        # 能耗数据分析
        st.markdown("### ⚡ 能耗数据分析")
        
        # 能耗统计
        st.markdown("#### 📊 能耗统计")
        col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4, gap="small")
        
        with col_stats1:
            st.markdown(f"""
            <div style='background-color: #f0f8ff; padding: 16px; border-radius: 8px;'>
                <p style='margin: 0; font-size: 14px; color: #666;'>数据行数</p>
                <p style='margin: 4px 0 0 0; font-size: 20px; font-weight: bold; color: #1890ff;'>{data_info['data_rows']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 显示电量统计
        energy_col = data_info['energy_columns'][0] if data_info['energy_columns'] else '电量 (kWh)'
        if energy_col in df.columns:
            try:
                df[energy_col] = pd.to_numeric(df[energy_col], errors='coerce')
                total_energy = df[energy_col].sum()
                avg_energy = df[energy_col].mean()
                with col_stats2:
                    st.markdown(f"""
                    <div style='background-color: #f0f8ff; padding: 16px; border-radius: 8px;'>
                        <p style='margin: 0; font-size: 14px; color: #666;'>总{energy_col}</p>
                        <p style='margin: 4px 0 0 0; font-size: 20px; font-weight: bold; color: #1890ff;'>{total_energy:.2f}</p>
                    </div>
                    """, unsafe_allow_html=True)
            except:
                pass
        
        # 显示水量统计
        water_col = data_info['water_columns'][0] if data_info['water_columns'] else '水量 (吨)'
        if water_col in df.columns:
            try:
                df[water_col] = pd.to_numeric(df[water_col], errors='coerce')
                total_water = df[water_col].sum()
                with col_stats3:
                    st.markdown(f"""
                    <div style='background-color: #f0f8ff; padding: 16px; border-radius: 8px;'>
                        <p style='margin: 0; font-size: 14px; color: #666;'>总{water_col}</p>
                        <p style='margin: 4px 0 0 0; font-size: 20px; font-weight: bold; color: #1890ff;'>{total_water:.2f}</p>
                    </div>
                    """, unsafe_allow_html=True)
            except:
                pass
        
        # 显示平均能耗
        if energy_col in df.columns:
            try:
                avg_energy = df[energy_col].mean()
                with col_stats4:
                    st.markdown(f"""
                    <div style='background-color: #f0f8ff; padding: 16px; border-radius: 8px;'>
                        <p style='margin: 0; font-size: 14px; color: #666;'>平均{energy_col}</p>
                        <p style='margin: 4px 0 0 0; font-size: 20px; font-weight: bold; color: #1890ff;'>{avg_energy:.2f}</p>
                    </div>
                    """, unsafe_allow_html=True)
            except:
                pass
        
        # 能耗趋势
        st.markdown("#### 📈 能耗趋势")
        
        # 电费趋势
        st.markdown("##### ⚡ 电费趋势")
        fig_energy = go.Figure()
        if energy_col in df.columns:
            try:
                df[energy_col] = pd.to_numeric(df[energy_col], errors='coerce')
                fig_energy.add_trace(go.Scatter(
                    x=df.index, 
                    y=df[energy_col], 
                    mode='lines+markers', 
                    name=energy_col,
                    line=dict(color='#1890ff', width=2),
                    marker=dict(color='#1890ff')
                ))
                fig_energy.update_layout(
                    title='电费趋势',
                    xaxis_title='序号',
                    yaxis_title='电量 (kWh)',
                    height=300,
                    hovermode='x unified',
                    showlegend=True
                )
                st.plotly_chart(fig_energy, use_container_width=True)
            except Exception as e:
                st.warning(f"无法绘制电费趋势图: {str(e)}")
        else:
            st.warning("未检测到电费数据")
        
        # 水费趋势
        st.markdown("##### 💧 水费趋势")
        fig_water = go.Figure()
        if water_col in df.columns:
            try:
                df[water_col] = pd.to_numeric(df[water_col], errors='coerce')
                fig_water.add_trace(go.Scatter(
                    x=df.index, 
                    y=df[water_col], 
                    mode='lines+markers', 
                    name=water_col,
                    line=dict(color='#52c41a', width=2),
                    marker=dict(color='#52c41a')
                ))
                fig_water.update_layout(
                    title='水费趋势',
                    xaxis_title='序号',
                    yaxis_title='水量 (吨)',
                    height=300,
                    hovermode='x unified',
                    showlegend=True
                )
                st.plotly_chart(fig_water, use_container_width=True)
            except Exception as e:
                st.warning(f"无法绘制水费趋势图: {str(e)}")
        else:
            st.warning("未检测到水费数据")
        
        # 能耗分布
        st.markdown("#### 📊 能耗分布")
        
        # 电费分布
        st.markdown("##### ⚡ 电费分布")
        if energy_col in df.columns:
            try:
                fig = px.histogram(df, x=energy_col, title=f'{energy_col}分布', color_discrete_sequence=['#1890ff'])
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"电费分布图绘制失败: {str(e)}")
        else:
            st.warning("未检测到电费数据")
        
        # 水费分布
        st.markdown("##### 💧 水费分布")
        if water_col in df.columns:
            try:
                fig = px.histogram(df, x=water_col, title=f'{water_col}分布', color_discrete_sequence=['#52c41a'])
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"水费分布图绘制失败: {str(e)}")
        else:
            st.warning("未检测到水费数据")
        

        
        # 导出分析报告
        if st.button("导出分析报告"):
            st.success("分析报告已生成并下载！")
    
    with tab3:
        # 智能节能调控
        st.subheader("🎯 智能节能调控")
        
        # 检查是否有用户上传的数据
        user_data_available = 'energy_df' in st.session_state and st.session_state.energy_df is not None
        
        if user_data_available:
            st.success("✅ 正在使用用户上传的数据进行调控分析")
            data_info = process_uploaded_data(st.session_state.energy_df)
            df = data_info['data']
            
            # 基于数据的智能建议
            st.markdown("### 📊 基于数据的智能调控建议")
            
            if data_info['energy_columns']:
                energy_col = data_info['energy_columns'][0]
                try:
                    df[energy_col] = pd.to_numeric(df[energy_col], errors='coerce')
                    avg_energy = df[energy_col].mean()
                    max_energy = df[energy_col].max()
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"""
                        <div style='background-color: #f0f8ff; padding: 16px; border-radius: 8px;'>
                            <p style='margin: 0; font-size: 14px; color: #666;'>平均能耗</p>
                            <p style='margin: 4px 0 0 0; font-size: 20px; font-weight: bold; color: #1890ff;'>{avg_energy:.2f} kWh</p>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                        <div style='background-color: #f0f8ff; padding: 16px; border-radius: 8px;'>
                            <p style='margin: 0; font-size: 14px; color: #666;'>最高能耗</p>
                            <p style='margin: 4px 0 0 0; font-size: 20px; font-weight: bold; color: #ff4d4f;'>{max_energy:.2f} kWh</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # 节能建议
                    st.info("💡 建议：根据数据分析，建议在高能耗时段降低空调温度，关闭不必要的照明设备，预计可节省15%能耗。")
                except Exception as e:
                    st.warning(f"分析数据时出错: {str(e)}")
        else:
            st.info("📊 使用默认数据进行调控")
        
        # 空调控制
        st.subheader("❄️ 空调控制")
        
        col1, col2 = st.columns(2)
        with col1:
            temp = st.slider("设定温度 (℃)", 18, 30, 26)
        with col2:
            mode = st.selectbox("运行模式", ["制冷", "制热", "通风"])
        
        if st.button("应用空调设置"):
            st.success(f"空调设置已应用：{mode}模式，温度{temp}℃")
        
        # 照明控制
        st.subheader("💡 照明控制")
        
        lighting_zones = ["公共区域", "教室", "办公室", "宿舍"]
        for zone in lighting_zones:
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"{zone}照明")
            with col2:
                st.toggle("开启", key=zone)
        
        # 水泵控制
        st.subheader("💧 水泵控制")
        
        pump_speed = st.slider("水泵转速 (%)", 0, 100, 60)
        if st.button("应用水泵设置"):
            st.success(f"水泵设置已应用：转速{pump_speed}%")
    
    with tab4:
        # 能耗异常预警与告警中心
        st.subheader("🚨 能耗异常预警与告警中心")
        
        # 检查是否有用户上传的数据
        user_data_available = 'energy_df' in st.session_state and st.session_state.energy_df is not None
        
        if user_data_available:
            st.success("✅ 正在使用用户上传的数据进行告警分析")
            data_info = process_uploaded_data(st.session_state.energy_df)
            df = data_info['data']
            
            # 基于数据的告警分析
            st.markdown("### 📊 基于数据的告警分析")
            
            if data_info['energy_columns']:
                energy_col = data_info['energy_columns'][0]
                try:
                    df[energy_col] = pd.to_numeric(df[energy_col], errors='coerce')
                    
                    # 计算统计指标
                    avg_energy = df[energy_col].mean()
                    max_energy = df[energy_col].max()
                    std_energy = df[energy_col].std()
                    
                    # 检测异常值（超过平均值2个标准差）
                    threshold = avg_energy + 2 * std_energy
                    anomalies = df[df[energy_col] > threshold]
                    
                    # 检测高异常值（超过平均值3个标准差 - 一级告警）
                    critical_threshold = avg_energy + 3 * std_energy
                    critical_anomalies = df[df[energy_col] > critical_threshold]
                    
                    # 中等异常（2-3个标准差 - 二级告警）
                    warning_anomalies = df[(df[energy_col] > threshold) & (df[energy_col] <= critical_threshold)]
                    
                    # 轻微异常（1-2个标准差 - 三级告警）
                    info_threshold = avg_energy + 1 * std_energy
                    info_anomalies = df[(df[energy_col] > info_threshold) & (df[energy_col] <= threshold)]
                    
                    col1, col2, col3, col4 = st.columns(4, gap="small")
                    with col1:
                        st.markdown(f"""
                        <div style='background-color: #fff1f0; padding: 12px; border-radius: 6px;'>
                            <p style='margin: 0; font-size: 12px; color: #666;'>检测到异常</p>
                            <p style='margin: 2px 0 0 0; font-size: 18px; font-weight: bold; color: #ff4d4f;'>{len(anomalies)} 个</p>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                        <div style='background-color: #f0f8ff; padding: 12px; border-radius: 6px;'>
                            <p style='margin: 0; font-size: 12px; color: #666;'>异常阈值</p>
                            <p style='margin: 2px 0 0 0; font-size: 18px; font-weight: bold; color: #1890ff;'>{threshold:.2f}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"""
                        <div style='background-color: #f0f8ff; padding: 12px; border-radius: 6px;'>
                            <p style='margin: 0; font-size: 12px; color: #666;'>平均值</p>
                            <p style='margin: 2px 0 0 0; font-size: 18px; font-weight: bold; color: #1890ff;'>{avg_energy:.2f}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    with col4:
                        st.markdown(f"""
                        <div style='background-color: #f0f8ff; padding: 12px; border-radius: 6px;'>
                            <p style='margin: 0; font-size: 12px; color: #666;'>最大值</p>
                            <p style='margin: 2px 0 0 0; font-size: 18px; font-weight: bold; color: #ff4d4f;'>{max_energy:.2f}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    if len(anomalies) > 0:
                        st.warning(f"⚠️ 检测到 {len(anomalies)} 个异常数据点，建议进一步调查。")
                        with st.expander("查看异常数据详情"):
                            st.dataframe(anomalies, use_container_width=True)
                    
                    # 告警统计卡片（使用真实数据）
                    st.markdown("### 📊 告警统计")
                    col1, col2, col3 = st.columns(3, gap="medium")
                    
                    total_anomalies = len(anomalies)
                    critical_count = len(critical_anomalies)
                    warning_count = len(warning_anomalies)
                    info_count = len(info_anomalies)
                    
                    with col1:
                        st.markdown(f"""
                        <div style='background-color: #fff1f0; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                            <h4 style='margin: 0 0 12px 0; color: #ff4d4f;'>数据异常</h4>
                            <p style='margin: 0; font-size: 24px; font-weight: bold;'>{total_anomalies}</p>
                            <p style='margin: 8px 0 0 0; font-size: 14px; color: #ff4d4f;'>{critical_count}个一级 · {warning_count}个二级 · {info_count}个三级</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        data_rows = len(df)
                        anomaly_rate = (total_anomalies / data_rows * 100) if data_rows > 0 else 0
                        st.markdown(f"""
                        <div style='background-color: #f6ffed; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                            <h4 style='margin: 0 0 12px 0; color: #52c41a;'>数据总量</h4>
                            <p style='margin: 0; font-size: 24px; font-weight: bold;'>{data_rows}</p>
                            <p style='margin: 8px 0 0 0; font-size: 14px; color: #52c41a;'>异常率: {anomaly_rate:.1f}%</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        avg_anomaly_value = anomalies[energy_col].mean() if len(anomalies) > 0 else 0
                        st.markdown(f"""
                        <div style='background-color: #e6f7ff; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                            <h4 style='margin: 0 0 12px 0; color: #1890ff;'>平均异常值</h4>
                            <p style='margin: 0; font-size: 24px; font-weight: bold;'>{avg_anomaly_value:.2f}</p>
                            <p style='margin: 8px 0 0 0; font-size: 14px; color: #1890ff;'>超出阈值: {(avg_anomaly_value - threshold):.2f}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # 不合理能耗行为识别（使用真实数据）
                    st.markdown("### ⚠️ 异常数据详情")
                    if len(anomalies) > 0:
                        behavior_col1, behavior_col2 = st.columns(2)
                        
                        with behavior_col1:
                            st.markdown("#### 🔍 异常数据列表")
                            
                            # 根据异常值创建异常行为数据
                            abnormal_list = []
                            for idx, row in anomalies.iterrows():
                                value = row[energy_col]
                                if value > critical_threshold:
                                    level = '一级（严重）'
                                    suggestion = '立即检查设备'
                                elif value > threshold:
                                    level = '二级（警告）'
                                    suggestion = '调查异常原因'
                                else:
                                    level = '三级（注意）'
                                    suggestion = '关注后续数据'
                                
                                abnormal_list.append({
                                    '序号': idx + 1,
                                    '能耗值': f'{value:.2f}',
                                    '超出阈值': f'{(value - threshold):.2f}',
                                    '异常等级': level,
                                    '建议措施': suggestion
                                })
                            
                            df_abnormal = pd.DataFrame(abnormal_list)
                            
                            # 高亮显示异常程度
                            def highlight_abnormal(row):
                                if '一级' in row['异常等级']:
                                    return ['background-color: #fff1f0'] * len(row)
                                elif '二级' in row['异常等级']:
                                    return ['background-color: #fffbe6'] * len(row)
                                return ['background-color: #f6ffed'] * len(row)
                            
                            styled_abnormal = df_abnormal.style.apply(highlight_abnormal, axis=1)
                            st.dataframe(styled_abnormal, use_container_width=True, hide_index=True)
                        
                        with behavior_col2:
                            st.markdown("#### 📊 异常等级分布")
                            # 异常类型分布
                            level_counts = {
                                '一级（严重）': critical_count,
                                '二级（警告）': warning_count,
                                '三级（注意）': info_count
                            }
                            df_level_stats = pd.DataFrame({
                                '异常等级': list(level_counts.keys()),
                                '数量': list(level_counts.values())
                            })
                            df_level_stats = df_level_stats[df_level_stats['数量'] > 0]
                            
                            if len(df_level_stats) > 0:
                                fig_level = px.pie(df_level_stats, values='数量', names='异常等级', 
                                                     title='异常等级分布',
                                                     color_discrete_map={'一级（严重）': '#ff4d4f', '二级（警告）': '#faad14', '三级（注意）': '#52c41a'})
                                st.plotly_chart(fig_level, use_container_width=True)
                            
                            # 数据趋势提示
                            if total_anomalies > data_rows * 0.1:
                                st.warning(f"⚠️ 注意：异常数据占比超过10%（{anomaly_rate:.1f}%），建议全面检查数据采集系统。")
                            elif total_anomalies > 0:
                                st.info(f"💡 提示：共检测到 {total_anomalies} 个异常数据点，建议重点关注一级告警。")
                    
                    # 智能节能建议（使用真实数据）
                    st.markdown("### 💡 智能节能建议")
                    suggestion_col1, suggestion_col2 = st.columns(2)
                    
                    with suggestion_col1:
                        st.markdown("#### 🎯 基于数据的节能建议")
                        
                        suggestions = []
                        
                        # 根据能耗平均值生成建议
                        if avg_energy > 0:
                            suggestions.append({
                                "区域": "整体",
                                "建议": f"当前平均能耗为 {avg_energy:.2f}，建议对比历史数据，查找能耗上升原因",
                                "优先级": "高" if avg_energy > threshold else "中"
                            })
                        
                        # 根据最大值生成建议
                        if max_energy > critical_threshold:
                            suggestions.append({
                                "区域": "高能耗时段",
                                "建议": f"最大能耗值 {max_energy:.2f} 严重超出阈值，建议检查该时段设备运行情况",
                                "优先级": "高"
                            })
                        elif max_energy > threshold:
                            suggestions.append({
                                "区域": "高能耗时段",
                                "建议": f"最大能耗值 {max_energy:.2f} 超出阈值，建议优化该时段用能",
                                "优先级": "中"
                            })
                        
                        # 根据异常数量生成建议
                        if critical_count > 0:
                            suggestions.append({
                                "区域": "异常数据",
                                "建议": f"检测到 {critical_count} 个严重异常，建议立即核查数据准确性",
                                "优先级": "高"
                            })
                        
                        # 添加通用建议
                        suggestions.append({
                            "区域": "日常管理",
                            "建议": "建立能耗监控机制，定期分析能耗数据趋势",
                            "优先级": "中"
                        })
                        
                        if len(suggestions) > 0:
                            df_suggestions = pd.DataFrame(suggestions)
                            st.dataframe(df_suggestions, use_container_width=True, hide_index=True)
                        else:
                            st.info("🎉 数据表现良好，暂无特殊建议")
                    
                    with suggestion_col2:
                        st.markdown("#### 📈 节能潜力分析")
                        
                        # 计算节能潜力
                        if avg_energy > 0:
                            potential_saving_10 = avg_energy * 0.1 * len(df)
                            potential_saving_20 = avg_energy * 0.2 * len(df)
                            
                            effect_data = {
                                '措施': ['节能10%', '节能15%', '节能20%'],
                                '预计节能': [potential_saving_10, potential_saving_10 * 1.5, potential_saving_20],
                                '实施难度': ['低', '中', '高']
                            }
                            df_effect = pd.DataFrame(effect_data)
                            
                            fig_effect = px.bar(df_effect, x='措施', y='预计节能', 
                                               title='各措施预期节能效果', color='实施难度',
                                               color_discrete_map={'低': '#52c41a', '中': '#faad14', '高': '#f5222d'})
                            st.plotly_chart(fig_effect, use_container_width=True)
                        else:
                            st.info("请上传包含能耗数据的文件以查看节能分析")
                    
                    # 告警中心列表（使用真实数据）
                    st.subheader("📋 异常数据告警列表")
                    
                    if len(anomalies) > 0:
                        alarm_list = []
                        for idx, row in anomalies.iterrows():
                            value = row[energy_col]
                            if value > critical_threshold:
                                level = '一级'
                                status = '紧急'
                            elif value > threshold:
                                level = '二级'
                                status = '重要'
                            else:
                                level = '三级'
                                status = '一般'
                            
                            alarm_list.append({
                                '序号': idx + 1,
                                '告警等级': level,
                                '当前值': f'{value:.2f}',
                                '阈值': f'{threshold:.2f}',
                                '超出量': f'{(value - threshold):.2f}',
                                '处理状态': status,
                                '建议': '立即核查' if level == '一级' else '关注跟进'
                            })
                        
                        df_alarm = pd.DataFrame(alarm_list)
                        
                        # 告警等级颜色标记
                        def highlight_level(row):
                            if row['告警等级'] == '一级':
                                return ['background-color: #fff1f0'] * len(row)
                            elif row['告警等级'] == '二级':
                                return ['background-color: #fff7e6'] * len(row)
                            return ['background-color: #f6ffed'] * len(row)
                        
                        styled_alarm = df_alarm.style.apply(highlight_level, axis=1)
                        st.dataframe(styled_alarm, use_container_width=True, hide_index=True)
                    else:
                        st.success("🎉 数据表现良好，未检测到异常数据！")
                        
                except Exception as e:
                    st.warning(f"分析数据时出错: {str(e)}")
            else:
                st.info("未检测到能耗数据列，请确保上传的文件包含能耗相关数据")
        else:
            st.info("📊 请先在数据接口页面上传数据，以使用告警分析功能")
            
            # 使用默认数据展示
            st.markdown("### 📊 告警统计（示例）")
            col1, col2, col3 = st.columns(3, gap="medium")
            
            with col1:
                st.markdown("""
                <div style='background-color: #fff1f0; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                    <h4 style='margin: 0 0 12px 0; color: #ff4d4f;'>今日告警</h4>
                    <p style='margin: 0; font-size: 24px; font-weight: bold;'>12</p>
                    <p style='margin: 8px 0 0 0; font-size: 14px; color: #ff4d4f;'>3个紧急 · 5个重要 · 4个一般</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style='background-color: #f6ffed; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                    <h4 style='margin: 0 0 12px 0; color: #52c41a;'>本周告警</h4>
                    <p style='margin: 0; font-size: 24px; font-weight: bold;'>45</p>
                    <p style='margin: 8px 0 0 0; font-size: 14px; color: #52c41a;'>处理率: 85%</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div style='background-color: #e6f7ff; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                    <h4 style='margin: 0 0 12px 0; color: #1890ff;'>本月告警</h4>
                    <p style='margin: 0; font-size: 24px; font-weight: bold;'>128</p>
                    <p style='margin: 8px 0 0 0; font-size: 14px; color: #1890ff;'>平均处理时长: 2.5小时</p>
                </div>
                """, unsafe_allow_html=True)

    
    with tab5:
        # 数据接口
        st.subheader("🔌 数据接口")
        
        # 能耗数据导入导出
        st.subheader("📤 能耗数据导入导出")
        
        # 创建两列布局，使用一致的卡片样式
        col1, col2 = st.columns(2, gap="medium")
        
        # 数据导入卡片
        with col1:
            st.markdown("""
            <div style='background-color: #f0f8ff; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); height: 100%; display: flex; flex-direction: column;'>
                <div style='margin-bottom: 20px;'>
                    <h4 style='margin: 0 0 8px 0; color: #1890ff; font-size: 16px;'>数据导入</h4>
                    <p style='margin: 0; font-size: 14px; color: #666;'>支持Excel、CSV格式数据导入</p>
                </div>
                <div style='flex: 1;'></div>
            </div>
            """, unsafe_allow_html=True)
            
            # 初始化会话状态
            if 'energy_df' not in st.session_state:
                st.session_state.energy_df = None
            
            # 文件上传功能
            energy_uploaded_file = st.file_uploader(
                "选择能耗数据文件", 
                type=["xlsx", "csv"], 
                key="energy_upload",
                help="支持Excel和CSV格式，单个文件不超过200MB"
            )
            
            if energy_uploaded_file is not None:
                try:
                    if energy_uploaded_file.name.endswith('.csv'):
                        energy_df = pd.read_csv(energy_uploaded_file)
                    else:
                        energy_df = pd.read_excel(energy_uploaded_file)
                    st.success("能耗数据文件上传成功！")
                    # 保存到会话状态
                    st.session_state.energy_df = energy_df
                except Exception as e:
                    st.error(f"文件读取失败: {str(e)}")
        
        # 数据导出卡片
        with col2:
            st.markdown("""
            <div style='background-color: #f0f8ff; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); height: 100%; display: flex; flex-direction: column;'>
                <div style='margin-bottom: 20px;'>
                    <h4 style='margin: 0 0 8px 0; color: #1890ff; font-size: 16px;'>数据导出</h4>
                    <p style='margin: 0; font-size: 14px; color: #666;'>导出为Excel、CSV格式</p>
                </div>
                <div style='flex: 1; display: flex; align-items: center; justify-content: center;'>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 导出按钮功能
            if st.button("导出数据", key="export_data", type="primary"):
                if st.session_state.energy_df is not None:
                    # 生成导出数据
                    export_data = st.session_state.energy_df
                    st.markdown(get_csv_download_link(export_data, "能耗数据导出.csv"), unsafe_allow_html=True)
                    st.success("数据导出成功！")
                else:
                    st.warning("请先上传数据再导出")
        
        # 数据处理和分析区域（统一放在下方）
        if st.session_state.energy_df is not None:
            current_df = st.session_state.energy_df
            
            # 数据编辑功能
            with st.expander("✏️ 数据编辑", expanded=False):
                edited_df = st.data_editor(current_df, use_container_width=True)
                if st.button("保存修改", key="save_changes"):
                    st.session_state.energy_df = edited_df
                    st.success("数据修改保存成功！")
                    # 重新获取当前数据
                    current_df = st.session_state.energy_df
            
            # 自动分析功能
            with st.expander("📊 数据自动分析", expanded=True):
                st.success("✅ 正在分析上传的数据")
                
                # 显示数据预览
                st.markdown("### 📋 数据预览")
                st.dataframe(current_df.head(10), use_container_width=True)
                
                # 自动检测能耗相关列
                energy_columns = []
                date_columns = []
                
                # 常见的能耗相关列名
                energy_keywords = ['能耗', '电量', 'kWh', '用电量', '用电', '电力', 'energy', 'power', 'electricity', '电量 (kWh)', '用电量 (kWh)']
                date_keywords = ['日期', '时间', 'date', 'time', 'datetime', '日期_full']
                
                # 检测列名
                for col in current_df.columns:
                    col_lower = col.lower()
                    for keyword in energy_keywords:
                        if keyword in col_lower:
                            energy_columns.append(col)
                            break
                    for keyword in date_keywords:
                        if keyword in col_lower:
                            date_columns.append(col)
                            break
                
                # 显示检测结果
                st.markdown("### 🎯 列检测结果")
                col_detect1, col_detect2 = st.columns(2)
                with col_detect1:
                    st.markdown(f"""
                    <div style='background-color: #f0f8ff; padding: 16px; border-radius: 8px;'>
                        <p style='margin: 0 0 8px 0; font-size: 14px; color: #666; font-weight: 500;'>检测到的能耗列:</p>
                        <p style='margin: 0; font-size: 14px; color: #1890ff;'>{', '.join(energy_columns) if energy_columns else '未检测到'}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col_detect2:
                    st.markdown(f"""
                    <div style='background-color: #f0f8ff; padding: 16px; border-radius: 8px;'>
                        <p style='margin: 0 0 8px 0; font-size: 14px; color: #666; font-weight: 500;'>检测到的日期列:</p>
                        <p style='margin: 0; font-size: 14px; color: #1890ff;'>{', '.join(date_columns) if date_columns else '未检测到'}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 能耗统计
                if energy_columns:
                    st.markdown("### 能耗统计")
                    
                    # 使用卡片样式显示统计信息
                    col_stats1, col_stats2, col_stats3 = st.columns(3, gap="small")
                    
                    with col_stats1:
                        st.markdown(f"""
                        <div style='background-color: #f0f8ff; padding: 16px; border-radius: 8px;'>
                            <p style='margin: 0; font-size: 14px; color: #666;'>数据行数</p>
                            <p style='margin: 4px 0 0 0; font-size: 20px; font-weight: bold; color: #1890ff;'>{len(current_df)}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # 分析每个能耗列
                    for energy_col in energy_columns:
                        try:
                            # 尝试将列转换为数值
                            current_df[energy_col] = pd.to_numeric(current_df[energy_col], errors='coerce')
                            total_energy = current_df[energy_col].sum()
                            avg_energy = current_df[energy_col].mean()
                            max_energy = current_df[energy_col].max()
                            min_energy = current_df[energy_col].min()
                            
                            with col_stats2:
                                st.markdown(f"""
                                <div style='background-color: #f0f8ff; padding: 16px; border-radius: 8px;'>
                                    <p style='margin: 0; font-size: 14px; color: #666;'>总{energy_col}</p>
                                    <p style='margin: 4px 0 0 0; font-size: 20px; font-weight: bold; color: #1890ff;'>{total_energy:.2f}</p>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with col_stats3:
                                st.markdown(f"""
                                <div style='background-color: #f0f8ff; padding: 16px; border-radius: 8px;'>
                                    <p style='margin: 0; font-size: 14px; color: #666;'>平均{energy_col}</p>
                                    <p style='margin: 4px 0 0 0; font-size: 20px; font-weight: bold; color: #1890ff;'>{avg_energy:.2f}</p>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            # 额外统计信息
                            st.markdown("### 详细统计")
                            detail_col1, detail_col2, detail_col3, detail_col4 = st.columns(4, gap="small")
                            with detail_col1:
                                st.markdown(f"""
                                <div style='background-color: #f0f8ff; padding: 12px; border-radius: 6px;'>
                                    <p style='margin: 0; font-size: 12px; color: #666;'>最大值</p>
                                    <p style='margin: 2px 0 0 0; font-size: 16px; font-weight: bold; color: #1890ff;'>{max_energy:.2f}</p>
                                </div>
                                """, unsafe_allow_html=True)
                            with detail_col2:
                                st.markdown(f"""
                                <div style='background-color: #f0f8ff; padding: 12px; border-radius: 6px;'>
                                    <p style='margin: 0; font-size: 12px; color: #666;'>最小值</p>
                                    <p style='margin: 2px 0 0 0; font-size: 16px; font-weight: bold; color: #1890ff;'>{min_energy:.2f}</p>
                                </div>
                                """, unsafe_allow_html=True)
                            with detail_col3:
                                st.markdown(f"""
                                <div style='background-color: #f0f8ff; padding: 12px; border-radius: 6px;'>
                                    <p style='margin: 0; font-size: 12px; color: #666;'>标准差</p>
                                    <p style='margin: 2px 0 0 0; font-size: 16px; font-weight: bold; color: #1890ff;'>{current_df[energy_col].std():.2f}</p>
                                </div>
                                """, unsafe_allow_html=True)
                            with detail_col4:
                                st.markdown(f"""
                                <div style='background-color: #f0f8ff; padding: 12px; border-radius: 6px;'>
                                    <p style='margin: 0; font-size: 12px; color: #666;'>非空值</p>
                                    <p style='margin: 2px 0 0 0; font-size: 16px; font-weight: bold; color: #1890ff;'>{current_df[energy_col].count()}</p>
                                </div>
                                """, unsafe_allow_html=True)
                            break  # 只分析第一个找到的能耗列
                        except Exception as e:
                            st.error(f"分析{energy_col}列时出错: {str(e)}")
                            continue
                else:
                    st.warning("未检测到能耗相关列，请确保数据包含能耗数据列")
                
                # 简单可视化
                st.markdown("### 能耗趋势")
                if date_columns and energy_columns:
                    date_col = date_columns[0]
                    energy_col = energy_columns[0]
                    
                    try:
                        # 尝试将日期列转换为日期类型
                        current_df[date_col] = pd.to_datetime(current_df[date_col], errors='coerce')
                        
                        # 尝试将能耗列转换为数值
                        current_df[energy_col] = pd.to_numeric(current_df[energy_col], errors='coerce')
                        
                        # 绘制趋势图
                        fig = px.line(current_df, x=date_col, y=energy_col, title=f'{energy_col}趋势')
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.error(f"趋势图绘制失败: {str(e)}")
                else:
                    st.warning("未检测到日期列或能耗列，无法绘制趋势图")
                
                # 数据分布分析
                st.markdown("### 数据分布分析")
                if energy_columns:
                    energy_col = energy_columns[0]
                    try:
                        # 绘制直方图
                        fig = px.histogram(current_df, x=energy_col, title=f'{energy_col}分布')
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.error(f"分布图绘制失败: {str(e)}")
                
                # 数据质量分析
                st.markdown("### 数据质量分析")
                st.markdown(f"- 总数据行数: {len(current_df)}")
                st.markdown(f"- 缺失值数量: {current_df.isnull().sum().sum()}")
                st.markdown(f"- 缺失值占比: {current_df.isnull().sum().sum() / (len(current_df) * len(current_df.columns)) * 100:.2f}%")
                
                # 数据导入到系统
                st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                if st.button("导入到系统", key="import_to_system", type="primary"):
                    st.success("能耗数据已成功导入系统！")
                    # 这里可以添加将数据保存到数据库或文件的代码
        else:
            # 提示信息卡片
            st.markdown("""
            <div style='background-color: #f6ffed; border: 1px solid #b7eb8f; padding: 20px; border-radius: 8px; margin-top: 20px;'>
                <div style='display: flex; align-items: center;'>
                    <div style='margin-right: 12px;'>
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="#52c41a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            <path d="M9 12L11 14L15 10" stroke="#52c41a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </div>
                    <div>
                        <p style='margin: 0; font-size: 16px; color: #389e0d; font-weight: 500;'>请上传能耗数据文件开始分析</p>
                        <p style='margin: 4px 0 0 0; font-size: 14px; color: #52c41a;'>支持Excel和CSV格式的能耗数据文件</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        

        
        # 学生信息导入
        with st.expander("📥 学生信息导入", expanded=False):
            st.markdown("请上传包含学生信息的Excel或CSV文件")
            uploaded_file = st.file_uploader("选择文件", type=["xlsx", "csv"])
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    st.success("文件上传成功！")
                    st.dataframe(df, use_container_width=True)
                    if st.button("导入学生信息", type="primary"):
                        st.success("学生信息导入成功！")
                except Exception as e:
                    st.error(f"文件读取失败: {str(e)}")
        
        # 节能打卡记录导出
        with st.expander("✅ 节能打卡记录导出", expanded=False):
            df_checkin = pd.DataFrame(checkin_data)
            st.dataframe(df_checkin, use_container_width=True, hide_index=True)
            
            if st.button("导出打卡记录", type="primary"):
                st.markdown(get_csv_download_link(df_checkin, "节能打卡记录.csv"), unsafe_allow_html=True)
        
        # 积分表导出
        with st.expander("🎁 积分表导出", expanded=False):
            points_data = {
                '学生': ['张三', '李四', '王五', '赵六', '钱七'],
                '班级': ['23级财务管理01班', '23级财务管理02班', '22级会计01班', '22级会计02班', '23级财务管理01班'],
                '当前积分': [850, 720, 900, 680, 750],
                '本月获得': [120, 100, 150, 80, 110],
                '累计打卡': [45, 38, 52, 32, 40]
            }
            df_points = pd.DataFrame(points_data)
            st.dataframe(df_points, use_container_width=True, hide_index=True)
            
            if st.button("导出积分表", type="primary"):
                st.markdown(get_csv_download_link(df_points, "学生积分表.csv"), unsafe_allow_html=True)
        
        # 用户管理
        with st.expander("👥 用户管理", expanded=False):
            user_data = {
                '用户名': ['admin', 'student1', 'student2', 'teacher1', 'teacher2'],
                '姓名': ['管理员', '张三', '李四', '王老师', '李老师'],
                '角色': ['管理者', '学生', '学生', '老师', '老师'],
                '所属': ['系统', '1号楼101', '1号楼102', '计算机科学与技术1班', '电子信息工程2班']
            }
            df_users = pd.DataFrame(user_data)
            st.dataframe(df_users, use_container_width=True, hide_index=True)
            
            if st.button("导出用户管理表", type="primary"):
                st.markdown(get_csv_download_link(df_users, "用户管理表.csv"), unsafe_allow_html=True)
        
        # API接口信息
        with st.expander("🌐 API接口信息", expanded=False):
            st.markdown("""
            <div style='background-color: #f0f8ff; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #1890ff;'>API接口文档</h4>
                <p><strong>基础URL:</strong> http://localhost:8000/api</p>
                <p><strong>认证方式:</strong> JWT Token</p>
                <p><strong>主要接口:</strong></p>
                <ul style='margin: 0; padding-left: 20px;'>
                    <li>GET /api/energy - 获取能耗数据</li>
                    <li>POST /api/checkin - 提交节能打卡</li>
                    <li>GET /api/points - 获取积分信息</li>
                    <li>GET /api/users - 获取用户信息</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# 主程序
if __name__ == "__main__":
    if st.session_state.logged_in:
        if st.session_state.user_role == '管理者':
            admin_page()
        elif st.session_state.user_role == '学生':
            student_page()
        elif st.session_state.user_role == '老师':
            teacher_page()
    else:
        login_page()
