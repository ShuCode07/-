import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import random
import string
import json
import os

# 全局变量
checkin_data = []

# 用户数据文件路径
USERS_DATA_FILE = 'users_data.json'

# 积分数据文件路径
SCORES_DATA_FILE = 'scores_data.json'

# 默认用户数据
DEFAULT_USERS_DATA = {
    'admin': {'role': '管理者', 'name': '管理员', 'password': '12345678'},
    'zhangshan': {'role': '学生', 'name': '张三', 'password': '12345678', 'dormitory': '1号楼101'},
    'wang': {'role': '老师', 'name': '王老师', 'password': '12345678', 'classes': '23级财务管理01班,23级财务管理02班'},
    'deng': {'role': '老师', 'name': '邓老师', 'password': '12345678', 'classes': '22级会计01班,22级会计02班'}
}

# 默认积分数据
DEFAULT_SCORES_DATA = {
    'zhangshan': {'weekly_score': 950, 'monthly_score': 3100, 'class': '23级财务管理01班'}
}

# 虚拟用户数据（在一键清除后添加）
VIRTUAL_USERS_DATA = {
    'admin': {'role': '管理者', 'name': '管理员', 'password': '12345678'},
    'zhangshan': {'role': '学生', 'name': '张三', 'password': '12345678', 'dormitory': '1号楼101'},
    'wang': {'role': '辅导员', 'name': '王老师', 'password': '12345678', 'class_info': '2023级金融学2班,2023级金融工程2班', 'office': '1号楼201'},
    'deng': {'role': '辅导员', 'name': '邓老师', 'password': '12345678', 'class_info': '2023级会计学1班,2023级会计学2班', 'office': '1号楼202'}
}

# 虚拟积分数据（在一键清除后添加）
VIRTUAL_SCORES_DATA = {
    'zhangshan': {'weekly_score': 950, 'monthly_score': 3100, 'class': '2023级金融学2班'}
}

# 标记是否为虚拟数据的键
VIRTUAL_DATA_FLAG = '_is_virtual'


# 上传文件记录文件路径
UPLOADED_FILES_FILE = 'uploaded_files.json'

# 保存上传文件记录到文件
def save_uploaded_files(uploaded_files):
    try:
        with open(UPLOADED_FILES_FILE, 'w', encoding='utf-8') as f:
            json.dump(uploaded_files, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.warning(f"保存上传文件记录失败: {str(e)}")
        return False

# 从文件加载上传文件记录
def load_uploaded_files():
    if os.path.exists(UPLOADED_FILES_FILE):
        try:
            with open(UPLOADED_FILES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.warning(f"加载上传文件记录失败，使用空列表: {str(e)}")
            return []
    else:
        return []

# 保存用户数据到文件
def save_users_data(users_data):
    try:
        with open(USERS_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.warning(f"保存用户数据失败: {str(e)}")
        return False

# 从文件加载用户数据
def load_users_data():
    if os.path.exists(USERS_DATA_FILE):
        try:
            # 尝试使用UTF-8编码加载文件
            with open(USERS_DATA_FILE, 'r', encoding='utf-8') as f:
                users_data = json.load(f)
                # 检查数据是否完整
                if isinstance(users_data, dict) and len(users_data) > 0:
                    return users_data
                else:
                    st.warning("加载的用户数据为空，使用默认数据")
                    return DEFAULT_USERS_DATA.copy()
        except UnicodeDecodeError:
            # 如果UTF-8编码失败，尝试使用GBK编码
            try:
                with open(USERS_DATA_FILE, 'r', encoding='gbk') as f:
                    users_data = json.load(f)
                    if isinstance(users_data, dict) and len(users_data) > 0:
                        return users_data
                    else:
                        st.warning("加载的用户数据为空，使用默认数据")
                        return DEFAULT_USERS_DATA.copy()
            except Exception as e:
                st.warning(f"加载用户数据失败（GBK编码），使用默认数据: {str(e)}")
                return DEFAULT_USERS_DATA.copy()
        except Exception as e:
            st.warning(f"加载用户数据失败，使用默认数据: {str(e)}")
            return DEFAULT_USERS_DATA.copy()
    else:
        # 文件不存在，创建默认数据
        save_users_data(DEFAULT_USERS_DATA)
        return DEFAULT_USERS_DATA.copy()

# 保存积分数据到文件
def save_scores_data(scores_data):
    try:
        with open(SCORES_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(scores_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.warning(f"保存积分数据失败: {str(e)}")
        return False

# 从文件加载积分数据
def load_scores_data():
    if os.path.exists(SCORES_DATA_FILE):
        try:
            with open(SCORES_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.warning(f"加载积分数据失败，使用默认数据: {str(e)}")
            return DEFAULT_SCORES_DATA.copy()
    else:
        # 文件不存在，创建默认数据
        save_scores_data(DEFAULT_SCORES_DATA)
        return DEFAULT_SCORES_DATA.copy()

# 初始化积分数据
if 'scores_data' not in st.session_state:
    st.session_state.scores_data = load_scores_data()

# 初始化用户数据
if 'users_data' not in st.session_state:
    st.session_state.users_data = load_users_data()

# 初始化上传文件记录
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = load_uploaded_files()

# 生成随机密码函数
def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# 学生页面
def student_page():
    # 设置页面标题
    st.set_page_config(
        page_title="学生个人中心",
        page_icon="🎓",
        layout="wide"
    )
    
    # 侧边栏导航
    with st.sidebar:
        # 个人中心标题
        st.title("🎓 学生个人中心")
        st.markdown(f"### 欢迎回来，{st.session_state.user_name}同学！")
        
        # 搜索框（带内置放大镜）
        with st.form(key='search_form'):
            search_query = st.text_input("搜索功能", placeholder="搜索功能", key="student_search")
            search_submitted = st.form_submit_button("搜索")
        
        # 搜索功能实现
        if search_submitted and search_query:
            # 定义二级科目映射
            search_mapping = {
                "首页": "首页",
                "个人中心": "打卡中心",
                "个人打卡中心": "打卡中心",
                "打卡中心": "打卡中心",
                "积分兑换": "兑换中心",
                "兑换中心": "兑换中心",
                "积分排行榜": "积分排行榜",
                "排行榜": "积分排行榜",
                "寝室能耗": "寝室能耗",
                "耗能排名": "耗能排名",
                "节能建议": "节能行动",
                "节能打卡": "节能行动",
                "节能行动": "节能行动"
            }
            
            # 搜索匹配
            for key, value in search_mapping.items():
                if search_query.lower() in key.lower():
                    st.session_state.selected_page = value
                    st.rerun()
        
        # 初始化折叠状态
        if 'personal_management_expanded' not in st.session_state:
            st.session_state.personal_management_expanded = True
        if 'energy_management_expanded' not in st.session_state:
            st.session_state.energy_management_expanded = True
        if 'energy_action_expanded' not in st.session_state:
            st.session_state.energy_action_expanded = True
        
        # 检查是否所有科目都已展开
        all_expanded = st.session_state.personal_management_expanded and st.session_state.energy_management_expanded and st.session_state.energy_action_expanded
        
        # 一键折叠/展开按钮
        if st.button("一键折叠" if all_expanded else "一键展开"):
            new_state = not all_expanded
            st.session_state.personal_management_expanded = new_state
            st.session_state.energy_management_expanded = new_state
            st.session_state.energy_action_expanded = new_state
            st.rerun()
        
        # 首页按钮
        if st.button("🏠 首页", use_container_width=True):
            st.session_state.selected_page = "首页"
            st.rerun()
        
        # 功能分类 - 个人管理
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            <div style='margin-top: 20px;'>
                <h4 style='margin: 0 0 10px 0; display: flex; align-items: center;'>
                    <span style='color: #1890ff; margin-right: 8px;'>🏠</span>
                    个人管理
                </h4>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("▼" if st.session_state.personal_management_expanded else "▶", key="personal_management_toggle", use_container_width=True):
                st.session_state.personal_management_expanded = not st.session_state.personal_management_expanded
                st.rerun()
        
        # 个人管理功能
        if st.session_state.personal_management_expanded:
            if st.button("打卡中心", use_container_width=True):
                st.session_state.selected_page = "打卡中心"
                st.rerun()
            if st.button("兑换中心", use_container_width=True):
                st.session_state.selected_page = "兑换中心"
                st.rerun()
            if st.button("积分排行榜", use_container_width=True):
                st.session_state.selected_page = "积分排行榜"
                st.rerun()
        
        # 功能分类 - 节能能耗管理
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            <div style='margin-top: 20px;'>
                <h4 style='margin: 0 0 10px 0; display: flex; align-items: center;'>
                    <span style='color: #52c41a; margin-right: 8px;'>💡</span>
                    节能能耗管理
                </h4>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("▼" if st.session_state.energy_management_expanded else "▶", key="energy_management_toggle", use_container_width=True):
                st.session_state.energy_management_expanded = not st.session_state.energy_management_expanded
                st.rerun()
        
        # 节能能耗管理功能
        if st.session_state.energy_management_expanded:
            if st.button("寝室能耗", use_container_width=True):
                st.session_state.selected_page = "寝室能耗"
                st.rerun()
            if st.button("耗能排名", use_container_width=True):
                st.session_state.selected_page = "耗能排名"
                st.rerun()
            if st.button("异常打卡申诉", use_container_width=True):
                st.session_state.selected_page = "异常打卡申诉"
                st.rerun()
            if st.button("节能行动", use_container_width=True):
                st.session_state.selected_page = "节能行动"
                st.rerun()
        

        
        # 登出按钮
        if st.button("登出", type="secondary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_position = None
            st.session_state.username = None
            st.session_state.dormitory = None
            st.session_state.user_name = None
            st.session_state.selected_page = None
            st.rerun()
    
    # 初始化连续打卡状态
    if 'checkin_streak' not in st.session_state:
        st.session_state.checkin_streak = 5  # 模拟连续打卡5天
    if 'last_checkin_date' not in st.session_state:
        st.session_state.last_checkin_date = '2024-01-15'  # 模拟最后打卡日期
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "首页"
    # 初始化积分余额
    if 'current_points' not in st.session_state:
        st.session_state.current_points = 850  # 初始积分
    # 初始化兑换记录
    if 'exchange_history' not in st.session_state:
        st.session_state.exchange_history = []  # 兑换记录
    # 积分明细的初始化由登录逻辑处理
    
    # 首页页面
    if st.session_state.selected_page == "首页":
        # 计算排名
        scores_data = st.session_state.scores_data
        student_scores = []
        for username, score_info in scores_data.items():
            if 'weekly_score' in score_info and 'monthly_score' in score_info:
                student_scores.append({
                    'username': username,
                    'weekly_score': score_info['weekly_score'],
                    'monthly_score': score_info['monthly_score']
                })
        
        # 计算本月排名
        monthly_rank = None
        weekly_rank = None
        if student_scores and 'username' in st.session_state:
            # 按本月积分排序
            df_monthly = pd.DataFrame(student_scores).sort_values('monthly_score', ascending=False).reset_index(drop=True)
            df_monthly.index = df_monthly.index + 1
            for idx, row in df_monthly.iterrows():
                if row['username'] == st.session_state.username:
                    monthly_rank = idx
                    break
            
            # 按本周积分排序
            df_weekly = pd.DataFrame(student_scores).sort_values('weekly_score', ascending=False).reset_index(drop=True)
            df_weekly.index = df_weekly.index + 1
            for idx, row in df_weekly.iterrows():
                if row['username'] == st.session_state.username:
                    weekly_rank = idx
                    break
        
        # 首页 - 个人信息
        st.subheader("👤 个人信息")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style='background-color: #f0f8ff; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #1890ff;'>基本信息</h4>
                <p><strong>姓名:</strong> {st.session_state.user_name}</p>
                <p><strong>学号:</strong> {st.session_state.username}</p>
                <p><strong>宿舍:</strong> {st.session_state.dormitory}</p>
                <p><strong>职务:</strong> 学生</p>
                <p><strong>班级:</strong> {st.session_state.get('student_class', '未分配班级')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background-color: #e3f2fd; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #1976D2;'>积分信息</h4>
                <p><strong>当前积分:</strong> {st.session_state.get('current_points', 0)}</p>
                <p><strong>本周获得:</strong> {st.session_state.get('weekly_score', 0)}</p>
                <p><strong>本月获得:</strong> {st.session_state.get('monthly_score', 0)}</p>
                <p><strong>本周排名:</strong> 第{f' {weekly_rank} 名' if weekly_rank else ' 无数据'}</p>
                <p><strong>本月排名:</strong> 第{f' {monthly_rank} 名' if monthly_rank else ' 无数据'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 奖励机制说明
        st.markdown("---")
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
    
    # 打卡中心页面
    elif st.session_state.selected_page == "打卡中心":
        # 个人打卡中心首页
        
        # 一键打卡快捷入口
        st.subheader("🚀 一键打卡")
        
        # 连续打卡信息和打卡功能
        col1, col2 = st.columns([2, 2], gap="medium")
        
        with col1:
            st.markdown(f"""
            <div style='background-color: #f0f8ff; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #1890ff;'>连续打卡</h4>
                <p style='margin: 0; font-size: 24px; font-weight: bold;'>{st.session_state.checkin_streak} 天</p>
                <p style='margin: 8px 0 0 0; font-size: 14px; color: #52c41a;'>距离额外奖励还需 {7 - st.session_state.checkin_streak} 天</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # 打卡信息和今日打卡状态合并
            today = '2024-01-16'  # 模拟今天日期
            is_checked_in = st.session_state.last_checkin_date == today
            
            st.markdown(f"""
            <div style='background-color: #f0f8ff; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); height: 100%;'>
                <h4 style='margin: 0 0 12px 0; color: #1890ff;'>今日打卡</h4>
                <p style='margin: 0 0 16px 0; font-size: 16px;'>{"已完成" if is_checked_in else "未完成"}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 立即打卡功能
            if not is_checked_in:
                # 简化为一键打卡，不需要其他输入
                if st.button("立即打卡", type="primary", use_container_width=True):
                    # 记录打卡
                    today = '2024-01-16'  # 模拟今天日期
                    
                    # 更新打卡状态
                    st.session_state.last_checkin_date = today
                    st.session_state.checkin_streak += 1
                    
                    # 更新积分
                    points_to_add = 10
                    st.session_state.weekly_score += points_to_add
                    st.session_state.monthly_score += points_to_add
                    st.session_state.current_points = st.session_state.monthly_score
                    
                    # 记录打卡记录
                    if 'checkin_records' not in st.session_state:
                        st.session_state.checkin_records = []
                    
                    # 确保username变量有定义
                    username = st.session_state.get('username', '')
                    
                    checkin_record = {
                        'date': today,
                        'username': username,
                        'name': st.session_state.user_name,
                        'dormitory': st.session_state.dormitory,
                        'action': '节能打卡',
                        'points': points_to_add
                    }
                    st.session_state.checkin_records.append(checkin_record)
                    
                    # 保存打卡记录到文件
                    try:
                        with open('checkin_records.json', 'w', encoding='utf-8') as f:
                            json.dump(st.session_state.checkin_records, f, ensure_ascii=False, indent=2)
                    except Exception as e:
                        st.warning(f"保存打卡记录失败: {str(e)}")
                    
                    # 更新scores_data并保存
                    if 'username' in st.session_state:
                        username = st.session_state.username
                        if username in st.session_state.scores_data:
                            st.session_state.scores_data[username]['weekly_score'] = st.session_state.weekly_score
                            st.session_state.scores_data[username]['monthly_score'] = st.session_state.monthly_score
                        else:
                            st.session_state.scores_data[username] = {
                                'weekly_score': st.session_state.weekly_score,
                                'monthly_score': st.session_state.monthly_score,
                                'class': st.session_state.get('student_class', '未分配班级'),
                                'name': st.session_state.user_name
                            }
                        save_scores_data(st.session_state.scores_data)
                    
                    # 添加积分明细记录
                    import datetime
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.session_state.points_detail.append({
                        '时间': now,
                        '来源': '日常打卡',
                        '积分变动': f'+{points_to_add}',
                        '余额': st.session_state.current_points
                    })
                    
                    # 添加打卡记录到全局打卡数据
                    new_checkin = {
                        '日期': today,
                        '学生': st.session_state.user_name,
                        '宿舍': st.session_state.dormitory,
                        '班级': st.session_state.get('student_class', '23级财务管理01班'),
                        '积分': points_to_add,
                        '行为': '日常打卡'
                    }
                    checkin_data.append(new_checkin)
                    
                    # 保存打卡记录到session_state
                    if 'checkin_records' not in st.session_state:
                        st.session_state.checkin_records = []
                    
                    # 确保user_id变量有定义
                    user_id = st.session_state.get('username', st.session_state.get('user_id', ''))
                    
                    st.session_state.checkin_records.append({
                        '时间': now,
                        '姓名': st.session_state.user_name,
                        '学号': user_id,
                        '宿舍': st.session_state.dormitory,
                        '类型': '日常打卡',
                        '积分': f'+{points_to_add}'
                    })
                    
                    st.success(f"打卡成功！获得{points_to_add}积分奖励！")
                    st.balloons()
                    st.rerun()
            else:
                st.button("打卡完成", disabled=True, use_container_width=True)
        
        # 移除col3，因为已经合并到col2中
        
        # 打卡日历
        st.subheader("📅 打卡日历")
        
        # 初始化会话状态中的日期选择
        if 'current_year' not in st.session_state:
            st.session_state.current_year = 2024
        if 'current_month' not in st.session_state:
            st.session_state.current_month = 1
        
        # 年份和月份选择器
        col1, col2 = st.columns(2)
        with col1:
            # 使用number_input允许用户输入自定义年份
            st.session_state.current_year = st.number_input("选择年份", min_value=2000, max_value=2100, value=st.session_state.current_year, step=1)
        with col2:
            months = list(range(1, 13))  # 1-12月
            st.session_state.current_month = st.selectbox("选择月份", months, index=st.session_state.current_month - 1)
        
        # 生成当月日历数据
        import calendar
        cal = calendar.monthcalendar(st.session_state.current_year, st.session_state.current_month)
        
        # 模拟打卡数据（实际应用中应该从数据库或文件中加载）
        # 这里使用简单的模拟数据
        checked_days = set()
        # 添加一些模拟的打卡日期
        if st.session_state.current_year == 2024 and st.session_state.current_month == 1:
            checked_days.update([10, 11, 12, 13, 14, 15])
            # 如果今天已经打卡，添加今天
            if st.session_state.last_checkin_date == '2024-01-16':
                checked_days.add(16)
        
        # 显示星期标题
        week_days = ['日', '一', '二', '三', '四', '五', '六']
        cols = st.columns(7)
        for i, day in enumerate(week_days):
            with cols[i]:
                st.markdown(f"<div style='text-align: center; font-weight: bold; margin-bottom: 8px;'>{day}</div>", unsafe_allow_html=True)
        
        # 显示日历网格
        for week in cal:
            cols = st.columns(7)
            for i, day in enumerate(week):
                with cols[i]:
                    if day == 0:
                        # 空白单元格
                        st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
                    else:
                        # 检查是否打卡
                        is_checked = day in checked_days
                        bg_color = '#e6f7ff' if is_checked else '#f5f5f5'
                        check_mark = '✓' if is_checked else ''
                        
                        st.markdown(f"""
                        <div style='text-align: center; padding: 12px; border-radius: 8px; background-color: {bg_color}; height: 60px; display: flex; flex-direction: column; justify-content: center;'>
                            <p style='margin: 0; font-size: 16px;'>{day}日</p>
                            <p style='margin: 4px 0 0 0; font-size: 18px; font-weight: bold; color: #1890ff;'>{check_mark}</p>
                        </div>
                        """, unsafe_allow_html=True)
    
    # 寝室能耗页面
    elif st.session_state.selected_page == "寝室能耗":
        # 寝室能耗
        st.subheader("🏠 寝室能耗")
        
        # 时间选择 - 改为日期范围选择
        st.markdown("### 班级能耗统计")
        date_range = st.date_input(
            "选择日期范围", 
            value=(pd.to_datetime('2024-01-10'), pd.to_datetime('2024-01-15')),
            format="YYYY/MM/DD"
        )
        start_date, end_date = date_range
        
        # 构建完整的日期数据
        date_range = pd.date_range(start='2024-01-10', end='2024-01-31')
        energy_data = {
            '日期': [d.strftime('%m月%d日') for d in date_range],
            '日期_full': date_range,
            '电量 (kWh)': [5.2, 4.8, 4.5, 4.2, 3.8, 3.5, 3.3, 3.2, 3.0, 2.9, 2.8, 2.7, 2.6, 2.5, 2.4, 2.3, 2.2, 2.1, 2.0, 1.9, 1.8, 1.7],
            '水量 (吨)': [1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.7, 0.6, 0.6, 0.5, 0.5, 0.5, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.1]
        }
        df_energy = pd.DataFrame(energy_data)
        
        # 根据选择的日期区间过滤数据
        mask = (df_energy['日期_full'] >= pd.to_datetime(start_date)) & (df_energy['日期_full'] <= pd.to_datetime(end_date))
        filtered_df = df_energy[mask]
        
        # 生成图表标题
        title = f"{st.session_state.dormitory} {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')} 能耗趋势"
        
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
    
    # 耗能排名页面
    elif st.session_state.selected_page == "耗能排名":
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
    
    # 节能行动页面
    elif st.session_state.selected_page == "节能行动":
        # 节能行动
        st.subheader("🌱 节能行动")
        
        # 节能建议部分
        st.markdown("### 💡 节能建议")
        suggestions = [
            "建议将空调温度设置在26℃，每提高1℃可节约10%的能耗",
            "离开宿舍时记得关闭所有电器，避免待机能耗",
            "使用节能灯具，可减少照明能耗30%以上",
            "合理安排用水时间，避免长流水",
            "建议在非高峰时段使用大功率电器"
        ]
        
        for i, suggestion in enumerate(suggestions, 1):
            st.markdown(f"**{i}. {suggestion}")
        
        st.markdown("---")
        
        # 节能打卡部分
        st.markdown("### ✅ 节能打卡")
        
        # 打卡表单
        with st.form("checkin_form"):
            st.markdown("#### 选择节能行为")
            action = st.selectbox("", ["关灯节能", "关空调节能", "关水龙头", "其他节能行为"])
            
            st.markdown("#### 备注")
            notes = st.text_area("", placeholder="请输入备注信息...")
            
            st.markdown("#### 上传照片（可选）")
            uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])
            
            submitted = st.form_submit_button("提交打卡", type="primary", use_container_width=True)
            
            if submitted:
                # 检查今日节能打卡状态
                today = '2024-01-16'  # 模拟今天日期
                # 初始化节能打卡状态
                if 'last_energy_checkin_date' not in st.session_state:
                    st.session_state.last_energy_checkin_date = None
                is_energy_checked_in = st.session_state.last_energy_checkin_date == today
                
                if not is_energy_checked_in:
                    # 更新积分
                    points_to_add = 10
                    st.session_state.weekly_score += points_to_add
                    st.session_state.monthly_score += points_to_add
                    st.session_state.current_points = st.session_state.monthly_score
                    
                    # 更新scores_data并保存
                    if 'username' in st.session_state:
                        username = st.session_state.username
                        if username in st.session_state.scores_data:
                            st.session_state.scores_data[username]['weekly_score'] = st.session_state.weekly_score
                            st.session_state.scores_data[username]['monthly_score'] = st.session_state.monthly_score
                        else:
                            st.session_state.scores_data[username] = {
                                'weekly_score': st.session_state.weekly_score,
                                'monthly_score': st.session_state.monthly_score,
                                'class': st.session_state.get('student_class', '未分配班级'),
                                'name': st.session_state.user_name
                            }
                        save_scores_data(st.session_state.scores_data)
                    
                    # 添加积分明细记录
                    import datetime
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.session_state.points_detail.append({
                        '时间': now,
                        '来源': f'节能打卡-{action}',
                        '积分变动': f'+{points_to_add}',
                        '余额': st.session_state.current_points
                    })
                    
                    # 添加打卡记录到全局打卡数据
                    new_checkin = {
                        '日期': today,
                        '学生': st.session_state.user_name,
                        '宿舍': st.session_state.dormitory,
                        '班级': st.session_state.get('student_class', '23级财务管理01班'),
                        '积分': points_to_add,
                        '行为': action
                    }
                    checkin_data.append(new_checkin)
                    
                    # 保存打卡记录到session_state
                    if 'checkin_records' not in st.session_state:
                        st.session_state.checkin_records = []
                    
                    # 确保user_id变量有定义
                    user_id = st.session_state.get('username', st.session_state.get('user_id', ''))
                    
                    st.session_state.checkin_records.append({
                        '时间': now,
                        '姓名': st.session_state.user_name,
                        '学号': user_id,
                        '宿舍': st.session_state.dormitory,
                        '类型': f'节能打卡-{action}',
                        '积分': f'+{points_to_add}'
                    })
                    
                    # 更新节能打卡状态
                    st.session_state.last_energy_checkin_date = today
                    
                    st.success(f"节能打卡成功！获得{points_to_add}积分奖励！")
                    st.balloons()
                else:
                    st.info("今日节能打卡已完成，请勿重复打卡")
        
        # 打卡记录
        st.markdown("### 📋 打卡记录")
        df_checkin = pd.DataFrame(checkin_data)
        
        if not df_checkin.empty and '学生' in df_checkin.columns:
            filtered_checkin = df_checkin[df_checkin['学生'] == st.session_state.user_name]
            
            if not filtered_checkin.empty:
                st.dataframe(filtered_checkin, use_container_width=True, hide_index=True)
            else:
                st.markdown("暂无打卡记录")
        else:
            st.markdown("暂无打卡记录")
        
        # 积分明细
        st.markdown("### 📊 积分明细")
        if 'points_detail' in st.session_state:
            df_points = pd.DataFrame(st.session_state.points_detail)
            if not df_points.empty:
                st.dataframe(df_points, use_container_width=True, hide_index=True)
            else:
                st.markdown("暂无积分明细记录")
        else:
            st.markdown("暂无积分明细记录")
    
    # 兑换中心页面
    elif st.session_state.selected_page == "兑换中心":
        # 兑换中心
        st.subheader("🎁 兑换中心")
        
        # 显示当前总积分
        st.markdown(f"### ⭐ 目前总积分：{st.session_state.current_points}")
        
        # 积分明细（可折叠）
        with st.expander("📊 积分明细", expanded=False):
            df_points = pd.DataFrame(st.session_state.points_detail)
            st.dataframe(df_points, use_container_width=True, hide_index=True)
        
        # 量化评分体系
        st.markdown("### 📊 节能量化评分体系")
        score_col1, score_col2, score_col3 = st.columns(3)
        with score_col1:
            st.metric("参与活动评分", "92分", "↑ 8分")
        with score_col2:
            st.metric("日常打卡评分", "85分", "↑ 12分")
        with score_col3:
            st.metric("综合评分", "88分", "↑ 10分")
        

        
        # 积分兑换商品
        st.markdown("### 🎁 积分兑换商品")
        col1, col2 = st.columns(2, gap="medium")
        
        with col1:
            st.markdown("""
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #333;'>素拓0.1</h4>
                <p style='margin: 0 0 12px 0; font-size: 20px; font-weight: bold;'>300积分</p>
            </div>
            """, unsafe_allow_html=True)
            # 居中显示兑换按钮
            col1_align = st.columns([1, 2, 1])
            with col1_align[1]:
                if st.button("兑换", key="exchange_1", use_container_width=True):
                    if st.session_state.current_points >= 300:
                        # 扣除积分（只扣除当前积分，不影响周积分和月积分）
                        points_to_spend = 300
                        st.session_state.current_points -= points_to_spend
                        # 注意：不扣除周积分和月积分，这样积分排名只算增加和惩罚，不算兑换扣除的积分
                        
                        # 更新scores_data并保存（只更新用户信息，不更新积分）
                        if 'username' in st.session_state:
                            username = st.session_state.username
                            if username in st.session_state.scores_data:
                                # 保持原有的周积分和月积分不变
                                pass
                            else:
                                st.session_state.scores_data[username] = {
                                    'weekly_score': st.session_state.weekly_score,
                                    'monthly_score': st.session_state.monthly_score,
                                    'class': st.session_state.get('student_class', '未分配班级'),
                                    'name': st.session_state.user_name
                                }
                            save_scores_data(st.session_state.scores_data)
                        
                        # 记录兑换历史
                        import datetime
                        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        st.session_state.exchange_history.append({
                            '时间': now,
                            '商品': '素拓0.1',
                            '消耗积分': points_to_spend,
                            '剩余积分': st.session_state.current_points
                        })
                        # 记录积分明细
                        st.session_state.points_detail.append({
                            '时间': now,
                            '来源': '兑换素拓0.1',
                            '积分变动': f'-{points_to_spend}',
                            '余额': st.session_state.current_points
                        })
                        st.success(f"兑换成功！剩余积分：{st.session_state.current_points}")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("积分不足，无法兑换")
        
        with col2:
            st.markdown("""
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #333;'>劳动时长0.5</h4>
                <p style='margin: 0 0 12px 0; font-size: 20px; font-weight: bold;'>200积分</p>
            </div>
            """, unsafe_allow_html=True)
            # 居中显示兑换按钮
            col2_align = st.columns([1, 2, 1])
            with col2_align[1]:
                if st.button("兑换", key="exchange_2", use_container_width=True):
                    if st.session_state.current_points >= 200:
                        # 扣除积分（只扣除当前积分，不影响周积分和月积分）
                        points_to_spend = 200
                        st.session_state.current_points -= points_to_spend
                        # 注意：不扣除周积分和月积分，这样积分排名只算增加和惩罚，不算兑换扣除的积分
                        
                        # 更新scores_data并保存（只更新用户信息，不更新积分）
                        if 'username' in st.session_state:
                            username = st.session_state.username
                            if username in st.session_state.scores_data:
                                # 保持原有的周积分和月积分不变
                                pass
                            else:
                                st.session_state.scores_data[username] = {
                                    'weekly_score': st.session_state.weekly_score,
                                    'monthly_score': st.session_state.monthly_score,
                                    'class': st.session_state.get('student_class', '未分配班级'),
                                    'name': st.session_state.user_name
                                }
                            save_scores_data(st.session_state.scores_data)
                        
                        # 记录兑换历史
                        import datetime
                        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        st.session_state.exchange_history.append({
                            '时间': now,
                            '商品': '劳动时长0.5',
                            '消耗积分': points_to_spend,
                            '剩余积分': st.session_state.current_points
                        })
                        # 记录积分明细
                        st.session_state.points_detail.append({
                            '时间': now,
                            '来源': '兑换劳动时长0.5',
                            '积分变动': f'-{points_to_spend}',
                            '余额': st.session_state.current_points
                        })
                        st.success(f"兑换成功！剩余积分：{st.session_state.current_points}")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("积分不足，无法兑换")
        
        # 当学期兑换记录
        st.markdown("### 📋 当学期兑换记录")
        if st.session_state.exchange_history:
            df_exchange = pd.DataFrame(st.session_state.exchange_history)
            st.dataframe(df_exchange, use_container_width=True, hide_index=True)
        else:
            st.markdown("暂无兑换记录")
    
    # 积分排行榜页面
    elif st.session_state.selected_page == "积分排行榜":
        # 积分排行榜
        st.subheader("🏅 积分排行榜")
        
        scores_data = st.session_state.scores_data
        
        if not scores_data:
            st.info("暂无积分数据")
        else:
            # 整理学生积分数据
            student_scores = []
            for username, score_info in scores_data.items():
                if 'weekly_score' in score_info and 'monthly_score' in score_info:
                    student_scores.append({
                        '用户名': username,
                        '姓名': score_info.get('name', username),
                        '班级': score_info.get('class', '未分配班级'),
                        '周积分': score_info['weekly_score'],
                        '月积分': score_info['monthly_score']
                    })
            
            if not student_scores:
                st.info("暂无学生积分数据")
            else:
                df_scores = pd.DataFrame(student_scores)
                medals = ['🥇', '🥈', '🥉']
                
                # 选择查看类型
                view_type = st.radio(
                    "查看方式",
                    ["查看全部排名", "选择排名区间", "一键定位我的排名"],
                    horizontal=True
                )
                
                # 本周和本月排行
                ranking_col1, ranking_col2 = st.columns(2)
                
                with ranking_col1:
                    st.markdown("#### 📊 本周排行")
                    df_weekly_sorted = df_scores.sort_values('周积分', ascending=False).reset_index(drop=True)
                    df_weekly_sorted.index = df_weekly_sorted.index + 1
                    df_weekly_sorted = df_weekly_sorted.reset_index().rename(columns={'index': '排名'})
                    df_weekly_sorted['排名'] = df_weekly_sorted.apply(
                        lambda x: medals[x['排名']-1] if x['排名'] <= 3 else str(x['排名']),
                        axis=1
                    )
                    
                    # 根据查看方式过滤数据
                    if view_type == "查看全部排名":
                        df_weekly_display = df_weekly_sorted
                    elif view_type == "选择排名区间":
                        weekly_count = len(df_weekly_sorted)
                        if weekly_count > 0:
                            weekly_start = st.slider(
                                "本周排名起始位置",
                                min_value=1,
                                max_value=weekly_count,
                                value=1,
                                key="weekly_start"
                            )
                            weekly_end = st.slider(
                                "本周排名结束位置",
                                min_value=weekly_start,
                                max_value=weekly_count,
                                value=min(weekly_start + 9, weekly_count),
                                key="weekly_end"
                            )
                            df_weekly_display = df_weekly_sorted.iloc[weekly_start-1:weekly_end]
                        else:
                            df_weekly_display = df_weekly_sorted
                    elif view_type == "一键定位我的排名":
                        # 查找当前用户的排名
                        my_weekly_rank = df_weekly_sorted[df_weekly_sorted['用户名'] == st.session_state.username]
                        if not my_weekly_rank.empty:
                            my_rank_num = int(my_weekly_rank['排名'].iloc[0]) if my_weekly_rank['排名'].iloc[0].isdigit() else (1 if my_weekly_rank['排名'].iloc[0] == '🥇' else 2 if my_weekly_rank['排名'].iloc[0] == '🥈' else 3)
                            # 显示用户附近的排名（用户前后各4名）
                            weekly_count = len(df_weekly_sorted)
                            start_idx = max(0, my_rank_num - 5)
                            end_idx = min(weekly_count, my_rank_num + 4)
                            df_weekly_display = df_weekly_sorted.iloc[start_idx:end_idx].copy()
                            # 高亮显示用户的排名
                            df_weekly_display['姓名'] = df_weekly_display.apply(
                                lambda x: f"⭐ {x['姓名']}" if x['用户名'] == st.session_state.username else x['姓名'],
                                axis=1
                            )
                            st.success(f"你本周排名第 {my_rank_num} 名！")
                        else:
                            df_weekly_display = df_weekly_sorted
                    
                    df_weekly_display = df_weekly_display[['排名', '姓名', '周积分', '班级']]
                    st.dataframe(df_weekly_display, use_container_width=True, hide_index=True)
                
                with ranking_col2:
                    st.markdown("#### 📊 本月排行")
                    df_monthly_sorted = df_scores.sort_values('月积分', ascending=False).reset_index(drop=True)
                    df_monthly_sorted.index = df_monthly_sorted.index + 1
                    df_monthly_sorted = df_monthly_sorted.reset_index().rename(columns={'index': '排名'})
                    df_monthly_sorted['排名'] = df_monthly_sorted.apply(
                        lambda x: medals[x['排名']-1] if x['排名'] <= 3 else str(x['排名']),
                        axis=1
                    )
                    
                    # 根据查看方式过滤数据
                    if view_type == "查看全部排名":
                        df_monthly_display = df_monthly_sorted
                    elif view_type == "选择排名区间":
                        monthly_count = len(df_monthly_sorted)
                        if monthly_count > 0:
                            monthly_start = st.slider(
                                "本月排名起始位置",
                                min_value=1,
                                max_value=monthly_count,
                                value=1,
                                key="monthly_start"
                            )
                            monthly_end = st.slider(
                                "本月排名结束位置",
                                min_value=monthly_start,
                                max_value=monthly_count,
                                value=min(monthly_start + 9, monthly_count),
                                key="monthly_end"
                            )
                            df_monthly_display = df_monthly_sorted.iloc[monthly_start-1:monthly_end]
                        else:
                            df_monthly_display = df_monthly_sorted
                    elif view_type == "一键定位我的排名":
                        # 查找当前用户的排名
                        my_monthly_rank = df_monthly_sorted[df_monthly_sorted['用户名'] == st.session_state.username]
                        if not my_monthly_rank.empty:
                            my_rank_num = int(my_monthly_rank['排名'].iloc[0]) if my_monthly_rank['排名'].iloc[0].isdigit() else (1 if my_monthly_rank['排名'].iloc[0] == '🥇' else 2 if my_monthly_rank['排名'].iloc[0] == '🥈' else 3)
                            # 显示用户附近的排名（用户前后各4名）
                            monthly_count = len(df_monthly_sorted)
                            start_idx = max(0, my_rank_num - 5)
                            end_idx = min(monthly_count, my_rank_num + 4)
                            df_monthly_display = df_monthly_sorted.iloc[start_idx:end_idx].copy()
                            # 高亮显示用户的排名
                            df_monthly_display['姓名'] = df_monthly_display.apply(
                                lambda x: f"⭐ {x['姓名']}" if x['用户名'] == st.session_state.username else x['姓名'],
                                axis=1
                            )
                            st.success(f"你本月排名第 {my_rank_num} 名！")
                        else:
                            df_monthly_display = df_monthly_sorted
                    
                    df_monthly_display = df_monthly_display[['排名', '姓名', '月积分', '班级']]
                    st.dataframe(df_monthly_display, use_container_width=True, hide_index=True)
    
    # 异常打卡申诉页面
    elif st.session_state.selected_page == "异常打卡申诉":
        # 异常打卡申诉
        st.subheader("⚠️ 异常打卡申诉")
        
        # 申诉表单
        with st.form("appeal_form"):
            st.markdown("### 申诉信息")
            appeal_date = st.date_input("异常打卡日期")
            appeal_reason = st.text_area("申诉原因", placeholder="请详细描述异常打卡的情况...")
            appeal_evidence = st.file_uploader("上传证明材料（可选）", type=["jpg", "jpeg", "png", "pdf"])
            
            submitted = st.form_submit_button("提交申诉", type="primary")
            
            if submitted:
                # 记录申诉
                import datetime
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # 初始化申诉记录
                if 'appeals' not in st.session_state:
                    st.session_state.appeals = []
                
                # 添加申诉记录
                st.session_state.appeals.append({
                    '时间': now,
                    '日期': appeal_date.strftime("%Y-%m-%d"),
                    '学生': st.session_state.user_name,
                    '宿舍': st.session_state.dormitory,
                    '原因': appeal_reason,
                    '状态': '待审核'
                })
                
                st.success("申诉提交成功！请等待老师审核。")
        
        # 显示历史申诉记录
        st.markdown("### 📋 历史申诉记录")
        if 'appeals' in st.session_state and st.session_state.appeals:
            df_appeals = pd.DataFrame(st.session_state.appeals)
            st.dataframe(df_appeals, use_container_width=True, hide_index=True)
        else:
            st.markdown("暂无申诉记录")

# 管理者页面
def admin_page():
    st.title("📊 校园能耗监测与智能节能系统")
    st.markdown("#### AI 赋能校园水电能耗智能监测与可视化，终端精准管控，高效识别异常与浪费，全面提升能耗管理效率。")
    
    # 初始化会话状态
    if 'admin_selected_page' not in st.session_state:
        st.session_state.admin_selected_page = "首页概览"
    
    with st.sidebar:
        # 管理终端标题
        st.title("🛠️ 管理终端")
        st.markdown("### 欢迎回来，管理员！")
        
        # 搜索框（带内置放大镜）
        with st.form(key='admin_search_form'):
            search_query = st.text_input("搜索功能", placeholder="搜索功能", key="admin_search")
            search_submitted = st.form_submit_button("搜索")
        
        # 搜索功能实现
        if search_submitted and search_query:
            # 定义功能映射
            search_mapping = {
                "首页": "首页概览",
                "首页概览": "首页概览",
                "能耗": "能耗监测",
                "能耗监测": "能耗监测",
                "预警": "能耗预警",
                "能耗预警": "能耗预警",
                "智能": "智能调控",
                "智能调控": "智能调控",
                "数据": "数据接口",
                "数据接口": "数据接口",
                "清除": "数据清除",
                "数据清除": "数据清除"
            }
            
            # 搜索匹配
            for key, value in search_mapping.items():
                if search_query.lower() in key.lower():
                    st.session_state.admin_selected_page = value
                    st.rerun()
        
        # 初始化折叠状态
        if 'management_expanded' not in st.session_state:
            st.session_state.management_expanded = True
        if 'system_expanded' not in st.session_state:
            st.session_state.system_expanded = True
        
        # 检查是否所有科目都已展开
        all_expanded = st.session_state.management_expanded and st.session_state.system_expanded
        
        # 一键折叠/展开按钮
        if st.button("一键折叠" if all_expanded else "一键展开"):
            new_state = not all_expanded
            st.session_state.management_expanded = new_state
            st.session_state.system_expanded = new_state
            st.rerun()
        
        # 首页按钮
        if st.button("🏠 首页概览", use_container_width=True):
            st.session_state.admin_selected_page = "首页概览"
            st.rerun()
        
        # 功能分类 - 管理功能
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            <div style='margin-top: 20px;'>
                <h4 style='margin: 0 0 10px 0; display: flex; align-items: center;'>
                    <span style='color: #1890ff; margin-right: 8px;'>📋</span>
                    管理功能
                </h4>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("▼" if st.session_state.management_expanded else "▶", key="management_toggle", use_container_width=True):
                st.session_state.management_expanded = not st.session_state.management_expanded
                st.rerun()
        
        # 管理功能
        if st.session_state.management_expanded:
            if st.button("能耗监测", use_container_width=True):
                st.session_state.admin_selected_page = "能耗监测"
                st.rerun()
            if st.button("能耗预警", use_container_width=True):
                st.session_state.admin_selected_page = "能耗预警"
                st.rerun()
            if st.button("智能调控", use_container_width=True):
                st.session_state.admin_selected_page = "智能调控"
                st.rerun()
        
        # 功能分类 - 系统设置
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            <div style='margin-top: 20px;'>
                <h4 style='margin: 0 0 10px 0; display: flex; align-items: center;'>
                    <span style='color: #1890ff; margin-right: 8px;'>⚙️</span>
                    系统设置
                </h4>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("▼" if st.session_state.system_expanded else "▶", key="system_toggle", use_container_width=True):
                st.session_state.system_expanded = not st.session_state.system_expanded
                st.rerun()
        
        # 系统设置功能
        if st.session_state.system_expanded:
            if st.button("数据接口", use_container_width=True):
                st.session_state.admin_selected_page = "数据接口"
                st.rerun()
            if st.button("数据清除", use_container_width=True):
                st.session_state.admin_selected_page = "数据清除"
                st.rerun()
        
        st.markdown("---")
        st.subheader("系统状态")
        status_col1, status_col2 = st.columns(2)
        with status_col1:
            st.markdown("""
            <div style='background-color: #f8f9fa; padding: 12px; border-radius: 8px; text-align: center;'>
                <p style='margin: 0 0 4px 0; font-weight: bold;'>系统状态</p>
                <p style='margin: 0;'>运行中 🟢</p>
            </div>
            """, unsafe_allow_html=True)
        with status_col2:
            st.markdown("""
            <div style='background-color: #f8f9fa; padding: 12px; border-radius: 8px; text-align: center;'>
                <p style='margin: 0 0 4px 0; font-weight: bold;'>数据更新</p>
                <p style='margin: 0;'>实时 🔄</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 登出按钮
        if st.button("登出", type="secondary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_position = None
            st.session_state.username = None
            st.session_state.user_name = None
            st.rerun()
    
    if st.session_state.admin_selected_page == "首页概览":
        # 水、电综合监测指标
        st.subheader("🌊💡 水电综合监测")
        col_water, col_electricity = st.columns(2, gap="medium")
        
        # 注意：以下数据为模拟数据
        # 实际应用中，应从Excel文件或API接口读取数据并进行按月统计
        # 例如：
        # 1. 从Excel读取数据：
        # df = pd.read_excel('energy_data.xlsx')
        # df['日期'] = pd.to_datetime(df['日期'])
        # df['月份'] = df['日期'].dt.to_period('M')
        # monthly_water = df.groupby('月份')['水耗'].sum().iloc[-1]
        # monthly_electricity = df.groupby('月份')['电耗'].sum().iloc[-1]
        # 
        # 2. 从API接口获取数据：
        # import requests
        # response = requests.get('http://api.example.com/energy/monthly')
        # data = response.json()
        # monthly_water = data['water_consumption']
        # monthly_electricity = data['electricity_consumption']
        
        with col_water:
            st.markdown("""
            <div style='background-color: #e6f7ff; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 16px 0; color: #1890ff; font-size: 18px; text-align: center;'>月总水耗</h4>
                <p style='margin: 0 0 8px 0; font-size: 28px; font-weight: bold;'>125.6</p>
                <p style='margin: 0 0 16px 0; font-size: 14px; color: #666;'>吨</p>
                <div style='background-color: #4CAF50; color: white; font-size: 16px; font-weight: bold; padding: 6px 12px; border-radius: 6px; display: inline-block;'>↓ 2.8%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_electricity:
            st.markdown("""
            <div style='background-color: #fff7e6; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 16px 0; color: #fa8c16; font-size: 18px; text-align: center;'>月总电耗</h4>
                <p style='margin: 0 0 8px 0; font-size: 28px; font-weight: bold;'>12,580</p>
                <p style='margin: 0 0 16px 0; font-size: 14px; color: #666;'>kWh</p>
                <div style='background-color: #4CAF50; color: white; font-size: 16px; font-weight: bold; padding: 6px 12px; border-radius: 6px; display: inline-block;'>↓ 3.2%</div>
            </div>
            """, unsafe_allow_html=True)
        
        # 校园水、电总能耗分布图
        st.subheader("📊 校园水、电总能耗分布图")
        col_water_dist, col_electricity_dist = st.columns(2, gap="medium")
        
        # 水耗分布饼图
        with col_water_dist:
            # 模拟数据，实际应从Excel或API获取
            water_dist_data = {
                '区域': ['教学楼', '图书馆', '宿舍楼', '行政楼', '其他'],
                '水耗': [45, 20, 30, 15, 10]
            }
            df_water_dist = pd.DataFrame(water_dist_data)
            
            fig_water_dist = go.Figure()
            fig_water_dist.add_trace(go.Pie(
                labels=df_water_dist['区域'],
                values=df_water_dist['水耗'],
                hole=0.3,
                marker_colors=['#1890ff', '#13c2c2', '#52c41a', '#faad14', '#f5222d']
            ))
            fig_water_dist.update_layout(
                title="水耗分布",
                height=450,
                legend_title="区域",
                font=dict(
                    size=16  # 整体字体大小
                ),
                title_font=dict(
                    size=20  # 标题字体大小
                ),
                legend=dict(
                    font=dict(
                        size=16  # 图例字体大小
                    )
                )
            )
            st.plotly_chart(fig_water_dist, use_container_width=True)
        
        # 电耗分布饼图
        with col_electricity_dist:
            # 模拟数据，实际应从Excel或API获取
            electricity_dist_data = {
                '区域': ['教学楼', '图书馆', '宿舍楼', '行政楼', '其他'],
                '电耗': [50, 25, 35, 20, 15]
            }
            df_electricity_dist = pd.DataFrame(electricity_dist_data)
            
            fig_electricity_dist = go.Figure()
            fig_electricity_dist.add_trace(go.Pie(
                labels=df_electricity_dist['区域'],
                values=df_electricity_dist['电耗'],
                hole=0.3,
                marker_colors=['#fa8c16', '#faad14', '#52c41a', '#13c2c2', '#1890ff']
            ))
            fig_electricity_dist.update_layout(
                title="电耗分布",
                height=450,
                legend_title="区域",
                font=dict(
                    size=16  # 整体字体大小
                ),
                title_font=dict(
                    size=20  # 标题字体大小
                ),
                legend=dict(
                    font=dict(
                        size=16  # 图例字体大小
                    )
                )
            )
            st.plotly_chart(fig_electricity_dist, use_container_width=True)
        
        # 数据获取说明
        st.markdown("""
        <div style='background-color: #f0f8ff; padding: 16px; border-radius: 8px; margin-top: 16px;'>
            <h5 style='margin: 0 0 8px 0; color: #1890ff;'>数据说明</h5>
            <p style='margin: 0; font-size: 14px; color: #666;'>
                上述饼图数据为模拟数据。实际应用中，可通过以下方式获取数据：
            </p>
            <ul style='margin: 8px 0 0 0; font-size: 14px; color: #666;'>
                <li>从Excel文件读取：使用pandas读取Excel文件，按区域分组统计水耗和电耗</li>
                <li>从API接口获取：调用后端API接口，获取按区域统计的能耗数据</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 原有指标卡片
        col1, col2, col3 = st.columns(3, gap="medium")
        
        with col1:
            st.markdown("""
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #333; font-size: 16px;'>今日总能耗</h4>
                <p style='margin: 0 0 12px 0; font-size: 28px; font-weight: bold;'>12,580</p>
                <div style='background-color: #4CAF50; color: white; font-size: 16px; font-weight: bold; padding: 6px 12px; border-radius: 6px; display: inline-block;'>↓ 3.2%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #333; font-size: 16px;'>本月累计能耗</h4>
                <p style='margin: 0 0 12px 0; font-size: 28px; font-weight: bold;'>358,420</p>
                <div style='background-color: #4CAF50; color: white; font-size: 16px; font-weight: bold; padding: 6px 12px; border-radius: 6px; display: inline-block;'>↓ 5.8%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #333; font-size: 16px;'>节能建议数</h4>
                <p style='margin: 0 0 12px 0; font-size: 28px; font-weight: bold;'>24</p>
                <div style='background-color: #4CAF50; color: white; font-size: 16px; font-weight: bold; padding: 6px 12px; border-radius: 6px; display: inline-block;'>↑ 8</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 能耗趋势分析
        st.subheader("📈 能耗趋势分析")
        
        # 添加日期范围筛选
        date_range = st.date_input(
            "选择日期范围",
            value=(pd.to_datetime('2024-01-01'), pd.to_datetime('2024-01-07')),
            min_value=pd.to_datetime('2024-01-01'),
            max_value=pd.to_datetime('2024-12-31'),
            key="energy_date_range"
        )
        
        # 生成所选日期范围内的能耗趋势数据
        start_date, end_date = date_range
        date_range_days = (end_date - start_date).days + 1
        
        # 生成日期列表
        dates = []
        for i in range(date_range_days):
            date = start_date + pd.Timedelta(days=i)
            dates.append(date.strftime('%m月%d日'))
        
        # 生成能耗值数据（模拟数据，实际应从数据库或API获取）
        energy_values = []
        base_value = 1250
        for i in range(date_range_days):
            # 能耗值逐渐减少
            value = max(800, base_value - i * 50)
            energy_values.append(value)
        
        energy_trend = {
            '日期': dates,
            '能耗值': energy_values
        }
        df_energy = pd.DataFrame(energy_trend)
        
        fig_energy = go.Figure()
        fig_energy.add_trace(go.Scatter(x=df_energy['日期'], y=df_energy['能耗值'], mode='lines+markers', name='能耗值'))
        fig_energy.update_layout(
            title=f"{start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')} 能耗趋势",
            xaxis_title="日期",
            yaxis_title="能耗值 (kWh)",
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig_energy, use_container_width=True)
        
        # AI分析结果展示
        st.subheader("🤖 AI实时分析")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='background-color: #f0f8ff; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #1890ff;'>异常检测</h4>
                <p><strong>检测到异常：</strong>教学楼A区空调能耗异常偏高</p>
                <p><strong>异常程度：</strong>严重</p>
                <p><strong>可能原因：</strong>空调温度设置过低，运行时间过长</p>
                <p><strong>建议措施：</strong>调整空调温度至26℃，设置自动关机时间</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background-color: #e8f5e8; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #2e7d32;'>节能建议</h4>
                <p><strong>1. 照明系统优化：</strong>更换LED灯具，预计节能30%</p>
                <p><strong>2. 空调系统调整：</strong>统一设置温度26℃，预计节能25%</p>
                <p><strong>3. 用水管理：</strong>安装节水龙头，预计节水15%</p>
                <p><strong>4. 设备管理：</strong>定期维护设备，减少能耗损失</p>
            </div>
            """, unsafe_allow_html=True)
    
    elif st.session_state.admin_selected_page == "能耗监测":
        st.header("📊 能耗监测中心")
        
        # 左右两列布局：水耗监测（左）和电耗监测（右）
        col_water, col_power = st.columns(2)
        
        # 模拟区域能耗数据
        area_energy_data = {
            "宿舍": {"水耗": 45.2, "电耗": 4200, "节能率": 15},
            "教学楼": {"水耗": 35.8, "电耗": 3950, "节能率": 12},
            "行政楼": {"水耗": 12.5, "电耗": 1080, "节能率": 8},
            "食堂": {"水耗": 25.6, "电耗": 3100, "节能率": 10},
            "快递站": {"水耗": 3.2, "电耗": 450, "节能率": 5},
            "保安室": {"水耗": 2.1, "电耗": 320, "节能率": 3},
            "小卖部": {"水耗": 1.2, "电耗": 280, "节能率": 2}
        }
        
        areas = ["宿舍", "教学楼", "行政楼", "食堂", "快递站", "保安室", "小卖部"]
        
        # 左侧：水耗监测
        with col_water:
            st.subheader("💧 水耗监测")
            
            # 时间筛选
            water_time_filter = st.selectbox("时间范围", ["今日", "本周", "本月", "自定义"], key="water_time")
            
            if water_time_filter == "自定义":
                water_date_range = st.date_input("选择日期范围", value=(pd.to_datetime('2024-01-01'), pd.to_datetime('2024-01-31')), min_value=pd.to_datetime('2024-01-01'), max_value=pd.to_datetime('2024-12-31'), key="water_date")
            
            # 区域选择（多选）
            water_selected_areas = st.multiselect("选择区域", areas, default=areas, key="water_areas")
            
            st.markdown("---")
            
            # 区域能耗详情
            st.markdown("#### 🏢 区域能耗详情")
            
            # 筛选数据
            water_filtered_data = []
            for area in water_selected_areas:
                if area in area_energy_data:
                    water_filtered_data.append({
                        "区域": area,
                        "水耗 (吨)": area_energy_data[area]["水耗"],
                        "节能率 (%)": area_energy_data[area]["节能率"]
                    })
            
            # 显示数据表格
            if water_filtered_data:
                df_water = pd.DataFrame(water_filtered_data)
                st.dataframe(df_water, use_container_width=True, hide_index=True)
            else:
                st.markdown("请选择至少一个区域")
            
            st.markdown("---")
            
            # 能耗趋势图
            st.markdown("#### 📊 能耗趋势分析")
            
            # 生成模拟数据
            water_dates = pd.date_range('2024-01-01', '2024-01-15').strftime('%m月%d日')
            water_energy_data = [45.2, 43.8, 42.5, 41.2, 40.0, 38.8, 37.5, 36.2, 35.0, 33.8, 32.5, 31.2, 30.0, 28.8, 27.5]
            
            # 趋势折线图
            st.markdown("##### 趋势折线图")
            fig_water_line = go.Figure()
            fig_water_line.add_trace(go.Scatter(x=water_dates, y=water_energy_data, mode='lines+markers', name='水耗 (吨)', line=dict(color="#1890ff")))
            fig_water_line.update_layout(
                xaxis_title='日期',
                yaxis_title='水耗 (吨)',
                height=300,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_water_line, use_container_width=True)
            
            # 柱状图
            st.markdown("##### 柱状图")
            fig_water_bar = go.Figure()
            fig_water_bar.add_trace(go.Bar(x=water_dates, y=water_energy_data, name='水耗 (吨)', marker=dict(color="#1890ff")))
            fig_water_bar.update_layout(
                xaxis_title='日期',
                yaxis_title='水耗 (吨)',
                height=300,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_water_bar, use_container_width=True)
            
            st.markdown("---")
            
            # 绘制饼图（区域分布）
            st.markdown("#### 🏢 区域能耗分布")
            
            # 模拟区域能耗数据
            water_area_data = {
                "宿舍": 45.2,
                "教学楼": 35.8,
                "行政楼": 12.5,
                "食堂": 25.6,
                "快递站": 3.2,
                "保安室": 2.1,
                "小卖部": 1.2
            }
            
            # 筛选区域数据
            water_filtered_area_data = {area: value for area, value in water_area_data.items() if area in water_selected_areas}
            
            if water_filtered_area_data:
                fig_water_pie = go.Figure()
                fig_water_pie.add_trace(go.Pie(
                    labels=list(water_filtered_area_data.keys()),
                    values=list(water_filtered_area_data.values()),
                    hoverinfo='label+percent',
                    textinfo='value',
                    textfont=dict(size=14),
                    marker=dict(colors=px.colors.qualitative.Plotly)
                ))
                fig_water_pie.update_layout(
                    title='水耗区域分布',
                    height=350,
                    margin=dict(l=20, r=20, t=60, b=20)
                )
                st.plotly_chart(fig_water_pie, use_container_width=True)
            else:
                st.markdown("请选择至少一个区域")
        
        # 右侧：电耗监测
        with col_power:
            st.subheader("⚡ 电耗监测")
            
            # 时间筛选
            power_time_filter = st.selectbox("时间范围", ["今日", "本周", "本月", "自定义"], key="power_time")
            
            if power_time_filter == "自定义":
                power_date_range = st.date_input("选择日期范围", value=(pd.to_datetime('2024-01-01'), pd.to_datetime('2024-01-31')), min_value=pd.to_datetime('2024-01-01'), max_value=pd.to_datetime('2024-12-31'), key="power_date")
            
            # 区域选择（多选）
            power_selected_areas = st.multiselect("选择区域", areas, default=areas, key="power_areas")
            
            st.markdown("---")
            
            # 区域能耗详情
            st.markdown("#### 🏢 区域能耗详情")
            
            # 筛选数据
            power_filtered_data = []
            for area in power_selected_areas:
                if area in area_energy_data:
                    power_filtered_data.append({
                        "区域": area,
                        "电耗 (kWh)": area_energy_data[area]["电耗"],
                        "节能率 (%)": area_energy_data[area]["节能率"]
                    })
            
            # 显示数据表格
            if power_filtered_data:
                df_power = pd.DataFrame(power_filtered_data)
                st.dataframe(df_power, use_container_width=True, hide_index=True)
            else:
                st.markdown("请选择至少一个区域")
            
            st.markdown("---")
            
            # 能耗趋势图
            st.markdown("#### 📊 能耗趋势分析")
            
            # 生成模拟数据
            power_dates = pd.date_range('2024-01-01', '2024-01-15').strftime('%m月%d日')
            power_energy_data = [4200, 4150, 4100, 4050, 4000, 3950, 3900, 3850, 3800, 3750, 3700, 3650, 3600, 3550, 3500]
            
            # 趋势折线图
            st.markdown("##### 趋势折线图")
            fig_power_line = go.Figure()
            fig_power_line.add_trace(go.Scatter(x=power_dates, y=power_energy_data, mode='lines+markers', name='电耗 (kWh)', line=dict(color="#fa8c16")))
            fig_power_line.update_layout(
                xaxis_title='日期',
                yaxis_title='电耗 (kWh)',
                height=300,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_power_line, use_container_width=True)
            
            # 柱状图
            st.markdown("##### 柱状图")
            fig_power_bar = go.Figure()
            fig_power_bar.add_trace(go.Bar(x=power_dates, y=power_energy_data, name='电耗 (kWh)', marker=dict(color="#fa8c16")))
            fig_power_bar.update_layout(
                xaxis_title='日期',
                yaxis_title='电耗 (kWh)',
                height=300,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_power_bar, use_container_width=True)
            
            st.markdown("---")
            
            # 绘制饼图（区域分布）
            st.markdown("#### 🏢 区域能耗分布")
            
            # 模拟区域能耗数据
            power_area_data = {
                "宿舍": 4200,
                "教学楼": 3950,
                "行政楼": 1080,
                "食堂": 3100,
                "快递站": 450,
                "保安室": 320,
                "小卖部": 280
            }
            
            # 筛选区域数据
            power_filtered_area_data = {area: value for area, value in power_area_data.items() if area in power_selected_areas}
            
            if power_filtered_area_data:
                fig_power_pie = go.Figure()
                fig_power_pie.add_trace(go.Pie(
                    labels=list(power_filtered_area_data.keys()),
                    values=list(power_filtered_area_data.values()),
                    hoverinfo='label+percent',
                    textinfo='value',
                    textfont=dict(size=14),
                    marker=dict(colors=px.colors.qualitative.Plotly)
                ))
                fig_power_pie.update_layout(
                    title='电耗区域分布',
                    height=350,
                    margin=dict(l=20, r=20, t=60, b=20)
                )
                st.plotly_chart(fig_power_pie, use_container_width=True)
            else:
                st.markdown("请选择至少一个区域")
    
    elif st.session_state.admin_selected_page == "能耗预警":
        st.header("⚠️ 能耗预警中心")
        
        st.markdown("""
        实时监测各楼栋电耗情况，及时发现异常高能耗并预警，保障校园能源安全！
        """)
        
        st.markdown("---")
        
        # 预警概览
        st.subheader("📊 预警概览")
        
        col1, col2, col3, col4 = st.columns(4, gap="medium")
        
        with col1:
            st.metric("预警楼栋数", "3", "↑ 1")
        
        with col2:
            st.metric("今日高能耗事件", "8", "↑ 3")
        
        with col3:
            st.metric("平均超阈值", "28%", "↑ 5%")
        
        with col4:
            st.metric("待处理预警", "2", "⚠️")
        

        
        # 预警详情操作
        st.subheader("⚡ 预警处理")
        
        # 初始化预警数据到session_state
        if 'warning_data' not in st.session_state:
            st.session_state.warning_data = [
                {
                    "楼栋": "1号宿舍楼",
                    "当前电耗 (kWh)": 5280,
                    "阈值 (kWh)": 4200,
                    "超出比例": "25.7%",
                    "预警级别": "一级预警",
                    "状态": "待处理",
                    "监测时间": "2026-04-11 14:30:00"
                },
                {
                    "楼栋": "3号教学楼",
                    "当前电耗 (kWh)": 4620,
                    "阈值 (kWh)": 3950,
                    "超出比例": "17.0%",
                    "预警级别": "二级预警",
                    "状态": "处理中",
                    "监测时间": "2026-04-11 14:25:00"
                },
                {
                    "楼栋": "2号食堂",
                    "当前电耗 (kWh)": 4030,
                    "阈值 (kWh)": 3100,
                    "超出比例": "30.0%",
                    "预警级别": "一级预警",
                    "状态": "待处理",
                    "监测时间": "2026-04-11 14:20:00"
                },
                {
                    "楼栋": "行政楼",
                    "当前电耗 (kWh)": 1188,
                    "阈值 (kWh)": 1080,
                    "超出比例": "10.0%",
                    "预警级别": "三级预警",
                    "状态": "已处理",
                    "监测时间": "2026-04-11 13:45:00"
                },
                {
                    "楼栋": "5号宿舍楼",
                    "当前电耗 (kWh)": 3850,
                    "阈值 (kWh)": 3500,
                    "超出比例": "10.0%",
                    "预警级别": "三级预警",
                    "状态": "已处理",
                    "监测时间": "2026-04-11 12:30:00"
                }
            ]
        
        # 从session_state获取预警数据
        df_warning = pd.DataFrame(st.session_state.warning_data)
        
        if not df_warning.empty:
            col_action1, col_action2 = st.columns(2)
            
            with col_action1:
                selected_building = st.selectbox("选择楼栋", df_warning["楼栋"].tolist())
            
            with col_action2:
                action_type = st.selectbox("操作类型", ["查看详情", "标记处理中", "标记已处理", "发送通知"])
            
            if st.button("执行操作", type="primary"):
                if action_type == "查看详情":
                    st.info(f"正在查看 {selected_building} 的详细预警信息...")
                elif action_type == "标记处理中":
                    # 更新session_state中的预警数据
                    for item in st.session_state.warning_data:
                        if item["楼栋"] == selected_building:
                            item["状态"] = "处理中"
                    st.success(f"{selected_building} 已标记为处理中！")
                    st.rerun()
                elif action_type == "标记已处理":
                    # 更新session_state中的预警数据
                    for item in st.session_state.warning_data:
                        if item["楼栋"] == selected_building:
                            item["状态"] = "已处理"
                    st.success(f"{selected_building} 已标记为已处理！")
                    st.rerun()
                elif action_type == "发送通知":
                    st.success(f"已向 {selected_building} 发送预警通知！")
                    st.balloons()
        
        # 电耗监测过高值数据表
        st.subheader("🏢 电耗监测过高值数据表")
        
        # 筛选功能
        col_filter1, col_filter2 = st.columns(2)
        
        with col_filter1:
            warning_level = st.selectbox("预警级别", ["全部", "一级预警", "二级预警", "三级预警"])
        
        with col_filter2:
            building_status = st.selectbox("处理状态", ["全部", "待处理", "处理中", "已处理"])
        
        # 根据筛选条件过滤数据
        if warning_level != "全部":
            df_warning = df_warning[df_warning["预警级别"] == warning_level]
        
        if building_status != "全部":
            df_warning = df_warning[df_warning["状态"] == building_status]
        
        # 显示数据表格（带样式）
        def highlight_warning(val):
            if val == "一级预警":
                return 'background-color: #ff4d4f; color: white'
            elif val == "二级预警":
                return 'background-color: #fa8c16; color: white'
            elif val == "三级预警":
                return 'background-color: #fadb14; color: black'
            elif val == "待处理":
                return 'background-color: #ff4d4f; color: white'
            elif val == "处理中":
                return 'background-color: #fa8c16; color: white'
            elif val == "已处理":
                return 'background-color: #52c41a; color: white'
            else:
                return ''
        
        # 应用样式
        styled_df = df_warning.style.applymap(highlight_warning, subset=["预警级别", "状态"])
        
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # 预警趋势分析
        st.subheader("📈 预警趋势分析")
        
        # 模拟预警趋势数据
        warning_dates = pd.date_range('2026-04-01', '2026-04-11').strftime('%m月%d日')
        warning_count_data = {
            "一级预警": [2, 1, 3, 2, 1, 0, 2, 3, 1, 2, 3],
            "二级预警": [3, 4, 2, 3, 4, 2, 3, 2, 4, 3, 2],
            "三级预警": [5, 3, 4, 3, 2, 5, 4, 3, 5, 4, 3]
        }
        
        df_trend = pd.DataFrame(warning_count_data, index=warning_dates)
        
        # 绘制趋势图
        fig_trend = go.Figure()
        
        fig_trend.add_trace(go.Scatter(
            x=df_trend.index,
            y=df_trend["一级预警"],
            mode='lines+markers',
            name='一级预警',
            line=dict(color="#ff4d4f", width=3),
            marker=dict(size=8)
        ))
        
        fig_trend.add_trace(go.Scatter(
            x=df_trend.index,
            y=df_trend["二级预警"],
            mode='lines+markers',
            name='二级预警',
            line=dict(color="#fa8c16", width=3),
            marker=dict(size=8)
        ))
        
        fig_trend.add_trace(go.Scatter(
            x=df_trend.index,
            y=df_trend["三级预警"],
            mode='lines+markers',
            name='三级预警',
            line=dict(color="#fadb14", width=3),
            marker=dict(size=8)
        ))
        
        fig_trend.update_layout(
            title='近10天预警趋势',
            xaxis_title='日期',
            yaxis_title='预警次数',
            height=400,
            margin=dict(l=20, r=20, t=60, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
        
        st.markdown("---")
        
        # 楼栋预警分布图
        st.subheader("🏗️ 各楼栋预警分布")
        
        building_warning_data = {
            "楼栋": ["1号宿舍楼", "2号宿舍楼", "3号宿舍楼", "1号教学楼", "2号教学楼", "3号教学楼", "行政楼", "1号食堂", "2号食堂"],
            "预警次数": [12, 8, 6, 9, 5, 7, 4, 10, 11]
        }
        
        df_building_warning = pd.DataFrame(building_warning_data)
        
        fig_building = go.Figure()
        fig_building.add_trace(go.Bar(
            x=df_building_warning["楼栋"],
            y=df_building_warning["预警次数"],
            marker=dict(color="#ff4d4f")
        ))
        
        fig_building.update_layout(
            title='各楼栋预警次数统计',
            xaxis_title='楼栋',
            yaxis_title='预警次数',
            height=400,
            margin=dict(l=20, r=20, t=60, b=80)
        )
        
        st.plotly_chart(fig_building, use_container_width=True)
    
    elif st.session_state.admin_selected_page == "智能调控":
        st.header("⚙️ 智能节能调控系统")
        
        st.markdown("""
        空调、照明、水泵全部智能联动，人走灯灭、按需供能，告别无效耗电！
        """)
        
        # 智能调控概览
        st.subheader("📊 调控概览")
        
        col1, col2, col3 = st.columns(3, gap="medium")
        
        with col1:
            st.metric("智能设备数", "128", "↑ 24")
        
        with col2:
            st.metric("今日节能", "856 kWh", "↑ 12.5%")
        
        with col3:
            st.metric("调控事件", "42", "实时")
    
    elif st.session_state.admin_selected_page == "数据接口":
        st.header("🔌 数据管理中心")
        
        st.markdown("""
        数据导入与导出功能，支持学生信息、教师信息和能耗数据的批量管理
        """)
        
        st.markdown("---")
        
        # 数据导入
        st.subheader("📥 数据导入")
        
        import_type = st.selectbox("选择导入类型", ["学生信息", "辅导员信息", "能耗数据"])
        
        # 账户生成选项
        if import_type in ["学生信息", "辅导员信息"]:
            generate_account = st.checkbox("自动生成对应账户", value=True, help="根据导入的信息自动生成登录账户")
            if generate_account:
                st.info(f"将根据导入的{'学生' if import_type == '学生信息' else '辅导员'}信息自动生成登录账户")
        
        uploaded_file = st.file_uploader("选择文件上传", type=["csv", "xlsx", "xls"])
        if uploaded_file is not None:
            # 记录上传的文件
            if 'uploaded_files' not in st.session_state:
                st.session_state.uploaded_files = []
            
            import datetime
            file_info = {
                'name': uploaded_file.name,
                'type': uploaded_file.type,
                'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # 检查文件是否已经记录
            file_exists = False
            for existing_file in st.session_state.uploaded_files:
                if existing_file['name'] == file_info['name'] and existing_file['date'] == file_info['date']:
                    file_exists = True
                    break
            
            if not file_exists:
                st.session_state.uploaded_files.append(file_info)
            
            # 读取上传的文件
            if uploaded_file.name.endswith('.csv'):
                df_uploaded = pd.read_csv(uploaded_file)
                st.dataframe(df_uploaded, use_container_width=True)
            elif uploaded_file.name.endswith('.xlsx'):
                df_uploaded = pd.read_excel(uploaded_file)
                st.dataframe(df_uploaded, use_container_width=True)
                
            if st.button("导入数据", type="primary", key="import_data_button_1"):
                    # 先清除虚拟账户
                    new_users_data = {}
                    for username, user_info in st.session_state.users_data.items():
                        if not user_info.get(VIRTUAL_DATA_FLAG, False):
                            new_users_data[username] = user_info
                    st.session_state.users_data = new_users_data
                    
                    # 清除虚拟积分数据
                    new_scores_data = {}
                    for username, score_info in st.session_state.scores_data.items():
                        if not score_info.get(VIRTUAL_DATA_FLAG, False):
                            new_scores_data[username] = score_info
                    st.session_state.scores_data = new_scores_data
                    
                    # 保存清除虚拟数据后的状态
                    save_users_data(st.session_state.users_data)
                    save_scores_data(st.session_state.scores_data)
                    
                    if import_type in ["学生信息", "辅导员信息"] and generate_account:
                        generated_accounts = []
                        columns = df_uploaded.columns.tolist()
                        for _, row in df_uploaded.iterrows():
                            try:
                                # 根据学号或工号生成用户名
                                if import_type == "学生信息" and '学号' in columns:
                                    username = str(row['学号'])
                                elif import_type == "辅导员信息" and '工号' in columns:
                                    # 辅导员优先使用姓名作为用户名，其次使用工号
                                    # 支持"姓名"和"辅导员姓名"字段
                                    username = str(row.get('姓名', row.get('辅导员姓名', str(row['工号']))))
                                elif import_type == "辅导员信息" and '学号' in columns:
                                    # 如果是辅导员信息导入，但文件中包含学号字段，说明可能是学生信息文件
                                    st.warning(f"导入类型为{import_type}，但文件中包含'学号'字段，可能是学生信息文件。请选择正确的导入类型。")
                                    continue
                                else:
                                    # 优先使用姓名作为用户名，支持"姓名"和"辅导员姓名"字段
                                    username = str(row.get('姓名', row.get('辅导员姓名', 'user_' + str(random.randint(1000, 9999)))))
                                
                                # 生成密码
                                password = generate_password()
                                
                                # 创建用户数据
                                if import_type == "学生信息":
                                    # 构建班级名称（年级+专业+班级）
                                    grade = str(row.get('年级', ''))
                                    major = str(row.get('专业', ''))
                                    # 尝试获取班级相关列，支持多种列名
                                    class_name = ''
                                    class_columns = ['班级', '班', 'class', 'ClassName']
                                    for col in class_columns:
                                        if col in columns:
                                            class_name = str(row.get(col, ''))
                                            break
                                    
                                    # 获取联系电话
                                    phone = str(row.get('联系电话', row.get('电话', '')))
                                    
                                    # 获取宿舍（支持多种列名）
                                    dormitory = ''
                                    dormitory_columns = ['宿舍', '宿舍号', '寝室', '寝室号', 'dormitory', 'Dormitory']
                                    for col in dormitory_columns:
                                        if col in columns:
                                            dormitory = str(row.get(col, ''))
                                            break
                                    if not dormitory:
                                        dormitory = '1号楼101'
                                    
                                    # 获取性别、学院、辅导员
                                    gender = str(row.get('性别', ''))
                                    college = str(row.get('学院', ''))
                                    counselor = str(row.get('辅导员', ''))
                                    
                                    # 组合完整班级名称
                                    full_class_name = ''
                                    if grade and major and class_name:
                                        # 统一格式为"2023级金融学2班"
                                        # 提取年级数字（如"2023"）
                                        grade_num = ''.join(filter(str.isdigit, grade))
                                        if grade_num:
                                            # 提取班级数字（如"2班"）
                                            class_num = class_name
                                            # 移除班级名称中的年级和专业信息
                                            class_num = class_num.replace(grade, '').replace(major, '').strip()
                                            # 确保班级名称以"班"结尾
                                            if not class_num.endswith('班'):
                                                class_num = f"{class_num}班"
                                            # 组合完整班级名称
                                            full_class_name = f"{grade_num}级{major}{class_num}"
                                        else:
                                            full_class_name = f"{grade}{major}{class_name}"
                                    elif grade and class_name:
                                        # 统一格式为"2023级金融学2班"
                                        # 提取年级数字（如"2023"）
                                        grade_num = ''.join(filter(str.isdigit, grade))
                                        if grade_num:
                                            # 提取班级数字（如"2班"）
                                            class_num = class_name
                                            # 移除班级名称中的年级信息
                                            class_num = class_num.replace(grade, '').strip()
                                            # 确保班级名称以"班"结尾
                                            if not class_num.endswith('班'):
                                                class_num = f"{class_num}班"
                                            # 组合完整班级名称
                                            full_class_name = f"{grade_num}级{class_num}"
                                        else:
                                            full_class_name = f"{grade}{class_name}"
                                    elif class_name:
                                        # 尝试从班级名称中提取年级和专业信息
                                        # 检查是否已经是"2023级金融学2班"格式
                                        if '级' in class_name and '班' in class_name:
                                            full_class_name = class_name
                                        else:
                                            # 否则使用原始班级名称
                                            full_class_name = class_name
                                    else:
                                        full_class_name = '未分配班级'
                                    
                                    # 如果用户已存在，保留原密码
                                    if username in st.session_state.users_data:
                                        old_password = st.session_state.users_data[username].get('password', password)
                                    else:
                                        old_password = password
                                    
                                    user_data = {
                                        'role': '学生',
                                        'name': str(row.get('姓名', username)),
                                        'password': old_password,
                                        'dormitory': dormitory,
                                        'grade': grade,
                                        'major': major,
                                        'class_name': full_class_name,
                                        'phone': phone,
                                        'gender': gender,
                                        'college': college,
                                        'counselor': counselor
                                    }
                                    # 如果用户不存在，为学生创建初始积分数据
                                    if username not in st.session_state.scores_data:
                                        weekly_score = random.randint(500, 1000)
                                        monthly_score = random.randint(2000, 4000)
                                        st.session_state.scores_data[username] = {
                                            'weekly_score': weekly_score,
                                            'monthly_score': monthly_score,
                                            'class': full_class_name,
                                            'name': str(row.get('姓名', username)),
                                            'grade': grade,
                                            'major': major,
                                            'counselor': counselor
                                        }
                                else:
                                    # 辅导员信息
                                    # 如果用户已存在，保留原密码
                                    if username in st.session_state.users_data:
                                        old_password = st.session_state.users_data[username].get('password', password)
                                    else:
                                        old_password = password
                                    
                                    teacher_grade = str(row.get('年级', ''))
                                    teacher_major = str(row.get('专业', ''))
                                    # 优先从"管理班级"字段读取，然后从"班级"字段读取
                                    teacher_classes = str(row.get('管理班级', row.get('班级', '')))
                                    # 优先从"办公区域"、"办公室区域"字段读取，然后从"办公室地点"和"办公室"字段读取
                                    teacher_office = str(
                                        row.get(
                                            '办公区域', 
                                            row.get(
                                                '办公室区域', 
                                                row.get(
                                                    '办公室地点', 
                                                    row.get('办公室', '')
                                                )
                                            )
                                        )
                                    )
                                    teacher_phone = str(row.get('联系电话', row.get('电话', '')))
                                    teacher_classes_list = []
                                    
                                    # 处理管理班级（支持多个班级，用逗号或顿号分隔）
                                    if teacher_classes:
                                        # 先将顿号替换为逗号，然后分割
                                        teacher_classes = teacher_classes.replace('、', ',')
                                        if ',' in teacher_classes:
                                            teacher_classes_list = [c.strip() for c in teacher_classes.split(',')]
                                        else:
                                            teacher_classes_list = [teacher_classes.strip()]
                                    
                                    # 组合完整班级名称
                                    full_classes_list = []
                                    for cls in teacher_classes_list:
                                        # 统一格式为"2023级金融学2班"
                                        # 检查是否已经是"2023级金融学2班"格式
                                        if '级' in cls and '班' in cls:
                                            # 班级名称已经是标准格式，直接使用
                                            full_classes_list.append(cls)
                                        elif teacher_grade and teacher_major and cls:
                                            # 提取年级数字（如"2023"）
                                            grade_num = ''.join(filter(str.isdigit, teacher_grade))
                                            if grade_num:
                                                # 提取班级数字（如"2班"）
                                                class_num = cls
                                                # 移除班级名称中的年级和专业信息
                                                class_num = class_num.replace(teacher_grade, '').replace(teacher_major, '').strip()
                                                # 确保班级名称以"班"结尾
                                                if not class_num.endswith('班'):
                                                    class_num = f"{class_num}班"
                                                # 组合完整班级名称
                                                full_classes_list.append(f"{grade_num}级{teacher_major}{class_num}")
                                            else:
                                                full_classes_list.append(f"{teacher_grade}{teacher_major}{cls}")
                                        elif teacher_grade and cls:
                                            # 提取年级数字（如"2023"）
                                            grade_num = ''.join(filter(str.isdigit, teacher_grade))
                                            if grade_num:
                                                # 提取班级数字（如"2班"）
                                                class_num = cls
                                                # 移除班级名称中的年级信息
                                                class_num = class_num.replace(teacher_grade, '').strip()
                                                # 确保班级名称以"班"结尾
                                                if not class_num.endswith('班'):
                                                    class_num = f"{class_num}班"
                                                # 组合完整班级名称
                                                full_classes_list.append(f"{grade_num}级{class_num}")
                                            else:
                                                full_classes_list.append(f"{teacher_grade}{cls}")
                                        elif cls:
                                            full_classes_list.append(cls)
                                    
                                    # 支持"姓名"和"辅导员姓名"字段作为姓名
                                    name = str(row.get('姓名', row.get('辅导员姓名', username)))
                                    user_data = {
                                        'role': '辅导员',
                                        'name': name,
                                        'password': old_password,
                                        'classes': ','.join(full_classes_list) if full_classes_list else '',
                                        'class_info': ','.join(full_classes_list) if full_classes_list else '',
                                        'grade': teacher_grade,
                                        'major': teacher_major,
                                        'office': teacher_office,
                                        'phone': teacher_phone
                                    }
                                
                                # 添加到用户数据中
                                st.session_state.users_data[username] = user_data
                                # 如果是新用户，显示生成的密码；如果是旧用户，显示原密码
                                display_password = old_password
                                generated_accounts.append({
                                    '用户名': username,
                                    '姓名': user_data['name'],
                                    '密码': display_password,
                                    '角色': user_data['role']
                                })
                            except Exception as e:
                                st.warning(f"生成账户失败: {str(e)}")
                        
                        if generated_accounts:
                            # 保存用户数据和积分数据到文件
                            save_users_data(st.session_state.users_data)
                            save_scores_data(st.session_state.scores_data)
                            st.success(f"{import_type}导入成功！共生成 {len(generated_accounts)} 个账户")
                            # 显示生成的账户信息
                            st.subheader("📋 生成的账户信息")
                            st.dataframe(pd.DataFrame(generated_accounts), use_container_width=True)
                            # 提供下载账户信息
                            csv = pd.DataFrame(generated_accounts).to_csv(index=False).encode('utf-8-sig')
                            st.download_button(
                                label="📥 下载账户信息",
                                data=csv,
                                file_name=f"{import_type}_账户信息.csv",
                                mime="text/csv"
                            )
                        st.balloons()
                    else:
                        # 处理不同类型的数据导入
                        columns = df_uploaded.columns.tolist()
                        
                        if import_type == "学生信息":
                            # 处理学生信息导入
                            for _, row in df_uploaded.iterrows():
                                try:
                                    # 根据学号生成用户名
                                    if '学号' in df_uploaded.columns:
                                        username = str(row['学号'])
                                    else:
                                        username = str(row.get('姓名', 'user_' + str(random.randint(1000, 9999))))
                                    
                                    # 获取年级和专业
                                    grade = str(row.get('年级', ''))
                                    major = str(row.get('专业', ''))
                                    
                                    # 尝试获取班级相关列，支持多种列名
                                    class_name = ''
                                    class_columns = ['班级', '班', 'class', 'ClassName']
                                    for col in class_columns:
                                        if col in columns:
                                            class_name = str(row.get(col, ''))
                                            break
                                    
                                    # 获取联系电话
                                    phone = str(row.get('联系电话', row.get('电话', '')))
                                    
                                    # 获取宿舍（支持多种列名）
                                    dormitory = ''
                                    dormitory_columns = ['宿舍', '宿舍号', '寝室', '寝室号', 'dormitory', 'Dormitory']
                                    for col in dormitory_columns:
                                        if col in columns:
                                            dormitory = str(row.get(col, ''))
                                            break
                                    if not dormitory:
                                        dormitory = '1号楼101'
                                    
                                    # 获取性别、学院、辅导员
                                    gender = str(row.get('性别', ''))
                                    college = str(row.get('学院', ''))
                                    counselor = str(row.get('辅导员', ''))
                                    
                                    # 组合完整班级名称
                                    full_class_name = ''
                                    if grade and major and class_name:
                                        # 统一格式为"2023级金融学2班"
                                        # 提取年级数字（如"2023"）
                                        grade_num = ''.join(filter(str.isdigit, grade))
                                        if grade_num:
                                            # 提取班级数字（如"2班"）
                                            class_num = class_name
                                            # 移除班级名称中的年级和专业信息
                                            class_num = class_num.replace(grade, '').replace(major, '').strip()
                                            # 确保班级名称以"班"结尾
                                            if not class_num.endswith('班'):
                                                class_num = f"{class_num}班"
                                            # 组合完整班级名称
                                            full_class_name = f"{grade_num}级{major}{class_num}"
                                        else:
                                            full_class_name = f"{grade}{major}{class_name}"
                                    elif grade and class_name:
                                        # 统一格式为"2023级金融学2班"
                                        # 提取年级数字（如"2023"）
                                        grade_num = ''.join(filter(str.isdigit, grade))
                                        if grade_num:
                                            # 提取班级数字（如"2班"）
                                            class_num = class_name
                                            # 移除班级名称中的年级信息
                                            class_num = class_num.replace(grade, '').strip()
                                            # 确保班级名称以"班"结尾
                                            if not class_num.endswith('班'):
                                                class_num = f"{class_num}班"
                                            # 组合完整班级名称
                                            full_class_name = f"{grade_num}级{class_num}"
                                        else:
                                            full_class_name = f"{grade}{class_name}"
                                    elif class_name:
                                        # 尝试从班级名称中提取年级和专业信息
                                        # 检查是否已经是"2023级金融学2班"格式
                                        if '级' in class_name and '班' in class_name:
                                            full_class_name = class_name
                                        else:
                                            # 否则使用原始班级名称
                                            full_class_name = class_name
                                    else:
                                        full_class_name = '未分配班级'
                                    
                                    # 更新或添加学生数据
                                    if username in st.session_state.users_data:
                                        # 更新现有学生信息
                                        st.session_state.users_data[username].update({
                                            'name': str(row.get('姓名', st.session_state.users_data[username].get('name', username))),
                                            'dormitory': str(row.get('宿舍', st.session_state.users_data[username].get('dormitory', '1号楼101'))),
                                            'grade': grade,
                                            'major': major,
                                            'class_name': full_class_name,
                                            'phone': phone,
                                            'gender': gender,
                                            'college': college,
                                            'counselor': counselor
                                        })
                                    else:
                                        # 添加新学生
                                        st.session_state.users_data[username] = {
                                            'role': '学生',
                                            'name': str(row.get('姓名', username)),
                                            'password': '12345678',  # 默认密码
                                            'dormitory': str(row.get('宿舍', '1号楼101')),
                                            'grade': grade,
                                            'major': major,
                                            'class_name': full_class_name,
                                            'phone': phone,
                                            'gender': gender,
                                            'college': college,
                                            'counselor': counselor
                                        }
                                    
                                    # 更新或添加积分数据
                                    if username not in st.session_state.scores_data:
                                        st.session_state.scores_data[username] = {
                                            'weekly_score': 0,
                                            'monthly_score': 0,
                                            'class': full_class_name,
                                            'name': str(row.get('姓名', username)),
                                            'grade': grade,
                                            'major': major,
                                            'counselor': counselor
                                        }
                                    else:
                                        # 更新现有积分数据
                                        st.session_state.scores_data[username].update({
                                            'class': full_class_name,
                                            'name': str(row.get('姓名', username)),
                                            'grade': grade,
                                            'major': major,
                                            'counselor': counselor
                                        })
                                except Exception as e:
                                    st.warning(f"处理学生数据失败: {str(e)}")
                        elif import_type == "教师信息" or import_type == "辅导员信息":
                            # 处理教师或辅导员信息导入
                            for _, row in df_uploaded.iterrows():
                                try:
                                    # 根据工号生成用户名
                                    if '工号' in df_uploaded.columns:
                                        username = str(row['工号'])
                                    else:
                                        username = str(row.get('姓名', 'teacher_' + str(random.randint(1000, 9999))))
                                    
                                    # 处理管理班级
                                    teacher_grade = str(row.get('年级', ''))
                                    teacher_major = str(row.get('专业', ''))
                                    # 优先从"管理班级"字段读取，然后从"班级"字段读取
                                    teacher_classes = str(row.get('管理班级', row.get('班级', '')))
                                    # 优先从"办公区域"、"办公室区域"字段读取，然后从"办公室地点"和"办公室"字段读取
                                    teacher_office = str(
                                        row.get(
                                            '办公区域', 
                                            row.get(
                                                '办公室区域', 
                                                row.get(
                                                    '办公室地点', 
                                                    row.get('办公室', '')
                                                )
                                            )
                                        )
                                    )
                                    teacher_phone = str(row.get('联系电话', row.get('电话', '')))
                                    teacher_classes_list = []
                                    
                                    if teacher_classes:
                                        if ',' in teacher_classes:
                                            teacher_classes_list = [c.strip() for c in teacher_classes.split(',')]
                                        else:
                                            teacher_classes_list = [teacher_classes.strip()]
                                    
                                    # 组合完整班级名称
                                    full_classes_list = []
                                    for cls in teacher_classes_list:
                                        # 统一格式为"2023级金融学2班"
                                        # 检查是否已经是"2023级金融学2班"格式
                                        if '级' in cls and '班' in cls:
                                            # 班级名称已经是标准格式，直接使用
                                            full_classes_list.append(cls)
                                        elif teacher_grade and teacher_major and cls:
                                            # 提取年级数字（如"2023"）
                                            grade_num = ''.join(filter(str.isdigit, teacher_grade))
                                            if grade_num:
                                                # 提取班级数字（如"2班"）
                                                class_num = cls
                                                # 移除班级名称中的年级和专业信息
                                                class_num = class_num.replace(teacher_grade, '').replace(teacher_major, '').strip()
                                                # 确保班级名称以"班"结尾
                                                if not class_num.endswith('班'):
                                                    class_num = f"{class_num}班"
                                                # 组合完整班级名称
                                                full_classes_list.append(f"{grade_num}级{teacher_major}{class_num}")
                                            else:
                                                full_classes_list.append(f"{teacher_grade}{teacher_major}{cls}")
                                        elif teacher_grade and cls:
                                            # 提取年级数字（如"2023"）
                                            grade_num = ''.join(filter(str.isdigit, teacher_grade))
                                            if grade_num:
                                                # 提取班级数字（如"2班"）
                                                class_num = cls
                                                # 移除班级名称中的年级信息
                                                class_num = class_num.replace(teacher_grade, '').strip()
                                                # 确保班级名称以"班"结尾
                                                if not class_num.endswith('班'):
                                                    class_num = f"{class_num}班"
                                                # 组合完整班级名称
                                                full_classes_list.append(f"{grade_num}级{class_num}")
                                            else:
                                                full_classes_list.append(f"{teacher_grade}{cls}")
                                        elif cls:
                                            full_classes_list.append(cls)
                                    
                                    # 更新或添加教师数据
                                    if username in st.session_state.users_data:
                                        # 更新现有教师信息
                                        st.session_state.users_data[username].update({
                                            'name': str(row.get('姓名', st.session_state.users_data[username].get('name', username))),
                                            'classes': ','.join(full_classes_list) if full_classes_list else '',
                                            'class_info': ','.join(full_classes_list) if full_classes_list else '',
                                            'grade': teacher_grade,
                                            'major': teacher_major,
                                            'office': teacher_office,
                                            'phone': teacher_phone
                                        })
                                    else:
                                        # 添加新教师
                                        st.session_state.users_data[username] = {
                                            'role': '老师',
                                            'name': str(row.get('姓名', username)),
                                            'password': '12345678',  # 默认密码
                                            'classes': ','.join(full_classes_list) if full_classes_list else '',
                                            'class_info': ','.join(full_classes_list) if full_classes_list else '',
                                            'grade': teacher_grade,
                                            'major': teacher_major,
                                            'office': teacher_office,
                                            'phone': teacher_phone
                                        }
                                except Exception as e:
                                    st.warning(f"处理教师数据失败: {str(e)}")
                        elif import_type == "能耗数据":
                            # 处理能耗数据导入
                            if 'energy_data' not in st.session_state:
                                st.session_state.energy_data = []
                            
                            for _, row in df_uploaded.iterrows():
                                try:
                                    energy_record = {
                                        '日期': str(row.get('日期', '')),
                                        '区域': str(row.get('区域', '')),
                                        '水耗 (吨)': float(row.get('水耗 (吨)', 0)),
                                        '电耗 (kWh)': float(row.get('电耗 (kWh)', 0)),
                                        '节能率 (%)': float(row.get('节能率 (%)', 0))
                                    }
                                    st.session_state.energy_data.append(energy_record)
                                except Exception as e:
                                    st.warning(f"处理能耗数据失败: {str(e)}")
                        
                        # 保存数据
                        if import_type in ["学生信息", "教师信息", "辅导员信息"]:
                            save_users_data(st.session_state.users_data)
                            save_scores_data(st.session_state.scores_data)
                        elif import_type == "能耗数据":
                            # 保存能耗数据到文件
                            import json
                            import os
                            ENERGY_DATA_FILE = 'energy_data.json'
                            try:
                                with open(ENERGY_DATA_FILE, 'w', encoding='utf-8') as f:
                                    json.dump(st.session_state.energy_data, f, ensure_ascii=False, indent=2)
                            except Exception as e:
                                st.warning(f"保存能耗数据失败: {str(e)}")
                        
                        st.success(f"{import_type}导入成功！")
                        st.balloons()
            else:
                # Excel文件 - 获取所有sheet
                excel_file = pd.ExcelFile(uploaded_file)
                sheet_names = excel_file.sheet_names
                
                # 记录上传的文件
                if 'uploaded_files' not in st.session_state:
                    st.session_state.uploaded_files = []
                
                import datetime
                file_info = {
                    'name': uploaded_file.name,
                    'type': uploaded_file.type,
                    'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # 检查文件是否已经记录
                file_exists = False
                for existing_file in st.session_state.uploaded_files:
                    if existing_file['name'] == file_info['name'] and existing_file['date'] == file_info['date']:
                        file_exists = True
                        break
                
                if not file_exists:
                    st.session_state.uploaded_files.append(file_info)
                    save_uploaded_files(st.session_state.uploaded_files)
                
                if len(sheet_names) > 1:
                    st.info(f"检测到 {len(sheet_names)} 个工作表")
                    
                    # 简化的工作表选择
                    st.markdown("#### 选择工作表")
                    
                    # 快捷操作按钮
                    col_btn1, col_btn2 = st.columns(2, gap="small")
                    with col_btn1:
                        if st.button("全选", key="btn_select_all"):
                            st.session_state["select_sheets"] = sheet_names
                            st.rerun()
                    with col_btn2:
                        if st.button("清空", key="btn_clear_all"):
                            st.session_state["select_sheets"] = []
                            st.rerun()
                    
                    # 多选框
                    selected_sheets = st.multiselect(
                        "", 
                        sheet_names, 
                        default=st.session_state.get("select_sheets", sheet_names),
                        key="select_sheets"
                    )
                    
                    # 显示选中的工作表数量
                    st.markdown(f"已选择 **{len(selected_sheets)}** 个工作表")
                    
                    # 导入按钮
                    if st.button("导入数据", type="primary", use_container_width=True):
                        if selected_sheets:
                            # 先清除虚拟账户
                            new_users_data = {}
                            for username, user_info in st.session_state.users_data.items():
                                if not user_info.get(VIRTUAL_DATA_FLAG, False):
                                    new_users_data[username] = user_info
                            st.session_state.users_data = new_users_data
                            
                            # 清除虚拟积分数据
                            new_scores_data = {}
                            for username, score_info in st.session_state.scores_data.items():
                                if not score_info.get(VIRTUAL_DATA_FLAG, False):
                                    new_scores_data[username] = score_info
                            st.session_state.scores_data = new_scores_data
                            
                            # 保存清除虚拟数据后的状态
                            save_users_data(st.session_state.users_data)
                            save_scores_data(st.session_state.scores_data)
                            
                            if import_type in ["学生信息", "教师信息", "辅导员信息"] and generate_account:
                                generated_accounts = []
                                for sheet_name in selected_sheets:
                                    df_uploaded = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                                    columns = df_uploaded.columns.tolist()
                                    for _, row in df_uploaded.iterrows():
                                        try:
                                            if import_type == "学生信息" and '学号' in columns:
                                                username = str(row['学号'])
                                            elif import_type == "辅导员信息" and '工号' in columns:
                                                # 辅导员优先使用姓名作为用户名，其次使用工号
                                                # 支持"姓名"和"辅导员姓名"字段
                                                username = str(row.get('姓名', row.get('辅导员姓名', str(row['工号']))))
                                            elif import_type == "辅导员信息" and '学号' in columns:
                                                # 如果是辅导员信息导入，但文件中包含学号字段，说明可能是学生信息文件
                                                st.warning(f"导入类型为{import_type}，但文件中包含'学号'字段，可能是学生信息文件。请选择正确的导入类型。")
                                                continue
                                            else:
                                                # 优先使用姓名作为用户名，支持"姓名"和"辅导员姓名"字段
                                                username = str(row.get('姓名', row.get('辅导员姓名', 'user_' + str(random.randint(1000, 9999)))))
                                            
                                            password = generate_password()
                                            
                                            if import_type == "学生信息":
                                                # 构建班级名称（年级+专业+班级）
                                                grade = str(row.get('年级', ''))
                                                major = str(row.get('专业', ''))
                                                # 尝试获取班级相关列，支持多种列名
                                                class_name = ''
                                                class_columns = ['班级', '班', 'class', 'ClassName']
                                                for col in class_columns:
                                                    if col in columns:
                                                        class_name = str(row.get(col, ''))
                                                        break
                                                
                                                # 获取联系电话
                                                phone = str(row.get('联系电话', row.get('电话', '')))
                                                
                                                # 获取性别、学院、辅导员
                                                gender = str(row.get('性别', ''))
                                                college = str(row.get('学院', ''))
                                                counselor = str(row.get('辅导员', ''))
                                                
                                                # 组合完整班级名称
                                                full_class_name = ''
                                                if grade and major and class_name:
                                                    full_class_name = f"{grade}{major}{class_name}"
                                                elif grade and class_name:
                                                    full_class_name = f"{grade}{class_name}"
                                                elif class_name:
                                                    full_class_name = class_name
                                                else:
                                                    full_class_name = '未分配班级'
                                                
                                                # 如果用户已存在，保留原密码
                                                if username in st.session_state.users_data:
                                                    old_password = st.session_state.users_data[username].get('password', password)
                                                else:
                                                    old_password = password
                                                
                                                user_data = {
                                                    'role': '学生',
                                                    'name': str(row.get('姓名', username)),
                                                    'password': old_password,
                                                    'dormitory': str(row.get('宿舍', '1号楼101')),
                                                    'grade': grade,
                                                    'major': major,
                                                    'class_name': full_class_name,
                                                    'phone': phone,
                                                    'gender': gender,
                                                    'college': college,
                                                    'counselor': counselor
                                                }
                                                # 如果用户不存在，为学生创建初始积分数据
                                                if username not in st.session_state.scores_data:
                                                    weekly_score = random.randint(500, 1000)
                                                    monthly_score = random.randint(2000, 4000)
                                                    st.session_state.scores_data[username] = {
                                                        'weekly_score': weekly_score,
                                                        'monthly_score': monthly_score,
                                                        'class': full_class_name,
                                                        'name': str(row.get('姓名', username)),
                                                        'grade': grade,
                                                        'major': major
                                                    }
                                            else:
                                                # 教师信息
                                                teacher_grade = str(row.get('年级', ''))
                                                teacher_major = str(row.get('专业', ''))
                                                # 优先从"管理班级"字段读取，然后从"班级"字段读取
                                                teacher_classes = str(row.get('管理班级', row.get('班级', '')))
                                                # 优先从"办公区域"、"办公室区域"字段读取，然后从"办公室地点"和"办公室"字段读取
                                                teacher_office = str(row.get('办公区域', row.get('办公室区域', row.get('办公室地点', row.get('办公室', '')))))
                                                teacher_phone = str(row.get('联系电话', row.get('电话', '')))
                                                teacher_classes_list = []
                                                
                                                # 处理管理班级（支持多个班级，用逗号分隔）
                                                if teacher_classes:
                                                    if ',' in teacher_classes:
                                                        teacher_classes_list = [c.strip() for c in teacher_classes.split(',')]
                                                    else:
                                                        teacher_classes_list = [teacher_classes.strip()]
                                                
                                                # 组合完整班级名称
                                                full_classes_list = []
                                                for cls in teacher_classes_list:
                                                    # 检查班级名称是否已经包含年级和专业信息
                                                    if '级' in cls and '班' in cls:
                                                        # 班级名称已经包含完整信息，直接使用
                                                        full_classes_list.append(cls)
                                                    elif teacher_grade and teacher_major and cls:
                                                        full_classes_list.append(f"{teacher_grade}{teacher_major}{cls}")
                                                    elif teacher_grade and cls:
                                                        full_classes_list.append(f"{teacher_grade}{cls}")
                                                    elif cls:
                                                        full_classes_list.append(cls)
                                                
                                                # 支持"姓名"和"辅导员姓名"字段作为姓名
                                                name = str(row.get('姓名', row.get('辅导员姓名', username)))
                                                # 如果用户已存在，保留原密码
                                                if username in st.session_state.users_data:
                                                    old_password = st.session_state.users_data[username].get('password', password)
                                                else:
                                                    old_password = password
                                                
                                                user_data = {
                                                    'role': '辅导员',
                                                    'name': name,
                                                    'password': old_password,
                                                    'classes': ','.join(full_classes_list) if full_classes_list else '',
                                                    'class_info': ','.join(full_classes_list) if full_classes_list else '',
                                                    'grade': teacher_grade,
                                                    'major': teacher_major,
                                                    'office': teacher_office,
                                                    'phone': teacher_phone
                                                }
                                            
                                            st.session_state.users_data[username] = user_data
                                            # 如果是新用户，显示生成的密码；如果是旧用户，显示原密码
                                            display_password = old_password
                                            
                                            generated_accounts.append({
                                                '用户名': username,
                                                '姓名': user_data['name'],
                                                '密码': display_password,
                                                '角色': user_data['role'],
                                                '工作表': sheet_name
                                            })
                                        except Exception as e:
                                            st.warning(f"工作表 {sheet_name} 生成账户失败: {str(e)}")
                                
                                if generated_accounts:
                                    save_users_data(st.session_state.users_data)
                                    save_scores_data(st.session_state.scores_data)
                                    st.success(f"{import_type}导入成功！共生成 {len(generated_accounts)} 个账户")
                                    st.subheader("📋 生成的账户信息")
                                    st.dataframe(pd.DataFrame(generated_accounts), use_container_width=True)
                                    csv = pd.DataFrame(generated_accounts).to_csv(index=False).encode('utf-8-sig')
                                    st.download_button(
                                        label="📥 下载账户信息",
                                        data=csv,
                                        file_name=f"{import_type}_账户信息.csv",
                                        mime="text/csv"
                                    )
                                st.balloons()
                            else:
                                # 处理Excel文件导入（不生成账户）
                                if import_type == "学生信息":
                                    for sheet_name in selected_sheets:
                                        df_uploaded = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                                        columns = df_uploaded.columns.tolist()
                                        for _, row in df_uploaded.iterrows():
                                            try:
                                                if '学号' in df_uploaded.columns:
                                                    username = str(row['学号'])
                                                else:
                                                    username = str(row.get('姓名', 'user_' + str(random.randint(1000, 9999))))
                                                
                                                # 获取年级和专业
                                                grade = str(row.get('年级', ''))
                                                major = str(row.get('专业', ''))
                                                
                                                # 尝试获取班级相关列，支持多种列名
                                                class_name = ''
                                                class_columns = ['班级', '班', 'class', 'ClassName']
                                                for col in class_columns:
                                                    if col in columns:
                                                        class_name = str(row.get(col, ''))
                                                        break
                                                
                                                # 获取联系电话
                                                phone = str(row.get('联系电话', row.get('电话', '')))
                                                
                                                # 获取性别、学院、辅导员
                                                gender = str(row.get('性别', ''))
                                                college = str(row.get('学院', ''))
                                                counselor = str(row.get('辅导员', ''))
                                                
                                                # 组合完整班级名称
                                                full_class_name = ''
                                                if grade and major and class_name:
                                                    full_class_name = f"{grade}{major}{class_name}"
                                                elif grade and class_name:
                                                    full_class_name = f"{grade}{class_name}"
                                                elif class_name:
                                                    full_class_name = class_name
                                                else:
                                                    full_class_name = '未分配班级'
                                                
                                                if username in st.session_state.users_data:
                                                    # 更新现有学生信息
                                                    st.session_state.users_data[username].update({
                                                        'name': str(row.get('姓名', st.session_state.users_data[username].get('name', username))),
                                                        'dormitory': str(row.get('宿舍', st.session_state.users_data[username].get('dormitory', '1号楼101'))),
                                                        'grade': grade,
                                                        'major': major,
                                                        'class_name': full_class_name,
                                                        'phone': phone,
                                                        'gender': gender,
                                                        'college': college,
                                                        'counselor': counselor
                                                    })
                                                else:
                                                    # 添加新学生
                                                    st.session_state.users_data[username] = {
                                                        'role': '学生',
                                                        'name': str(row.get('姓名', username)),
                                                        'password': '12345678',
                                                        'dormitory': str(row.get('宿舍', '1号楼101')),
                                                        'grade': grade,
                                                        'major': major,
                                                        'class_name': full_class_name,
                                                        'phone': phone,
                                                        'gender': gender,
                                                        'college': college,
                                                        'counselor': counselor
                                                    }
                                                
                                                if username not in st.session_state.scores_data:
                                                    st.session_state.scores_data[username] = {
                                                        'weekly_score': 0,
                                                        'monthly_score': 0,
                                                        'class': full_class_name,
                                                        'name': str(row.get('姓名', username)),
                                                        'grade': grade,
                                                        'major': major
                                                    }
                                            except Exception as e:
                                                st.warning(f"处理工作表 {sheet_name} 数据失败: {str(e)}")
                                
                                # 保存数据
                                if import_type in ["学生信息", "教师信息", "辅导员信息"]:
                                    save_users_data(st.session_state.users_data)
                                    save_scores_data(st.session_state.scores_data)
                                elif import_type == "能耗数据":
                                    import json
                                    import os
                                    ENERGY_DATA_FILE = 'energy_data.json'
                                    try:
                                        with open(ENERGY_DATA_FILE, 'w', encoding='utf-8') as f:
                                            json.dump(st.session_state.energy_data, f, ensure_ascii=False, indent=2)
                                    except Exception as e:
                                        st.warning(f"保存能耗数据失败: {str(e)}")
                                st.success(f"{import_type}导入成功！共导入 {len(selected_sheets)} 个工作表")
                                st.balloons()
                        else:
                            st.warning("请至少选择一个工作表")
                else:
                    df_uploaded = pd.read_excel(uploaded_file, sheet_name=sheet_names[0])
                    st.markdown("---")
                    st.markdown(f"### 工作表：{sheet_names[0]}")
                    st.dataframe(df_uploaded, use_container_width=True)
                    
                    if st.button("导入数据", type="primary", key="import_data_button_2"):
                        # 先清除虚拟账户
                        new_users_data = {}
                        for username, user_info in st.session_state.users_data.items():
                            if not user_info.get(VIRTUAL_DATA_FLAG, False):
                                new_users_data[username] = user_info
                        st.session_state.users_data = new_users_data
                        
                        # 清除虚拟积分数据
                        new_scores_data = {}
                        for username, score_info in st.session_state.scores_data.items():
                            if not score_info.get(VIRTUAL_DATA_FLAG, False):
                                new_scores_data[username] = score_info
                        st.session_state.scores_data = new_scores_data
                        
                        # 保存清除虚拟数据后的状态
                        save_users_data(st.session_state.users_data)
                        save_scores_data(st.session_state.scores_data)
                        
                        if import_type in ["学生信息", "教师信息", "辅导员信息"] and generate_account:
                            generated_accounts = []
                            columns = df_uploaded.columns.tolist()
                            for _, row in df_uploaded.iterrows():
                                try:
                                    if '学号' in columns:
                                        username = str(row['学号'])
                                    elif '工号' in columns:
                                        username = str(row['工号'])
                                    else:
                                        username = str(row.get('姓名', 'user_' + str(random.randint(1000, 9999))))
                                    
                                    password = generate_password()
                                    
                                    # 如果用户已存在，保留原密码
                                    if username in st.session_state.users_data:
                                        old_password = st.session_state.users_data[username].get('password', password)
                                    else:
                                        old_password = password
                                    
                                    if import_type == "学生信息":
                                        # 获取宿舍（支持多种列名）
                                        dormitory = ''
                                        dormitory_columns = ['宿舍', '宿舍号', '寝室', '寝室号', 'dormitory', 'Dormitory']
                                        for col in dormitory_columns:
                                            if col in columns:
                                                dormitory = str(row.get(col, ''))
                                                break
                                        if not dormitory:
                                            dormitory = '1号楼101'
                                        
                                        user_data = {
                                            'role': '学生',
                                            'name': str(row.get('姓名', username)),
                                            'password': old_password,
                                            'dormitory': dormitory
                                        }
                                        # 如果用户不存在，为学生创建初始积分数据
                                        if username not in st.session_state.scores_data:
                                            student_class = str(row.get('班级', '未分配班级'))
                                            weekly_score = random.randint(500, 1000)
                                            monthly_score = random.randint(2000, 4000)
                                            st.session_state.scores_data[username] = {
                                                'weekly_score': weekly_score,
                                                'monthly_score': monthly_score,
                                                'class': student_class,
                                                'name': str(row.get('姓名', username))
                                            }
                                    elif import_type == "辅导员信息":
                                        # 处理管理班级
                                        teacher_grade = str(row.get('年级', ''))
                                        teacher_major = str(row.get('专业', ''))
                                        # 优先从"管理班级"字段读取，然后从"班级"字段读取
                                        teacher_classes = str(row.get('管理班级', row.get('班级', '')))
                                        # 优先从"办公区域"、"办公室区域"字段读取，然后从"办公室地点"和"办公室"字段读取
                                        teacher_office = str(
                                            row.get(
                                                '办公区域', 
                                                row.get(
                                                    '办公室区域', 
                                                    row.get(
                                                        '办公室地点', 
                                                        row.get('办公室', '')
                                                    )
                                                )
                                            )
                                        )
                                        teacher_phone = str(row.get('联系电话', row.get('电话', '')))
                                        teacher_classes_list = []
                                        
                                        if teacher_classes:
                                            if ',' in teacher_classes:
                                                teacher_classes_list = [c.strip() for c in teacher_classes.split(',')]
                                            else:
                                                teacher_classes_list = [teacher_classes.strip()]
                                        
                                        # 组合完整班级名称
                                        full_classes_list = []
                                        for cls in teacher_classes_list:
                                            # 检查班级名称是否已经包含年级和专业信息
                                            if '级' in cls and '班' in cls:
                                                # 班级名称已经包含完整信息，直接使用
                                                full_classes_list.append(cls)
                                            elif teacher_grade and teacher_major and cls:
                                                full_classes_list.append(f"{teacher_grade}{teacher_major}{cls}")
                                            elif teacher_grade and cls:
                                                full_classes_list.append(f"{teacher_grade}{cls}")
                                            elif cls:
                                                full_classes_list.append(cls)
                                        
                                        user_data = {
                                            'role': '辅导员',
                                            'name': str(row.get('姓名', username)),
                                            'password': old_password,
                                            'classes': ','.join(full_classes_list) if full_classes_list else '',
                                            'class_info': ','.join(full_classes_list) if full_classes_list else '',
                                            'grade': teacher_grade,
                                            'major': teacher_major,
                                            'office': teacher_office,
                                            'phone': teacher_phone
                                        }
                                    else:
                                        user_data = {
                                            'role': '老师',
                                            'name': str(row.get('姓名', username)),
                                            'password': old_password,
                                            'classes': str(row.get('班级', ''))
                                        }
                                    
                                    st.session_state.users_data[username] = user_data
                                    # 如果是新用户，显示生成的密码；如果是旧用户，显示原密码
                                    display_password = old_password
                                    generated_accounts.append({
                                        '用户名': username,
                                        '姓名': user_data['name'],
                                        '密码': display_password,
                                        '角色': user_data['role']
                                    })
                                except Exception as e:
                                    st.warning(f"生成账户失败: {str(e)}")
                            
                            if generated_accounts:
                                save_users_data(st.session_state.users_data)
                                save_scores_data(st.session_state.scores_data)
                                st.success(f"{import_type}导入成功！共生成 {len(generated_accounts)} 个账户")
                                st.subheader("📋 生成的账户信息")
                                st.dataframe(pd.DataFrame(generated_accounts), use_container_width=True)
                                csv = pd.DataFrame(generated_accounts).to_csv(index=False).encode('utf-8-sig')
                                st.download_button(
                                    label="📥 下载账户信息",
                                    data=csv,
                                    file_name=f"{import_type}_账户信息.csv",
                                    mime="text/csv"
                                )
                            st.balloons()
                        else:
                            # 处理单个Excel工作表导入（不生成账户）
                            if import_type == "学生信息":
                                for _, row in df_uploaded.iterrows():
                                    try:
                                        if '学号' in df_uploaded.columns:
                                            username = str(row['学号'])
                                        else:
                                            username = str(row.get('姓名', 'user_' + str(random.randint(1000, 9999))))
                                        
                                        # 尝试获取年级和专业信息
                                        grade = str(row.get('年级', ''))
                                        major = str(row.get('专业', ''))
                                        
                                        # 尝试获取班级相关列，支持多种列名
                                        class_name = ''
                                        class_columns = ['班级', '班', 'class', 'ClassName']
                                        for col in class_columns:
                                            if col in df_uploaded.columns:
                                                class_name = str(row.get(col, ''))
                                                break
                                        
                                        # 获取联系电话
                                        phone = str(row.get('联系电话', row.get('电话', '')))
                                        
                                        # 获取宿舍（支持多种列名）
                                        dormitory = ''
                                        dormitory_columns = ['宿舍', '宿舍号', '寝室', '寝室号', 'dormitory', 'Dormitory']
                                        for col in dormitory_columns:
                                            if col in df_uploaded.columns:
                                                dormitory = str(row.get(col, ''))
                                                break
                                        if not dormitory:
                                            dormitory = '1号楼101'
                                        
                                        # 获取性别、学院、辅导员
                                        gender = str(row.get('性别', ''))
                                        college = str(row.get('学院', ''))
                                        counselor = str(row.get('辅导员', ''))
                                        
                                        # 组合完整班级名称
                                        full_class_name = ''
                                        if grade and major and class_name:
                                            full_class_name = f"{grade}{major}{class_name}"
                                        elif grade and class_name:
                                            full_class_name = f"{grade}{class_name}"
                                        elif class_name:
                                            full_class_name = class_name
                                        else:
                                            full_class_name = '未分配班级'
                                        
                                        if username in st.session_state.users_data:
                                            # 更新现有学生信息
                                            st.session_state.users_data[username].update({
                                                'name': str(row.get('姓名', st.session_state.users_data[username].get('name', username))),
                                                'dormitory': dormitory if dormitory else st.session_state.users_data[username].get('dormitory', '1号楼101'),
                                                'grade': grade,
                                                'major': major,
                                                'class_name': full_class_name,
                                                'phone': phone,
                                                'gender': gender,
                                                'college': college,
                                                'counselor': counselor
                                            })
                                        else:
                                            # 添加新学生
                                            st.session_state.users_data[username] = {
                                                'role': '学生',
                                                'name': str(row.get('姓名', username)),
                                                'password': '12345678',
                                                'dormitory': dormitory,
                                                'grade': grade,
                                                'major': major,
                                                'class_name': full_class_name,
                                                'phone': phone,
                                                'gender': gender,
                                                'college': college,
                                                'counselor': counselor
                                            }
                                        
                                        if username not in st.session_state.scores_data:
                                            st.session_state.scores_data[username] = {
                                                'weekly_score': 0,
                                                'monthly_score': 0,
                                                'class': full_class_name,
                                                'name': str(row.get('姓名', username)),
                                                'grade': grade,
                                                'major': major
                                            }
                                    except Exception as e:
                                        st.warning(f"处理数据失败: {str(e)}")
                                
                                # 保存数据
                                save_users_data(st.session_state.users_data)
                                save_scores_data(st.session_state.scores_data)
                            elif import_type == "辅导员信息":
                                for _, row in df_uploaded.iterrows():
                                    try:
                                        if '工号' in df_uploaded.columns:
                                            username = str(row['工号'])
                                        elif '学号' in df_uploaded.columns:
                                            # 如果是辅导员信息导入，但文件中包含学号字段，说明可能是学生信息文件
                                            st.warning(f"导入类型为{import_type}，但文件中包含'学号'字段，可能是学生信息文件。请选择正确的导入类型。")
                                            continue
                                        else:
                                            username = str(row.get('姓名', 'teacher_' + str(random.randint(1000, 9999))))
                                        
                                        teacher_grade = str(row.get('年级', ''))
                                        teacher_major = str(row.get('专业', ''))
                                        # 优先从"管理班级"字段读取，然后从"班级"字段读取
                                        teacher_classes = str(row.get('管理班级', row.get('班级', '')))
                                        # 优先从"办公区域"、"办公室区域"字段读取，然后从"办公室地点"和"办公室"字段读取
                                        teacher_office = str(row.get('办公区域', row.get('办公室区域', row.get('办公室地点', row.get('办公室', '')))))
                                        teacher_phone = str(row.get('联系电话', row.get('电话', '')))
                                        teacher_classes_list = []
                                        
                                        # 处理管理班级（支持多个班级，用逗号或顿号分隔）
                                        if teacher_classes:
                                            # 先将顿号替换为逗号，然后分割
                                            teacher_classes = teacher_classes.replace('、', ',')
                                            if ',' in teacher_classes:
                                                teacher_classes_list = [c.strip() for c in teacher_classes.split(',')]
                                            else:
                                                teacher_classes_list = [teacher_classes.strip()]
                                        
                                        full_classes_list = []
                                        for cls in teacher_classes_list:
                                            # 检查班级名称是否已经包含年级和专业信息
                                            if '级' in cls and '班' in cls:
                                                # 班级名称已经包含完整信息，直接使用
                                                full_classes_list.append(cls)
                                            elif teacher_grade and teacher_major and cls:
                                                full_classes_list.append(f"{teacher_grade}{teacher_major}{cls}")
                                            elif teacher_grade and cls:
                                                full_classes_list.append(f"{teacher_grade}{cls}")
                                            elif cls:
                                                full_classes_list.append(cls)
                                        
                                        if username in st.session_state.users_data:
                                            # 保留原密码，只更新其他信息
                                            st.session_state.users_data[username].update({
                                                'name': str(row.get('姓名', st.session_state.users_data[username].get('name', username))),
                                                'classes': ','.join(full_classes_list) if full_classes_list else '',
                                                'class_info': ','.join(full_classes_list) if full_classes_list else '',
                                                'grade': teacher_grade,
                                                'major': teacher_major,
                                                'office': teacher_office,
                                                'phone': teacher_phone
                                            })
                                        else:
                                            # 添加新辅导员，生成随机密码
                                            password = generate_password()
                                            st.session_state.users_data[username] = {
                                                'role': '辅导员',
                                                'name': str(row.get('姓名', username)),
                                                'password': password,
                                                'classes': ','.join(full_classes_list) if full_classes_list else '',
                                                'class_info': ','.join(full_classes_list) if full_classes_list else '',
                                                'grade': teacher_grade,
                                                'major': teacher_major,
                                                'office': teacher_office,
                                                'phone': teacher_phone
                                            }
                                    except Exception as e:
                                        st.warning(f"处理数据失败: {str(e)}")
                                
                                # 保存数据
                                save_users_data(st.session_state.users_data)
                                save_scores_data(st.session_state.scores_data)
                            elif import_type == "能耗数据":
                                if 'energy_data' not in st.session_state:
                                    st.session_state.energy_data = []
                                
                                for _, row in df_uploaded.iterrows():
                                    try:
                                        energy_record = {
                                            '日期': str(row.get('日期', '')),
                                            '区域': str(row.get('区域', '')),
                                            '水耗 (吨)': float(row.get('水耗 (吨)', 0)),
                                            '电耗 (kWh)': float(row.get('电耗 (kWh)', 0)),
                                            '节能率 (%)': float(row.get('节能率 (%)', 0))
                                        }
                                        st.session_state.energy_data.append(energy_record)
                                    except Exception as e:
                                        st.warning(f"处理数据失败: {str(e)}")
                            
                            # 保存数据
                            if import_type in ["学生信息", "教师信息"]:
                                save_users_data(st.session_state.users_data)
                                save_scores_data(st.session_state.scores_data)
                            elif import_type == "能耗数据":
                                import json
                                import os
                                ENERGY_DATA_FILE = 'energy_data.json'
                                try:
                                    with open(ENERGY_DATA_FILE, 'w', encoding='utf-8') as f:
                                        json.dump(st.session_state.energy_data, f, ensure_ascii=False, indent=2)
                                except Exception as e:
                                    st.warning(f"保存能耗数据失败: {str(e)}")
                            
                            st.success(f"{import_type}导入成功！")
                            st.balloons()
        
        st.markdown("---")
        
        # 查看已生成账户
        st.subheader("👥 账户管理")
        
        # 角色筛选功能
        role_filter = st.selectbox(
            "按角色筛选",
            options=["所有角色", "管理者", "辅导员", "学生"],
            help="选择要查看的用户角色"
        )
        
        # 显示账户列表
        users_data = st.session_state.users_data
        account_list = []
        for username, user_info in users_data.items():
            # 根据角色筛选
            if role_filter != "所有角色" and user_info['role'] != role_filter:
                continue
            
            # 构建账户信息
            account_info = {
                '用户名': username,
                '姓名': user_info['name'],
                '角色': user_info['role'],
                '密码': user_info.get('password', '********')
            }
            
            # 根据角色添加不同的信息
            if user_info.get('role') == '辅导员' or user_info.get('role') == '老师':
                account_info['管理班级'] = user_info.get('classes', user_info.get('class_info', ''))
                account_info['办公区域'] = user_info.get('office', user_info.get('办公区域', ''))
                account_info['联系电话'] = user_info.get('phone', user_info.get('联系电话', ''))
            elif user_info.get('role') == '学生':
                account_info['班级'] = user_info.get('class_name', '')
                account_info['宿舍'] = user_info.get('dormitory', '')
                account_info['辅导员'] = user_info.get('counselor', '')
                account_info['联系电话'] = user_info.get('phone', '')
                
            account_list.append(account_info)
        
        df_accounts = pd.DataFrame(account_list)
        st.dataframe(df_accounts, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 刷新账户列表"):
                st.rerun()
            with col2:
                csv = df_accounts.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="📥 导出所有账户",
                    data=csv,
                    file_name="系统账户列表.csv",
                    mime="text/csv"
                )
        
        st.markdown("---")
        
        # 数据导出
        st.subheader("📤 数据导出")
        
        export_type = st.selectbox("选择导出类型", ["学生信息", "辅导员信息", "能耗数据", "节能打卡记录", "积分表"])
        
        if export_type == "学生信息":
            # 使用真实的学生数据
            student_data = {
                '学号': [],
                '姓名': [],
                '性别': [],
                '学院': [],
                '年级': [],
                '专业': [],
                '班级': [],
                '宿舍': [],
                '辅导员': [],
                '周积分': [],
                '月积分': [],
                '联系电话': []
            }
            
            for username, user_info in st.session_state.users_data.items():
                if user_info.get('role') == '学生':
                    student_data['学号'].append(username)
                    student_data['姓名'].append(user_info.get('name', ''))
                    # 从多个字段读取性别信息
                    gender = user_info.get('性别', user_info.get('gender', ''))
                    student_data['性别'].append(gender if gender else '未提供')
                    # 从多个字段读取学院信息
                    college = user_info.get('学院', user_info.get('college', ''))
                    student_data['学院'].append(college if college else '未分配')
                    # 从多个字段读取年级信息
                    grade = user_info.get('年级', user_info.get('grade', ''))
                    student_data['年级'].append(grade if grade else '未分配')
                    # 从多个字段读取专业信息
                    major = user_info.get('专业', user_info.get('major', ''))
                    student_data['专业'].append(major if major else '未分配')
                    # 尝试从用户数据中读取班级信息
                    class_name = user_info.get('class_name', user_info.get('class', ''))
                    # 如果用户数据中没有班级信息，尝试从积分数据中读取
                    if not class_name:
                        score_info = st.session_state.scores_data.get(username, {})
                        class_name = score_info.get('class', '')
                    # 如果仍然没有班级信息，显示未分配班级
                    student_data['班级'].append(class_name if class_name else '未分配班级')
                    student_data['宿舍'].append(user_info.get('dormitory', '未分配宿舍'))
                    # 从多个字段读取辅导员信息
                    counselor = user_info.get('辅导员', user_info.get('counselor', ''))
                    student_data['辅导员'].append(counselor if counselor else '未分配')
                    # 获取积分数据
                    score_info = st.session_state.scores_data.get(username, {})
                    student_data['周积分'].append(score_info.get('weekly_score', 0))
                    student_data['月积分'].append(score_info.get('monthly_score', 0))
                    student_data['联系电话'].append(user_info.get('phone', '未提供'))
            
            df_student = pd.DataFrame(student_data)
            st.dataframe(df_student, use_container_width=True, hide_index=True)
            
            # 导出为CSV
            csv = df_student.to_csv(index=False)
            st.download_button(
                label="导出学生信息",
                data=csv,
                file_name="学生信息.csv",
                mime="text/csv"
            )
            
            # 导出为Excel
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output) as writer:
                df_student.to_excel(writer, index=False, sheet_name='学生信息')
            output.seek(0)
            st.download_button(
                label="导出学生信息 (Excel)",
                data=output,
                file_name="学生信息.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        elif export_type == "辅导员信息":
            # 使用真实的辅导员数据
            teacher_data = {
                '工号': [],
                '姓名': [],
                '性别': [],
                '管理学院': [],
                '管理班级': [],
                '办公室': [],
                '联系电话': []
            }
            
            for username, user_info in st.session_state.users_data.items():
                if user_info.get('role') == '辅导员' or user_info.get('role') == '老师':
                    teacher_data['工号'].append(username)
                    teacher_data['姓名'].append(user_info.get('name', ''))
                    # 从多个字段读取性别信息
                    gender = user_info.get('性别', user_info.get('gender', ''))
                    teacher_data['性别'].append(gender if gender else '未提供')
                    # 从多个字段读取管理学院信息
                    college = user_info.get('管理学院', user_info.get('学院', user_info.get('college', '')))
                    teacher_data['管理学院'].append(college if college else '未分配')
                    # 从多个字段读取管理班级信息
                    classes = user_info.get('class_info', user_info.get('classes', ''))
                    teacher_data['管理班级'].append(classes if classes else '无')
                    # 从多个字段读取办公区域信息
                    office = user_info.get('办公区域', user_info.get('office', ''))
                    teacher_data['办公室'].append(office if office else '未分配')
                    # 从多个字段读取联系电话
                    phone = user_info.get('联系电话', user_info.get('phone', ''))
                    teacher_data['联系电话'].append(phone if phone else '未提供')
            
            df_teacher = pd.DataFrame(teacher_data)
            st.dataframe(df_teacher, use_container_width=True, hide_index=True)
            
            # 导出为CSV
            csv = df_teacher.to_csv(index=False)
            st.download_button(
                label="导出辅导员信息",
                data=csv,
                file_name="辅导员信息.csv",
                mime="text/csv"
            )
            
            # 导出为Excel
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_teacher.to_excel(writer, index=False, sheet_name='辅导员信息')
            output.seek(0)
            st.download_button(
                label="导出辅导员信息 (Excel)",
                data=output,
                file_name="辅导员信息.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        elif export_type == "能耗数据":
            # 使用真实的能耗数据
            if 'energy_data' in st.session_state and st.session_state.energy_data:
                # 从session_state获取真实能耗数据
                energy_data = {
                    '日期': [],
                    '区域': [],
                    '水耗 (吨)': [],
                    '电耗 (kWh)': [],
                    '节能率 (%)': []
                }
                
                for record in st.session_state.energy_data:
                    energy_data['日期'].append(record.get('日期', ''))
                    energy_data['区域'].append(record.get('区域', ''))
                    energy_data['水耗 (吨)'].append(record.get('水耗 (吨)', 0))
                    energy_data['电耗 (kWh)'].append(record.get('电耗 (kWh)', 0))
                    energy_data['节能率 (%)'].append(record.get('节能率 (%)', 0))
                
                df_energy = pd.DataFrame(energy_data)
            else:
                # 模拟能耗数据（当没有真实数据时）
                energy_data = {
                    '日期': ['2024-01-10', '2024-01-11', '2024-01-12', '2024-01-13', '2024-01-14', '2024-01-15'],
                    '区域': ['宿舍', '教学楼', '行政楼', '食堂', '快递站', '保安室'],
                    '水耗 (吨)': [45.2, 35.8, 12.5, 25.6, 3.2, 2.1],
                    '电耗 (kWh)': [4200, 3950, 1080, 3100, 450, 320],
                    '节能率 (%)': [15, 12, 8, 10, 5, 3]
                }
                df_energy = pd.DataFrame(energy_data)
            
            st.dataframe(df_energy, use_container_width=True, hide_index=True)
            
            # 导出为CSV
            csv = df_energy.to_csv(index=False)
            st.download_button(
                label="导出能耗数据",
                data=csv,
                file_name="能耗数据.csv",
                mime="text/csv"
            )
            
            # 导出为Excel
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output) as writer:
                df_energy.to_excel(writer, index=False, sheet_name='能耗数据')
            output.seek(0)
            st.download_button(
                label="导出能耗数据 (Excel)",
                data=output,
                file_name="能耗数据.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        elif export_type == "节能打卡记录":
            # 使用真实的节能打卡记录
            checkin_data = {
                '日期': [],
                '学生姓名': [],
                '学号': [],
                '宿舍': [],
                '打卡类型': [],
                '积分变动': []
            }
            
            # 从checkin_records.json文件中读取节能打卡记录
            try:
                if os.path.exists('checkin_records.json'):
                    with open('checkin_records.json', 'r', encoding='utf-8') as f:
                        checkin_records = json.load(f)
                    for record in checkin_records:
                        checkin_data['日期'].append(record.get('date', ''))
                        checkin_data['学生姓名'].append(record.get('name', ''))
                        checkin_data['学号'].append(record.get('username', ''))
                        checkin_data['宿舍'].append(record.get('dormitory', ''))
                        checkin_data['打卡类型'].append(record.get('action', ''))
                        checkin_data['积分变动'].append(f"+{record.get('points', 0)}")
            except Exception as e:
                st.warning(f"加载打卡记录失败: {str(e)}")
            
            df_checkin = pd.DataFrame(checkin_data)
            st.dataframe(df_checkin, use_container_width=True, hide_index=True)
            
            # 导出为CSV
            csv = df_checkin.to_csv(index=False)
            st.download_button(
                label="导出节能打卡记录",
                data=csv,
                file_name="节能打卡记录.csv",
                mime="text/csv"
            )
            
            # 导出为Excel
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output) as writer:
                df_checkin.to_excel(writer, index=False, sheet_name='节能打卡记录')
            output.seek(0)
            st.download_button(
                label="导出节能打卡记录 (Excel)",
                data=output,
                file_name="节能打卡记录.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        elif export_type == "积分表":
            # 使用真实的积分数据
            score_data = {
                '学号': [],
                '姓名': [],
                '班级': [],
                '周积分': [],
                '月积分': []
            }
            
            for username, score_info in st.session_state.scores_data.items():
                score_data['学号'].append(username)
                score_data['姓名'].append(score_info.get('name', ''))
                score_data['班级'].append(score_info.get('class', '未分配班级'))
                score_data['周积分'].append(score_info.get('weekly_score', 0))
                score_data['月积分'].append(score_info.get('monthly_score', 0))
            
            df_score = pd.DataFrame(score_data)
            st.dataframe(df_score, use_container_width=True, hide_index=True)
            
            # 导出为CSV
            csv = df_score.to_csv(index=False)
            st.download_button(
                label="导出积分表",
                data=csv,
                file_name="积分表.csv",
                mime="text/csv"
            )
            
            # 导出为Excel
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output) as writer:
                df_score.to_excel(writer, index=False, sheet_name='积分表')
            output.seek(0)
            st.download_button(
                label="导出积分表 (Excel)",
                data=output,
                file_name="积分表.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        st.markdown("---")
        
        # 数据模板下载
        st.subheader("📋 数据模板下载")
        
        template_type = st.selectbox("选择模板类型", ["学生信息模板", "教师信息模板", "能耗数据模板"])
        
        if template_type == "学生信息模板":
            # 创建学生信息模板
            template_data = {
                '学号': ['20230101', '20230102'],
                '姓名': ['张三', '李四'],
                '班级': ['23级财务管理01班', '23级财务管理02班'],
                '宿舍': ['1号楼101', '2号楼201'],
                '积分': [850, 780],
                '联系电话': ['13800138001', '13800138002']
            }
            df_template = pd.DataFrame(template_data)
            
            # 导出为Excel模板
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output) as writer:
                df_template.to_excel(writer, index=False, sheet_name='学生信息模板')
            output.seek(0)
            st.download_button(
                label="下载学生信息模板",
                data=output,
                file_name="学生信息模板.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        elif template_type == "教师信息模板":
            # 创建教师信息模板
            template_data = {
                '工号': ['T001', 'T002'],
                '姓名': ['王老师', '邓老师'],
                '职务': ['辅导员', '教师'],
                '管理班级': ['23级财务管理01班,23级财务管理02班', '22级会计01班'],
                '办公室': ['行政楼302', '教学楼A301'],
                '联系电话': ['13900139001', '13900139002']
            }
            df_template = pd.DataFrame(template_data)
            
            # 导出为Excel模板
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output) as writer:
                df_template.to_excel(writer, index=False, sheet_name='教师信息模板')
            output.seek(0)
            st.download_button(
                label="下载教师信息模板",
                data=output,
                file_name="教师信息模板.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        elif template_type == "能耗数据模板":
            # 创建能耗数据模板
            template_data = {
                '日期': ['2024-01-10', '2024-01-11'],
                '区域': ['宿舍', '教学楼'],
                '水耗 (吨)': [45.2, 35.8],
                '电耗 (kWh)': [4200, 3950],
                '节能率 (%)': [15, 12]
            }
            df_template = pd.DataFrame(template_data)
            
            # 导出为Excel模板
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output) as writer:
                df_template.to_excel(writer, index=False, sheet_name='能耗数据模板')
            output.seek(0)
            st.download_button(
                label="下载能耗数据模板",
                data=output,
                file_name="能耗数据模板.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    elif st.session_state.admin_selected_page == "数据清除":
        st.header("🗑️ 数据清除中心")
        
        st.markdown("""
        数据清除功能，支持选择性清除系统中的各类数据。请谨慎操作！
        """)
        
        st.markdown("---")
        
        # 统计当前数据
        student_count = sum(1 for user_info in st.session_state.users_data.values() if user_info.get('role') == '学生')
        counselor_count = sum(1 for user_info in st.session_state.users_data.values() if user_info.get('role') in ['辅导员', '老师'])
        score_count = len(st.session_state.scores_data)
        energy_count = len(st.session_state.energy_data) if 'energy_data' in st.session_state else 0
        
        # 显示当前数据统计
        st.subheader("📊 当前数据统计")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("学生账户", student_count)
        with col2:
            st.metric("辅导员账户", counselor_count)
        with col3:
            st.metric("积分数据", score_count)
        with col4:
            st.metric("能耗数据", energy_count)
        
        st.markdown("---")
        
        st.subheader("⚠️ 数据清除操作")
        
        # 选择要清除的数据类型
        clear_type = st.multiselect(
            "选择要清除的数据类型",
            ["学生信息", "辅导员信息", "积分数据", "能耗数据", "打卡记录"],
            help="可以同时选择多个数据类型进行清除"
        )
        
        # 确认清除
        if clear_type:
            st.warning("⚠️ 数据清除后无法恢复，请谨慎操作！")
            
            # 二次确认
            confirm_clear = st.checkbox("我确认要清除选中的数据，清除后无法恢复")
            
            if confirm_clear:
                if st.button("🚨 执行清除", type="primary", use_container_width=True):
                    # 开始清除数据
                    with st.spinner("正在清除数据..."):
                        cleared_count = 0
                        
                        if "学生信息" in clear_type:
                            # 清除学生信息
                            new_users_data = {}
                            for username, user_info in st.session_state.users_data.items():
                                if user_info.get('role') != '学生':
                                    new_users_data[username] = user_info
                            st.session_state.users_data = new_users_data
                            
                            # 同时清除学生的积分数据
                            new_scores_data = {}
                            for username, score_info in st.session_state.scores_data.items():
                                if username in st.session_state.users_data:
                                    new_scores_data[username] = score_info
                            st.session_state.scores_data = new_scores_data
                            cleared_count += 1
                        
                        if "辅导员信息" in clear_type:
                            # 清除辅导员信息
                            new_users_data = {}
                            for username, user_info in st.session_state.users_data.items():
                                if user_info.get('role') not in ['辅导员', '老师']:
                                    new_users_data[username] = user_info
                            st.session_state.users_data = new_users_data
                            cleared_count += 1
                        
                        if "积分数据" in clear_type:
                            # 清除积分数据
                            st.session_state.scores_data = {}
                            cleared_count += 1
                        
                        if "能耗数据" in clear_type:
                            # 清除能耗数据
                            st.session_state.energy_data = []
                            cleared_count += 1
                        
                        if "打卡记录" in clear_type:
                            # 清除打卡记录
                            import os
                            checkin_file = 'checkin_records.json'
                            if os.path.exists(checkin_file):
                                os.remove(checkin_file)
                            cleared_count += 1
                        
                        # 保存数据
                        save_users_data(st.session_state.users_data)
                        save_scores_data(st.session_state.scores_data)
                        
                        # 清除成功
                        st.success(f"✅ 数据清除成功！已清除 {cleared_count} 类数据。")
                        st.balloons()
                        
                        # 刷新页面
                        import time
                        time.sleep(1)
                        st.rerun()
        
        st.markdown("---")
        
        st.subheader("💥 一键全部清除")
        
        st.error("⚠️ 警告：此操作将清除所有数据，仅保留管理员账户！")
        
        clear_all_confirm = st.checkbox("我确认要清除所有数据，此操作无法恢复")
        
        if clear_all_confirm:
            if st.button("🧨 一键全部清除", type="primary", use_container_width=True):
                with st.spinner("正在清除所有数据..."):
                    # 使用虚拟数据
                    st.session_state.users_data = {}
                    for username, user_info in VIRTUAL_USERS_DATA.items():
                        # 添加虚拟数据标记
                        user_info_copy = user_info.copy()
                        user_info_copy[VIRTUAL_DATA_FLAG] = True
                        st.session_state.users_data[username] = user_info_copy
                    
                    st.session_state.scores_data = {}
                    for username, score_info in VIRTUAL_SCORES_DATA.items():
                        # 添加虚拟数据标记
                        score_info_copy = score_info.copy()
                        score_info_copy[VIRTUAL_DATA_FLAG] = True
                        st.session_state.scores_data[username] = score_info_copy
                    
                    st.session_state.energy_data = []
                    
                    # 删除打卡记录文件
                    import os
                    checkin_file = 'checkin_records.json'
                    if os.path.exists(checkin_file):
                        os.remove(checkin_file)
                    
                    # 保存数据
                    save_users_data(st.session_state.users_data)
                    save_scores_data(st.session_state.scores_data)
                    
                    st.success("✅ 所有数据已清除！已添加虚拟账户。")
                    st.balloons()
                    
                    import time
                    time.sleep(2)
                    st.rerun()

# 老师页面
def teacher_page():
    # 设置页面标题
    st.set_page_config(
        page_title="教师管理中心",
        page_icon="👨‍🏫",
        layout="wide"
    )
    
    # 侧边栏导航
    with st.sidebar:
        # 教师管理中心标题
        st.title("👨‍🏫 教师管理中心")
        st.markdown(f"### 欢迎回来，{st.session_state.user_name}老师！")
        
        # 搜索框（带内置放大镜）
        with st.form(key='search_form'):
            search_query = st.text_input("搜索功能", placeholder="搜索功能", key="teacher_search")
            search_submitted = st.form_submit_button("搜索")
        
        # 搜索功能实现
        if search_submitted and search_query:
            # 定义二级科目映射
            search_mapping = {
                "首页": "首页",
                "学生管理": "学生管理",
                "能耗管理": "能耗管理",
                "行政楼": "行政楼能耗",
                "行政楼能耗": "行政楼能耗",
                "学生耗电异常申诉": "学生耗电异常申诉",
                "异常申诉": "学生耗电异常申诉",
                "打卡管理": "打卡管理",
                "积分管理": "积分管理",
                "节能建议": "节能建议",
                "清除": "数据清除",
                "数据清除": "数据清除"
            }
            
            # 搜索匹配
            for key, value in search_mapping.items():
                if search_query.lower() in key.lower():
                    st.session_state.teacher_selected_page = value
                    st.rerun()
        
        # 初始化折叠状态
        if 'overview_management_expanded' not in st.session_state:
            st.session_state.overview_management_expanded = True
        if 'student_management_expanded' not in st.session_state:
            st.session_state.student_management_expanded = True
        if 'energy_management_expanded' not in st.session_state:
            st.session_state.energy_management_expanded = True
        if 'checkin_score_expanded' not in st.session_state:
            st.session_state.checkin_score_expanded = True
        
        # 检查是否所有科目都已展开
        all_expanded = st.session_state.overview_management_expanded and st.session_state.student_management_expanded and st.session_state.energy_management_expanded and st.session_state.checkin_score_expanded
        
        # 一键折叠/展开按钮
        if st.button("一键折叠" if all_expanded else "一键展开"):
            new_state = not all_expanded
            st.session_state.overview_management_expanded = new_state
            st.session_state.student_management_expanded = new_state
            st.session_state.energy_management_expanded = new_state
            st.session_state.checkin_score_expanded = new_state
            st.rerun()
        
        # 首页按钮（带图标，直接显示）
        if st.button("🏠 首页", use_container_width=True):
            st.session_state.teacher_selected_page = "首页"
            st.rerun()
        
        # 功能分类 - 学生管理
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            <div style='margin-top: 20px;'>
                <h4 style='margin: 0 0 10px 0; display: flex; align-items: center;'>
                    <span style='color: #52c41a; margin-right: 8px;'>👥</span>
                    学生管理
                </h4>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("▼" if st.session_state.student_management_expanded else "▶", key="student_management_toggle", use_container_width=True):
                st.session_state.student_management_expanded = not st.session_state.student_management_expanded
                st.rerun()
        
        # 学生管理功能
        if st.session_state.student_management_expanded:
            if st.button("学生管理", use_container_width=True):
                st.session_state.teacher_selected_page = "学生管理"
                st.rerun()
        
        # 功能分类 - 能耗管理
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            <div style='margin-top: 20px;'>
                <h4 style='margin: 0 0 10px 0; display: flex; align-items: center;'>
                    <span style='color: #faad14; margin-right: 8px;'>💡</span>
                    能耗管理
                </h4>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("▼" if st.session_state.energy_management_expanded else "▶", key="energy_management_toggle", use_container_width=True):
                st.session_state.energy_management_expanded = not st.session_state.energy_management_expanded
                st.rerun()
        
        # 能耗管理功能
        if st.session_state.energy_management_expanded:
            if st.button("能耗管理", use_container_width=True):
                st.session_state.teacher_selected_page = "能耗管理"
                st.rerun()
            if st.button("行政楼能耗", use_container_width=True):
                st.session_state.teacher_selected_page = "行政楼能耗"
                st.rerun()
            if st.button("学生耗电异常申诉", use_container_width=True):
                st.session_state.teacher_selected_page = "学生耗电异常申诉"
                st.rerun()
        
        # 功能分类 - 打卡与积分
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            <div style='margin-top: 20px;'>
                <h4 style='margin: 0 0 10px 0; display: flex; align-items: center;'>
                    <span style='color: #722ed1; margin-right: 8px;'>✅</span>
                    打卡与积分
                </h4>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("▼" if st.session_state.checkin_score_expanded else "▶", key="checkin_score_toggle", use_container_width=True):
                st.session_state.checkin_score_expanded = not st.session_state.checkin_score_expanded
                st.rerun()
        
        # 打卡与积分功能
        if st.session_state.checkin_score_expanded:
            if st.button("打卡管理", use_container_width=True):
                st.session_state.teacher_selected_page = "打卡管理"
                st.rerun()
            if st.button("积分管理", use_container_width=True):
                st.session_state.teacher_selected_page = "积分管理"
                st.rerun()
            if st.button("节能建议", use_container_width=True):
                st.session_state.teacher_selected_page = "节能建议"
                st.rerun()
            if st.button("数据清除", use_container_width=True):
                st.session_state.teacher_selected_page = "数据清除"
                st.rerun()
        
        # 登出按钮
        if st.button("登出", type="secondary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_position = None
            st.session_state.username = None
            st.session_state.user_name = None
            st.session_state.teacher_selected_page = None
            st.rerun()
    
    # 初始化选中页面
    if 'teacher_selected_page' not in st.session_state:
        st.session_state.teacher_selected_page = "首页"
    
    # 首页
    if st.session_state.teacher_selected_page == "首页":
        # 辅导员基本信息
        st.subheader("👨‍🏫 基本信息")
        
        # 从用户数据中获取辅导员信息
        username = st.session_state.username
        users_data = st.session_state.users_data
        teacher_info_data = users_data.get(username, {})
        
        # 获取管理班级
        classes_str = teacher_info_data.get('class_info', teacher_info_data.get('classes', ''))
        teacher_classes = []
        if classes_str:
            teacher_classes = [c.strip() for c in classes_str.split(',') if c.strip()]
        
        # 如果没有班级数据，使用默认值
        if not teacher_classes:
            teacher_classes = ['暂未分配班级']
        
        # 统计管理班级的学生数量
        total_students = 0
        scores_data = st.session_state.scores_data
        # 记录已经统计过的学生ID，避免重复统计
        counted_user_ids = set()
        
        # 显示老师管理的班级
        st.markdown(f"### 管理班级: {', '.join(teacher_classes)}")
        
        # 遍历用户数据中的所有学生
        for user_id, user_data in users_data.items():
            if user_data.get('role') == '学生':
                # 直接通过学生的counselor字段来确定学生是否属于该老师
                student_counselor = user_data.get('counselor', '')
                if st.session_state.user_name in student_counselor:
                    total_students += 1
                    counted_user_ids.add(user_id)
                else:
                    # 尝试通过班级匹配来确定学生是否属于该老师
                    user_class = user_data.get('class_name', '')
                    if user_class:
                        # 检查学生班级是否在老师管理的班级中
                        in_teacher_classes = False
                        for teacher_class in teacher_classes:
                            if teacher_class in user_class or user_class in teacher_class:
                                in_teacher_classes = True
                                break
                        if not in_teacher_classes:
                            # 尝试更宽松的匹配方式
                            for teacher_class in teacher_classes:
                                teacher_class_key = ''.join(filter(str.isalnum, teacher_class))
                                user_class_key = ''.join(filter(str.isalnum, user_class))
                                if teacher_class_key in user_class_key or user_class_key in teacher_class_key:
                                    in_teacher_classes = True
                                    break
                        if in_teacher_classes:
                            total_students += 1
                            counted_user_ids.add(user_id)
        
        # 遍历分数数据中的所有学生
        for user_id, score_data in scores_data.items():
            if user_id not in counted_user_ids:
                # 检查分数数据中是否有辅导员信息
                score_counselor = score_data.get('counselor', '')
                if st.session_state.user_name in score_counselor:
                    total_students += 1
                    counted_user_ids.add(user_id)
                else:
                    # 尝试通过班级匹配来确定学生是否属于该老师
                    student_class = score_data.get('class', '')
                    if student_class:
                        # 检查学生班级是否在老师管理的班级中
                        in_teacher_classes = False
                        for teacher_class in teacher_classes:
                            if teacher_class in student_class or student_class in teacher_class:
                                in_teacher_classes = True
                                break
                        if not in_teacher_classes:
                            # 尝试更宽松的匹配方式
                            for teacher_class in teacher_classes:
                                teacher_class_key = ''.join(filter(str.isalnum, teacher_class))
                                student_class_key = ''.join(filter(str.isalnum, student_class))
                                if teacher_class_key in student_class_key or student_class_key in teacher_class_key:
                                    in_teacher_classes = True
                                    break
                        if in_teacher_classes:
                            total_students += 1
                            counted_user_ids.add(user_id)
        
        # 显示总学生数
        st.markdown(f"### 总学生数: {total_students}")
        
        # 获取办公室地点
        office_location = teacher_info_data.get('office', teacher_info_data.get('办公室', '未分配'))
        
        teacher_info = {
            '姓名': st.session_state.user_name,
            '职务': teacher_info_data.get('role', '辅导员'),
            '管理班级': '、'.join(teacher_classes),
            '办公室地点': office_location
        }
        
        st.markdown(f"""
        <div style='background-color: #f0f8ff; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 20px;'>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;'>
                <div>
                    <h5 style='margin: 0 0 8px 0; color: #666;'>姓名</h5>
                    <p style='margin: 0; font-size: 16px; font-weight: bold; color: #1a1a1a;'>{teacher_info['姓名']}</p>
                </div>
                <div>
                    <h5 style='margin: 0 0 8px 0; color: #666;'>职务</h5>
                    <p style='margin: 0; font-size: 16px; font-weight: bold; color: #1a1a1a;'>{teacher_info['职务']}</p>
                </div>
                <div>
                    <h5 style='margin: 0 0 8px 0; color: #666;'>管理班级</h5>
                    <p style='margin: 0; font-size: 16px; font-weight: bold; color: #1a1a1a;'>{teacher_info['管理班级']}</p>
                </div>
                <div>
                    <h5 style='margin: 0 0 8px 0; color: #666;'>办公室地点</h5>
                    <p style='margin: 0; font-size: 16px; font-weight: bold; color: #1a1a1a;'>{teacher_info['办公室地点']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 顶部数据概览
        st.subheader("📊 数据概览")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style='background-color: #e8f5e8; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1); height: 120px; display: flex; flex-direction: column; justify-content: center;'>
                <h4 style='margin: 0 0 8px 0; color: #2e7d32;'>总学生数</h4>
                <p style='margin: 0; font-size: 24px; font-weight: bold;'>{total_students}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background-color: #e3f2fd; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1); height: 120px; display: flex; flex-direction: column; justify-content: center;'>
                <h4 style='margin: 0 0 8px 0; color: #1565c0;'>日常打卡率</h4>
                <p style='margin: 0; font-size: 24px; font-weight: bold;'>85%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style='background-color: #e8f5e8; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1); height: 120px; display: flex; flex-direction: column; justify-content: center;'>
                <h4 style='margin: 0 0 8px 0; color: #2e7d32;'>节能打卡率</h4>
                <p style='margin: 0; font-size: 24px; font-weight: bold;'>78%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style='background-color: #ffebee; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1); height: 120px; display: flex; flex-direction: column; justify-content: center;'>
                <h4 style='margin: 0 0 8px 0; color: #c62828;'>本周异常申请审批数</h4>
                <p style='margin: 0; font-size: 24px; font-weight: bold;'>15</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 能耗趋势图表和打卡统计
        st.subheader("📈 数据趋势")
        col1, col2 = st.columns(2)
        
        # 左侧：管理班级总能耗趋势图
        with col1:
            st.markdown("### 管理班级总能耗趋势")
            # 日期筛选
            selected_dates = st.date_input("选择日期范围", value=(pd.to_datetime("2024-01-10"), pd.to_datetime("2024-01-31")), key="energy_date_range")
            
            if len(selected_dates) == 2:
                energy_start_date, energy_end_date = selected_dates
                date_range = pd.date_range(start=energy_start_date, end=energy_end_date)
                date_length = len(date_range)
            else:
                # 默认日期范围
                energy_start_date = pd.to_datetime("2024-01-10")
                energy_end_date = pd.to_datetime("2024-01-31")
                date_range = pd.date_range(start=energy_start_date, end=energy_end_date)
                date_length = len(date_range)
            
            # 生成对应长度的数据
            base_electricity = 5.2
            base_water = 1.2
            electricity_data = []
            water_data = []
            
            for i in range(date_length):
                # 电量逐渐减少
                electricity = max(1.0, base_electricity - i * 0.15)
                electricity_data.append(round(electricity, 1))
                # 水量逐渐减少
                water = max(0.1, base_water - i * 0.05)
                water_data.append(round(water, 1))
            
            energy_data = {
                '日期': [d.strftime('%m月%d日') for d in date_range],
                '电量 (kWh)': electricity_data,
                '水量 (吨)': water_data
            }
            df_energy = pd.DataFrame(energy_data)
            
            fig_energy = go.Figure()
            fig_energy.add_trace(go.Scatter(x=df_energy['日期'], y=df_energy['电量 (kWh)'], mode='lines+markers', name='电量'))
            fig_energy.add_trace(go.Scatter(x=df_energy['日期'], y=df_energy['水量 (吨)'], mode='lines+markers', name='水量'))
            fig_energy.update_layout(
                title=f"管理班级总能耗趋势 ({energy_start_date.strftime('%Y-%m-%d')} 至 {energy_end_date.strftime('%Y-%m-%d')})",
                xaxis_title="日期",
                yaxis_title="消耗量",
                height=400,
                hovermode='x unified'
            )
            st.plotly_chart(fig_energy, use_container_width=True)
        
        # 右侧：班级打卡量柱状图（带日期筛选）
        with col2:
            # 日期筛选
            st.markdown("### 班级打卡量")
            date_option = st.selectbox("选择日期范围", ["今日", "本周", "本月", "自定义日期"], key="class_checkin_date_selectbox")
            
            if date_option == "自定义日期":
                start_date = st.date_input("开始日期", value=pd.to_datetime("2024-01-10"), key="checkin_start_date")
                end_date = st.date_input("结束日期", value=pd.to_datetime("2024-01-16"), key="checkin_end_date")
            elif date_option == "今日":
                start_date = pd.to_datetime("2024-01-16")  # 今日
                end_date = pd.to_datetime("2024-01-16")  # 今日
            elif date_option == "本周":
                start_date = pd.to_datetime("2024-01-10")  # 本周开始（2024-01-10是周三，假设周一为一周开始）
                end_date = pd.to_datetime("2024-01-16")  # 本周结束
            elif date_option == "本月":
                start_date = pd.to_datetime("2024-01-01")  # 本月开始
                end_date = pd.to_datetime("2024-01-31")  # 本月结束
            
            # 模拟班级打卡数据
            class_data = {
                '班级': ['23级财务管理01班', '23级财务管理02班', '23级会计01班', '23级会计02班', '23级审计01班'],
                '打卡量': [45, 38, 42, 35, 30]
            }
            df_class_checkin = pd.DataFrame(class_data)
            
            fig_checkin = go.Figure()
            fig_checkin.add_trace(go.Bar(x=df_class_checkin['班级'], y=df_class_checkin['打卡量'], name='打卡量'))
            fig_checkin.update_layout(
                title=f"班级打卡量 ({start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')})",
                xaxis_title="班级",
                yaxis_title="打卡数量",
                height=400,
                hovermode='y unified'
            )
            st.plotly_chart(fig_checkin, use_container_width=True)
    
    # 学生管理
    elif st.session_state.teacher_selected_page == "学生管理":
        st.subheader("👥 学生管理")
        
        # 从用户数据中获取教师信息
        username = st.session_state.username
        users_data = st.session_state.users_data
        scores_data = st.session_state.scores_data
        teacher_info_data = users_data.get(username, {})
        
        # 显示教师信息（调试用）
        st.markdown(f"### 教师信息: {st.session_state.user_name}")
        st.markdown(f"用户名: {username}")
        
        # 获取管理班级
        classes_str = teacher_info_data.get('class_info', teacher_info_data.get('classes', ''))
        teacher_classes = []
        if classes_str:
            teacher_classes = [c.strip() for c in classes_str.split(',') if c.strip()]
        
        # 如果没有班级数据，使用默认值
        if not teacher_classes:
            teacher_classes = ['暂未分配班级']
        
        # 显示管理班级
        st.markdown(f"### 管理班级: {', '.join(teacher_classes)}")
        
        # 添加调试信息：统计所有辅导员和班级
        with st.expander("📊 查看系统中的所有辅导员和班级信息（调试用）"):
            # 统计users_data中的辅导员和班级
            counselor_set = set()
            class_set = set()
            student_count_by_counselor = {}
            student_count_by_class = {}
            
            for user_id, user_data in users_data.items():
                if user_data.get('role') == '学生':
                    counselor = user_data.get('counselor', '未知辅导员')
                    class_name = user_data.get('class_name', '未知班级')
                    counselor_set.add(counselor)
                    class_set.add(class_name)
                    
                    # 统计每个辅导员的学生数
                    if counselor not in student_count_by_counselor:
                        student_count_by_counselor[counselor] = 0
                    student_count_by_counselor[counselor] += 1
                    
                    # 统计每个班级的学生数
                    if class_name not in student_count_by_class:
                        student_count_by_class[class_name] = 0
                    student_count_by_class[class_name] += 1
            
            # 统计scores_data中的辅导员和班级
            for user_id, score_data in scores_data.items():
                counselor = score_data.get('counselor', '未知辅导员')
                class_name = score_data.get('class', '未知班级')
                counselor_set.add(counselor)
                class_set.add(class_name)
                
                # 统计每个辅导员的学生数
                if counselor not in student_count_by_counselor:
                    student_count_by_counselor[counselor] = 0
                student_count_by_counselor[counselor] += 1
                
                # 统计每个班级的学生数
                if class_name not in student_count_by_class:
                    student_count_by_class[class_name] = 0
                student_count_by_class[class_name] += 1
            
            # 显示辅导员列表
            st.markdown("#### 系统中的所有辅导员:")
            for counselor in sorted(counselor_set):
                count = student_count_by_counselor.get(counselor, 0)
                st.markdown(f"- {counselor}: {count} 名学生")
            
            # 显示班级列表
            st.markdown("#### 系统中的所有班级:")
            for class_name in sorted(class_set):
                count = student_count_by_class.get(class_name, 0)
                st.markdown(f"- {class_name}: {count} 名学生")
        
        # 班级查询栏
        selected_classes = st.multiselect("选择班级", teacher_classes, default=teacher_classes)
        
        # 收集所有学生数据
        student_list = []
        # 统计处理的学生数量
        processed_students = 0
        # 统计匹配的学生数量
        matched_students = 0
        # 记录已经处理过的学生ID，避免重复处理
        processed_user_ids = set()
        # 用于调试：记录匹配详情
        match_details = []
        
        # 遍历用户数据中的所有学生
        for user_id, user_data in users_data.items():
            if user_data.get('role') == '学生':
                processed_students += 1
                processed_user_ids.add(user_id)
                # 直接通过学生的counselor字段来确定学生是否属于该老师
                student_counselor = user_data.get('counselor', '')
                # 从scores_data中读取学生的班级信息，与学生端保持一致
                student_class = scores_data.get(user_id, {}).get('class', '')
                # 从user_data中获取班级信息（如果scores_data中没有）
                display_class = student_class or user_data.get('class_name', '')
                
                # 检查学生是否属于该老师
                is_teacher_student = False
                match_method = '未匹配'
                
                # 方式1：通过辅导员字段匹配
                if st.session_state.user_name in student_counselor:
                    is_teacher_student = True
                    match_method = '辅导员匹配'
                # 方式2：通过班级匹配
                elif display_class:
                    # 检查学生班级是否在老师管理的班级中
                    in_teacher_classes = False
                    for teacher_class in teacher_classes:
                        # 严格匹配
                        if teacher_class in display_class or display_class in teacher_class:
                            in_teacher_classes = True
                            break
                    if not in_teacher_classes:
                        # 尝试更宽松的匹配方式
                        for teacher_class in teacher_classes:
                            # 提取班级名称中的关键信息进行匹配
                            teacher_class_key = ''.join(filter(str.isalnum, teacher_class))
                            display_class_key = ''.join(filter(str.isalnum, display_class))
                            if teacher_class_key in display_class_key or display_class_key in teacher_class_key:
                                in_teacher_classes = True
                                break
                    if in_teacher_classes:
                        is_teacher_student = True
                        match_method = '班级匹配'
                
                # 如果是该老师的学生
                if is_teacher_student:
                    # 根据选择的班级筛选
                    if selected_classes:
                        class_match_found = False
                        # 如果是通过辅导员匹配的，直接通过班级筛选
                        if match_method == '辅导员匹配':
                            class_match_found = True
                        else:
                            # 否则进行班级匹配
                            for selected_class in selected_classes:
                                # 严格匹配
                                if selected_class in display_class or display_class in selected_class:
                                    class_match_found = True
                                    break
                            if not class_match_found:
                                # 尝试更宽松的匹配方式
                                for selected_class in selected_classes:
                                    # 提取班级名称中的关键信息进行匹配
                                    selected_class_key = ''.join(filter(str.isalnum, selected_class))
                                    display_class_key = ''.join(filter(str.isalnum, display_class))
                                    if selected_class_key in display_class_key or display_class_key in selected_class_key:
                                        class_match_found = True
                                        break
                        if not class_match_found:
                            # 记录未通过班级筛选的学生
                            match_details.append({
                                '学号': user_id,
                                '姓名': user_data.get('name', ''),
                                '辅导员': student_counselor,
                                '班级': display_class,
                                '匹配方式': match_method,
                                '结果': '未通过班级筛选'
                            })
                            continue
                    
                    matched_students += 1
                    # 获取积分数据
                    score_info = scores_data.get(user_id, {})
                    monthly_score = score_info.get('monthly_score', 0)
                    weekly_score = score_info.get('weekly_score', 0)
                    
                    # 获取学生详细信息
                    student_name = user_data.get('name', '')
                    student_dormitory = user_data.get('dormitory', '未分配')
                    student_phone = user_data.get('phone', '未提供')
                    student_gender = user_data.get('gender', '未知')
                    student_college = user_data.get('college', '未提供')
                    student_grade = user_data.get('grade', '未提供')
                    student_major = user_data.get('major', '未提供')
                    
                    student_list.append({
                        '学号': user_id,
                        '姓名': student_name,
                        '班级': display_class,
                        '宿舍': student_dormitory,
                        '性别': student_gender,
                        '学院': student_college,
                        '年级': student_grade,
                        '专业': student_major,
                        '周积分': weekly_score,
                        '月积分': monthly_score,
                        '联系电话': student_phone
                    })
                    
                    # 记录匹配成功的学生
                    match_details.append({
                        '学号': user_id,
                        '姓名': student_name,
                        '辅导员': student_counselor,
                        '班级': display_class,
                        '匹配方式': match_method,
                        '结果': '匹配成功'
                    })
                else:
                    # 记录未匹配的学生
                    match_details.append({
                        '学号': user_id,
                        '姓名': user_data.get('name', ''),
                        '辅导员': student_counselor,
                        '班级': display_class,
                        '匹配方式': '未匹配',
                        '结果': '未匹配'
                    })
        
        # 遍历分数数据中的所有学生，处理用户数据中没有的学生
        for user_id, score_data in scores_data.items():
            if user_id not in processed_user_ids:
                processed_students += 1
                processed_user_ids.add(user_id)
                # 检查分数数据中是否有辅导员信息
                score_counselor = score_data.get('counselor', '')
                # 从分数数据中获取班级信息
                display_class = score_data.get('class', '')
                
                # 检查学生是否属于该老师
                is_teacher_student = False
                match_method = '未匹配'
                
                # 方式1：通过辅导员字段匹配
                if st.session_state.user_name in score_counselor:
                    is_teacher_student = True
                    match_method = '辅导员匹配'
                # 方式2：通过班级匹配
                elif display_class:
                    # 检查学生班级是否在老师管理的班级中
                    in_teacher_classes = False
                    for teacher_class in teacher_classes:
                        # 严格匹配
                        if teacher_class in display_class or display_class in teacher_class:
                            in_teacher_classes = True
                            break
                    if not in_teacher_classes:
                        # 尝试更宽松的匹配方式
                        for teacher_class in teacher_classes:
                            # 提取班级名称中的关键信息进行匹配
                            teacher_class_key = ''.join(filter(str.isalnum, teacher_class))
                            display_class_key = ''.join(filter(str.isalnum, display_class))
                            if teacher_class_key in display_class_key or display_class_key in teacher_class_key:
                                in_teacher_classes = True
                                break
                    if in_teacher_classes:
                        is_teacher_student = True
                        match_method = '班级匹配'
                
                # 如果是该老师的学生
                if is_teacher_student:
                    # 根据选择的班级筛选
                    if selected_classes:
                        class_match_found = False
                        # 如果是通过辅导员匹配的，直接通过班级筛选
                        if match_method == '辅导员匹配':
                            class_match_found = True
                        else:
                            # 否则进行班级匹配
                            for selected_class in selected_classes:
                                # 严格匹配
                                if selected_class in display_class or display_class in selected_class:
                                    class_match_found = True
                                    break
                            if not class_match_found:
                                # 尝试更宽松的匹配方式
                                for selected_class in selected_classes:
                                    # 提取班级名称中的关键信息进行匹配
                                    selected_class_key = ''.join(filter(str.isalnum, selected_class))
                                    display_class_key = ''.join(filter(str.isalnum, display_class))
                                    if selected_class_key in display_class_key or display_class_key in selected_class_key:
                                        class_match_found = True
                                        break
                        if not class_match_found:
                            # 记录未通过班级筛选的学生
                            match_details.append({
                                '学号': user_id,
                                '姓名': score_data.get('name', ''),
                                '辅导员': score_counselor,
                                '班级': display_class,
                                '匹配方式': match_method,
                                '结果': '未通过班级筛选'
                            })
                            continue
                    
                    matched_students += 1
                    # 获取积分数据
                    monthly_score = score_data.get('monthly_score', 0)
                    weekly_score = score_data.get('weekly_score', 0)
                    
                    # 获取学生详细信息
                    student_name = score_data.get('name', '')
                    student_dormitory = score_data.get('dormitory', '未分配')
                    student_phone = score_data.get('phone', '未提供')
                    student_gender = score_data.get('gender', '未知')
                    student_college = score_data.get('college', '未提供')
                    student_grade = score_data.get('grade', '未提供')
                    student_major = score_data.get('major', '未提供')
                    
                    student_list.append({
                        '学号': user_id,
                        '姓名': student_name,
                        '班级': display_class,
                        '宿舍': student_dormitory,
                        '性别': student_gender,
                        '学院': student_college,
                        '年级': student_grade,
                        '专业': student_major,
                        '周积分': weekly_score,
                        '月积分': monthly_score,
                        '联系电话': student_phone
                    })
                    
                    # 记录匹配成功的学生
                    match_details.append({
                        '学号': user_id,
                        '姓名': student_name,
                        '辅导员': score_counselor,
                        '班级': display_class,
                        '匹配方式': match_method,
                        '结果': '匹配成功'
                    })
                else:
                    # 记录未匹配的学生
                    match_details.append({
                        '学号': user_id,
                        '姓名': score_data.get('name', ''),
                        '辅导员': score_counselor,
                        '班级': display_class,
                        '匹配方式': '未匹配',
                        '结果': '未匹配'
                    })
        
        # 显示处理和匹配的学生数量
        st.markdown(f"### 处理学生数据: 共 {processed_students} 名学生，匹配 {matched_students} 名学生")
        
        # 显示匹配详情（调试用）
        with st.expander("🔍 查看学生匹配详情（调试用）"):
            df_match_details = pd.DataFrame(match_details)
            if not df_match_details.empty:
                st.dataframe(df_match_details, use_container_width=True)
        
        df_students = pd.DataFrame(student_list)
        
        # 排序功能
        if 'sort_order' not in st.session_state:
            st.session_state.sort_order = 'desc'
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### 学生列表 ({len(df_students)}人)")
        with col2:
            if st.button("🔄 切换排序" if st.session_state.sort_order == 'desc' else "🔄 切换排序"):
                st.session_state.sort_order = 'asc' if st.session_state.sort_order == 'desc' else 'desc'
                st.rerun()
        
        if not df_students.empty:
            # 按月积分排序
            df_students = df_students.sort_values('月积分', ascending=(st.session_state.sort_order == 'asc'))
            # 添加排名列
            df_students.insert(0, '排名', range(1, len(df_students) + 1))
            
            # 显示学生列表
            st.dataframe(df_students, use_container_width=True)
            
            # 提供导出功能
            csv = df_students.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 导出学生列表",
                data=csv,
                file_name=f"{st.session_state.user_name}_学生列表.csv",
                mime="text/csv"
            )
        else:
            st.info("暂无学生数据")
    
    # 能耗管理
    elif st.session_state.teacher_selected_page == "能耗管理":
        st.subheader("💡 能耗管理")
        
        # 预警卡片切换
        # 添加自定义CSS样式使按钮更大
        st.markdown("""
        <style>
        .stButton > button {
            height: 50px;
            font-size: 16px;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 高能耗预警", key="high_energy"):
                st.session_state.energy_tab = "high_energy"
                st.rerun()
        
        with col2:
            if st.button("⚡ 违规用电预警", key="violation"):
                st.session_state.energy_tab = "violation"
                st.rerun()
        
        with col3:
            if st.button("🏆 节能标兵", key="energy_saving"):
                st.session_state.energy_tab = "energy_saving"
                st.rerun()
        
        # 初始化tab状态
        if 'energy_tab' not in st.session_state:
            st.session_state.energy_tab = "high_energy"
        
        # 根据选中的tab显示不同数据
        if st.session_state.energy_tab == "high_energy":
            # 高能耗预警数据
            energy_data = {
                '排名': [1, 2, 3, 4, 5],
                '宿舍': ['1号楼102', '2号楼202', '1号楼101', '1号楼103', '3号楼301'],
                '当日能耗 (kWh)': [4.0, 3.8, 3.5, 3.2, 2.8],
                '环比': [5.2, 3.8, 2.1, -1.5, -6.3]
            }
            st.markdown("### 高能耗预警")
        elif st.session_state.energy_tab == "violation":
            # 违规用电预警数据
            energy_data = {
                '排名': [1, 2, 3],
                '宿舍': ['1号楼102', '2号楼202', '3号楼302'],
                '违规类型': ['使用大功率电器', '私拉电线', '长时间待机'],
                '警告次数': [3, 2, 1]
            }
            st.markdown("### 违规用电预警")
        else:
            # 节能标兵数据
            energy_data = {
                '排名': [1, 2, 3, 4, 5],
                '宿舍': ['3号楼301', '1号楼103', '1号楼101', '2号楼202', '1号楼102'],
                '当日能耗 (kWh)': [2.8, 3.2, 3.5, 3.8, 4.0],
                '节能率': [35, 30, 25, 20, 15]
            }
            st.markdown("### 节能标兵")
        
        df_energy = pd.DataFrame(energy_data)
        st.dataframe(df_energy, use_container_width=True)
        
        st.markdown("---")
        
        # 能耗分析图表
        st.markdown("### 能耗分析")
        
        # 三个图表并排显示
        col1, col2, col3 = st.columns(3)
        
        # 楼栋能耗对比柱状图
        with col1:
            st.markdown("#### 楼栋能耗对比")
            building_energy = {
                '楼栋': ['1号楼', '2号楼', '3号楼', '4号楼', '5号楼', '6号楼'],
                '能耗 (kWh)': [30, 40, 45, 50, 35, 25]
            }
            df_building = pd.DataFrame(building_energy)
            
            fig_building = go.Figure()
            fig_building.add_trace(go.Bar(
                x=df_building['楼栋'],
                y=df_building['能耗 (kWh)'],
                marker_color='#1890ff'
            ))
            fig_building.update_layout(
                xaxis_title='楼栋',
                yaxis_title='能耗 (kWh)',
                height=300,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_building, use_container_width=True)
        
        # 班级能耗占比饼图
        with col2:
            st.markdown("#### 班级能耗占比")
            class_energy = {
                '班级': ['23级财务管理01班', '23级财务管理02班', '23级会计01班', '23级会计02班', '23级审计01班'],
                '能耗 (kWh)': [125.5, 118.3, 132.7, 128.9, 115.2]
            }
            df_class = pd.DataFrame(class_energy)
            
            fig_class = go.Figure()
            fig_class.add_trace(go.Pie(
                labels=df_class['班级'],
                values=df_class['能耗 (kWh)'],
                hole=0.3
            ))
            fig_class.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_class, use_container_width=True)
        
        # 宿舍能耗趋势图
        with col3:
            st.markdown("#### 宿舍能耗趋势")
            dates = ['10', '20', '30', '40', '50', '60', '70', '80']
            class_trends = {
                '23级财务管理01班': [100, 200, 300, 350, 400, 380, 360, 350]
            }
            
            fig_trend = go.Figure()
            colors = ['#1890ff']
            
            for i, (class_name, trend) in enumerate(class_trends.items()):
                fig_trend.add_trace(go.Scatter(
                    x=dates,
                    y=trend,
                    name=class_name,
                    line=dict(color=colors[i], width=2)
                ))
            
            fig_trend.update_layout(
                xaxis_title='日期',
                yaxis_title='能耗 (kWh)',
                height=300,
                margin=dict(l=20, r=20, t=20, b=20),
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
            )
            st.plotly_chart(fig_trend, use_container_width=True)
    
    # 打卡管理
    elif st.session_state.teacher_selected_page == "打卡管理":
        st.subheader("✅ 打卡管理")
        
        # 导入必要的模块
        import os
        import json
        
        # 获取当前登录教师信息
        current_teacher = st.session_state.users_data.get(st.session_state.username, {})
        
        # 获取教师管理的班级
        teacher_classes_str = current_teacher.get('class_info', current_teacher.get('classes', ''))
        teacher_classes = []
        if teacher_classes_str:
            # 同时支持中文逗号和英文逗号
            teacher_classes_str = teacher_classes_str.replace('，', ',')
            teacher_classes = [c.strip() for c in teacher_classes_str.split(',') if c.strip()]
        
        # 加载打卡记录
        all_checkin_records = []
        try:
            if os.path.exists('checkin_records.json'):
                with open('checkin_records.json', 'r', encoding='utf-8') as f:
                    all_checkin_records = json.load(f)
        except Exception as e:
            st.warning(f"加载打卡记录失败: {str(e)}")
        
        # 筛选教师管理班级的学生打卡记录
        checkin_records = []
        for record in all_checkin_records:
            record_username = record.get('username', '')
            if record_username in st.session_state.users_data:
                student_data = st.session_state.users_data[record_username]
                # 学生班级字段是 class_name，不是 class
                student_class = student_data.get('class_name', '')
                # 检查学生是否属于教师管理的班级
                class_match = False
                for tc in teacher_classes:
                    # 去除空格和中文逗号，统一格式
                    tc_clean = tc.replace('，', '').replace(' ', '')
                    student_class_clean = student_class.replace('，', '').replace(' ', '')
                    # 检查班级名称是否匹配（忽略年级前缀）
                    if tc_clean in student_class_clean or student_class_clean in tc_clean:
                        class_match = True
                        break
                if class_match:
                    checkin_records.append(record)
        
        # 统计卡片
        st.markdown("### 打卡统计")
        col1, col2, col3 = st.columns(3)
        
        total_checkins = len(checkin_records)
        total_points = sum(record.get('points', 0) for record in checkin_records)
        compliance_rate = "85%"  # 可以根据实际数据计算
        
        with col1:
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
                <h5 style='margin: 0 0 10px 0; color: #1a1a1a;'>总打卡数</h5>
                <p style='margin: 0; font-size: 24px; font-weight: bold; color: #1890ff;'>{total_checkins}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
                <h5 style='margin: 0 0 10px 0; color: #1a1a1a;'>达标率</h5>
                <p style='margin: 0; font-size: 24px; font-weight: bold; color: #52c41a;'>{compliance_rate}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
                <h5 style='margin: 0 0 10px 0; color: #1a1a1a;'>总积分</h5>
                <p style='margin: 0; font-size: 24px; font-weight: bold; color: #faad14;'>{total_points}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 学生打卡明细和详情
        col1, col2 = st.columns(2)
        
        with col1:
            # 学生打卡明细
            st.markdown("### 学生打卡明细")
            
            if checkin_records:
                # 转换为DataFrame
                checkin_data = {
                    '日期': [record.get('date', '') for record in checkin_records],
                    '学生': [record.get('name', '') for record in checkin_records],
                    '宿舍': [record.get('dormitory', '') for record in checkin_records],
                    '行为': [record.get('action', '') for record in checkin_records],
                    '积分': [record.get('points', 0) for record in checkin_records]
                }
                df_checkin_records = pd.DataFrame(checkin_data)
                st.dataframe(df_checkin_records, use_container_width=True)
                
                # 导出功能
                export_format = st.selectbox("导出格式", ["CSV", "Excel"], key="export_format_1")
                if export_format == "CSV":
                    csv = df_checkin_records.to_csv(index=False)
                    st.download_button(
                        label="导出打卡明细",
                        data=csv,
                        file_name="打卡明细.csv",
                        mime="text/csv"
                    )
                else:
                    # 导出为Excel
                    import io
                    output = io.BytesIO()
                    with pd.ExcelWriter(output) as writer:
                        df_checkin_records.to_excel(writer, index=False, sheet_name='打卡明细')
                    output.seek(0)
                    st.download_button(
                        label="导出打卡明细",
                        data=output,
                        file_name="打卡明细.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.info("暂无打卡记录")
        
        with col2:
            # 打卡详情
            st.markdown("### 打卡详情")
            
            if checkin_records:
                # 统计不同打卡类型的次数和积分
                action_stats = {}
                for record in checkin_records:
                    action = record.get('action', '其他')
                    if action not in action_stats:
                        action_stats[action] = {'count': 0, 'points': 0, 'users': set()}
                    action_stats[action]['count'] += 1
                    action_stats[action]['points'] += record.get('points', 0)
                    action_stats[action]['users'].add(record.get('username', ''))
                
                # 转换为DataFrame
                details_data = {
                    '打卡类型': list(action_stats.keys()),
                    '积分奖励': [action_stats[action]['points'] // action_stats[action]['count'] if action_stats[action]['count'] > 0 else 0 for action in action_stats],
                    '参与人数': [len(action_stats[action]['users']) for action in action_stats],
                    '达标要求': ['每日1次' for _ in action_stats]
                }
                df_checkin_details = pd.DataFrame(details_data)
                st.dataframe(df_checkin_details, use_container_width=True)
                
                # 导出功能
                export_format = st.selectbox("导出格式", ["CSV", "Excel"], key="export_format_2")
                if export_format == "CSV":
                    csv = df_checkin_details.to_csv(index=False)
                    st.download_button(
                        label="导出打卡详情",
                        data=csv,
                        file_name="打卡详情.csv",
                        mime="text/csv"
                    )
                else:
                    # 导出为Excel
                    import io
                    output = io.BytesIO()
                    with pd.ExcelWriter(output) as writer:
                        df_checkin_details.to_excel(writer, index=False, sheet_name='打卡详情')
                    output.seek(0)
                    st.download_button(
                        label="导出打卡详情",
                        data=output,
                        file_name="打卡详情.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.info("暂无打卡详情")
        
        # 打卡趋势 - 移到下方并占据整个宽度
        st.markdown("---")
        st.markdown("### 打卡趋势")
        
        # 添加日期范围筛选
        trend_date_range = st.date_input("选择日期范围", value=(pd.to_datetime("2024-01-10"), pd.to_datetime("2024-01-16")), key="trend_date_range")
        
        if len(trend_date_range) == 2:
            start_date, end_date = trend_date_range
            # 生成日期范围
            date_range = pd.date_range(start=start_date, end=end_date)
            dates = [d.strftime('%m月%d日') for d in date_range]
            
            # 生成对应长度的打卡数据
            import random
            checkin_counts = []
            base_count = 12
            for i in range(len(dates)):
                # 模拟打卡数据，有一定波动
                count = base_count + random.randint(-2, 5)
                checkin_counts.append(max(5, count))  # 确保数据不为负数
        else:
            # 默认日期范围
            dates = ['1月10日', '1月11日', '1月12日', '1月13日', '1月14日', '1月15日', '1月16日']
            checkin_counts = [12, 15, 18, 14, 16, 19, 21]
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=dates,
            y=checkin_counts,
            mode='lines+markers',
            line=dict(color='#1890ff', width=2),
            marker=dict(size=6, color='#1890ff')
        ))
        fig_trend.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title="日期",
            yaxis_title="打卡数"
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    # 积分管理
    elif st.session_state.teacher_selected_page == "积分管理":
        st.subheader("🎁 积分管理")
        
        # 积分排行榜
        score_ranking = {
            '排名': [1, 2, 3, 4, 5],
            '姓名': ['王五', '张三', '李四', '赵六', '钱七'],
            '班级': ['23级财务管理02班', '23级财务管理01班', '23级财务管理01班', '23级财务管理02班', '23级财务管理01班'],
            '积分': [920, 850, 780, 650, 720]
        }
        df_score_ranking = pd.DataFrame(score_ranking)
        st.dataframe(df_score_ranking, use_container_width=True)
        
        # 导出功能
        export_format = st.selectbox("导出格式", ["CSV", "Excel"], key="export_format_3")
        if export_format == "CSV":
            csv = df_score_ranking.to_csv(index=False)
            st.download_button(
                label="导出积分排行榜",
                data=csv,
                file_name="积分排行榜.csv",
                mime="text/csv"
            )
        else:
            # 导出为Excel
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output) as writer:
                df_score_ranking.to_excel(writer, index=False, sheet_name='积分排行榜')
            output.seek(0)
            st.download_button(
                label="导出积分排行榜",
                data=output,
                file_name="积分排行榜.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    # 节能建议
    elif st.session_state.teacher_selected_page == "节能建议":
        st.subheader("💡 节能建议管理")
        
        # 节能建议列表
        suggestions = {
            '编号': [1, 2, 3, 4, 5],
            '建议内容': [
                "建议将空调温度设置在26℃，每提高1℃可节约10%的能耗",
                "离开宿舍时记得关闭所有电器，避免待机能耗",
                "使用节能灯具，可减少照明能耗30%以上",
                "合理安排用水时间，避免长流水",
                "建议在非高峰时段使用大功率电器"
            ],
            '提出人': ['张三', '李四', '王五', '赵六', '钱七'],
            '采纳状态': ['已采纳', '已采纳', '已采纳', '审核中', '审核中']
        }
        df_suggestions = pd.DataFrame(suggestions)
        st.dataframe(df_suggestions, use_container_width=True)
        
        # 导出功能
        export_format = st.selectbox("导出格式", ["CSV", "Excel"], key="export_format_4")
        if export_format == "CSV":
            csv = df_suggestions.to_csv(index=False)
            st.download_button(
                label="导出节能建议",
                data=csv,
                file_name="节能建议.csv",
                mime="text/csv"
            )
        else:
            # 导出为Excel
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output) as writer:
                df_suggestions.to_excel(writer, index=False, sheet_name='节能建议')
            output.seek(0)
            st.download_button(
                label="导出节能建议",
                data=output,
                file_name="节能建议.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    # 数据清除
    elif st.session_state.teacher_selected_page == "数据清除":
        st.header("🗑️ 数据清除中心")
        
        st.markdown("""
        数据清除功能，支持选择性清除您所管理班级的各类数据。请谨慎操作！
        """)
        
        st.markdown("---")
        
        # 从用户数据中获取辅导员信息
        username = st.session_state.username
        users_data = st.session_state.users_data
        teacher_info_data = users_data.get(username, {})
        
        # 获取管理班级
        classes_str = teacher_info_data.get('class_info', teacher_info_data.get('classes', ''))
        teacher_classes = []
        if classes_str:
            teacher_classes = [c.strip() for c in classes_str.split(',') if c.strip()]
        
        # 如果没有班级数据，使用默认值
        if not teacher_classes:
            teacher_classes = ['暂未分配班级']
        
        # 统计当前所管理班级的学生数据
        scores_data = st.session_state.scores_data
        processed_user_ids = set()
        student_list = []
        
        # 先从用户数据中查找学生
        for user_id, user_data in users_data.items():
            if user_id in processed_user_ids:
                continue
            if user_data.get('role') == '学生':
                processed_user_ids.add(user_id)
                
                # 检查是否是该老师的学生
                is_teacher_student = False
                
                # 方式1：通过辅导员字段匹配
                student_counselor = user_data.get('counselor', user_data.get('辅导员', ''))
                if st.session_state.user_name in student_counselor:
                    is_teacher_student = True
                
                # 方式2：通过班级匹配
                if not is_teacher_student:
                    display_class = user_data.get('class_name', user_data.get('class', ''))
                    # 从score_data中获取班级信息
                    if not display_class:
                        score_info = scores_data.get(user_id, {})
                        display_class = score_info.get('class', '')
                    
                    if display_class:
                        for teacher_class in teacher_classes:
                            teacher_class_key = ''.join(filter(str.isalnum, teacher_class))
                            display_class_key = ''.join(filter(str.isalnum, display_class))
                            if teacher_class_key in display_class_key or display_class_key in teacher_class_key:
                                is_teacher_student = True
                                break
                
                if is_teacher_student:
                    student_list.append({
                        'user_id': user_id,
                        'name': user_data.get('name', ''),
                        'class': display_class
                    })
        
        # 从分数数据中查找学生
        for user_id, score_data in scores_data.items():
            if user_id in processed_user_ids:
                continue
            
            user_data = users_data.get(user_id, {})
            if not user_data or user_data.get('role') == '学生':
                processed_user_ids.add(user_id)
                
                # 检查是否是该老师的学生
                is_teacher_student = False
                
                # 方式1：通过辅导员字段匹配
                student_counselor = user_data.get('counselor', user_data.get('辅导员', score_data.get('counselor', score_data.get('辅导员', ''))))
                if st.session_state.user_name in student_counselor:
                    is_teacher_student = True
                
                # 方式2：通过班级匹配
                if not is_teacher_student:
                    display_class = user_data.get('class_name', user_data.get('class', score_data.get('class', '')))
                    
                    if display_class:
                        for teacher_class in teacher_classes:
                            teacher_class_key = ''.join(filter(str.isalnum, teacher_class))
                            display_class_key = ''.join(filter(str.isalnum, display_class))
                            if teacher_class_key in display_class_key or display_class_key in teacher_class_key:
                                is_teacher_student = True
                                break
                
                if is_teacher_student:
                    student_list.append({
                        'user_id': user_id,
                        'name': user_data.get('name', score_data.get('name', '')),
                        'class': display_class
                    })
        
        # 统计当前数据
        student_count = len(student_list)
        
        # 显示当前数据统计
        st.subheader("📊 当前数据统计")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("管理班级", len(teacher_classes))
        with col2:
            st.metric("学生数量", student_count)
        
        st.markdown("---")
        
        st.subheader("⚠️ 数据清除操作")
        
        # 选择要清除的数据类型
        clear_type = st.multiselect(
            "选择要清除的数据类型",
            ["学生打卡记录", "学生积分数据"],
            help="可以同时选择多个数据类型进行清除"
        )
        
        # 显示管理的班级
        if student_count > 0:
            st.subheader("🎯 管理的学生列表")
            df_students = pd.DataFrame(student_list)
            df_students.columns = ['学号', '姓名', '班级']
            st.dataframe(df_students, use_container_width=True, hide_index=True)
        
        # 确认清除
        if clear_type:
            st.warning("⚠️ 数据清除后无法恢复，请谨慎操作！")
            
            # 二次确认
            confirm_clear = st.checkbox("我确认要清除选中的数据，清除后无法恢复")
            
            if confirm_clear:
                if st.button("🚨 执行清除", type="primary", use_container_width=True):
                    # 开始清除数据
                    with st.spinner("正在清除数据..."):
                        cleared_count = 0
                        
                        if "学生打卡记录" in clear_type:
                            # 清除打卡记录
                            import os
                            checkin_file = 'checkin_records.json'
                            if os.path.exists(checkin_file):
                                # 读取现有打卡记录
                                import json
                                with open(checkin_file, 'r', encoding='utf-8') as f:
                                    checkin_records = json.load(f)
                                
                                # 只保留非该老师管理学生的打卡记录
                                student_ids = [s['user_id'] for s in student_list]
                                new_checkin_records = []
                                for record in checkin_records:
                                    if record.get('user_id') not in student_ids:
                                        new_checkin_records.append(record)
                                
                                # 保存新的打卡记录
                                with open(checkin_file, 'w', encoding='utf-8') as f:
                                    json.dump(new_checkin_records, f, ensure_ascii=False, indent=2)
                                
                                cleared_count += 1
                        
                        if "学生积分数据" in clear_type:
                            # 清除学生积分数据
                            student_ids = [s['user_id'] for s in student_list]
                            new_scores_data = {}
                            for user_id, score_info in scores_data.items():
                                if user_id not in student_ids:
                                    new_scores_data[user_id] = score_info
                            st.session_state.scores_data = new_scores_data
                            save_scores_data(st.session_state.scores_data)
                            cleared_count += 1
                        
                        # 清除成功
                        st.success(f"✅ 数据清除成功！已清除 {cleared_count} 类数据。")
                        st.balloons()
                        
                        # 刷新页面
                        import time
                        time.sleep(1)
                        st.rerun()
        
        st.markdown("---")
        
        st.subheader("💥 一键全部清除")
        
        st.error("⚠️ 警告：此操作将清除您所管理班级的所有打卡记录和积分数据！")
        
        clear_all_confirm = st.checkbox("我确认要清除所有数据，此操作无法恢复")
        
        if clear_all_confirm:
            if st.button("🧨 一键全部清除", type="primary", use_container_width=True):
                with st.spinner("正在清除所有数据..."):
                    # 清除打卡记录
                    import os
                    import json
                    checkin_file = 'checkin_records.json'
                    if os.path.exists(checkin_file):
                        with open(checkin_file, 'r', encoding='utf-8') as f:
                            checkin_records = json.load(f)
                        
                        student_ids = [s['user_id'] for s in student_list]
                        new_checkin_records = []
                        for record in checkin_records:
                            if record.get('user_id') not in student_ids:
                                new_checkin_records.append(record)
                        
                        with open(checkin_file, 'w', encoding='utf-8') as f:
                            json.dump(new_checkin_records, f, ensure_ascii=False, indent=2)
                    
                    # 清除学生积分数据
                    student_ids = [s['user_id'] for s in student_list]
                    new_scores_data = {}
                    for user_id, score_info in scores_data.items():
                        if user_id not in student_ids:
                            new_scores_data[user_id] = score_info
                    st.session_state.scores_data = new_scores_data
                    save_scores_data(st.session_state.scores_data)
                    
                    st.success("✅ 所有数据已清除！")
                    st.balloons()
                    
                    import time
                    time.sleep(2)
                    st.rerun()
    
    # 行政楼能耗
    elif st.session_state.teacher_selected_page == "行政楼能耗":
        st.subheader("🏢 行政楼能耗监测")
        
        st.markdown("""
        实时监测行政楼能耗情况，智能检测未关水电设备，保障办公环境节能高效！
        """)
        
        st.markdown("---")
        
        # 下班智能检测未关水电提示弹窗
        from datetime import datetime
        current_hour = datetime.now().hour
        
        # 模拟下班时间检测（17:00-18:00之间显示提示）
        if 17 <= current_hour <= 18:
            st.warning("""
            ⚠️ **下班提醒**
            
            检测到当前为下班时间，请检查以下设备是否已关闭：
            - 💡 办公室照明
            - 💻 电脑及显示器
            - ❄️ 空调设备
            - 🚰 饮水机
            - 🔌 其他用电设备
            
            请确保所有设备关闭后再离开，共同节约能源！
            """)
        
        # 能耗概览
        st.subheader("📊 能耗概览")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("今日电耗", "118.5 kWh", "↓ 8.2%")
            st.metric("本月电耗", "2,856 kWh", "↓ 12.3%")
        
        with col2:
            st.metric("今日水耗", "2.3 吨", "↓ 5.1%")
            st.metric("节能率", "15.8%", "↑ 3.2%")
        
        st.markdown("---")
        
        # 筛选条件
        st.subheader("🔍 筛选条件")
        
        col_filter1, col_filter2 = st.columns(2)
        
        with col_filter1:
            time_range = st.selectbox("时间范围", ["今日", "本周", "本月", "自定义"], key="admin_building_time")
            
            if time_range == "自定义":
                custom_date_range = st.date_input("选择日期范围", value=(datetime.now().date(), datetime.now().date()), key="admin_building_date")
        
        with col_filter2:
            energy_type = st.selectbox("能耗类型", ["全部", "电耗", "水耗"], key="admin_building_energy_type")
        
        st.markdown("---")
        
        # 能耗数据可视化
        st.subheader("📈 能耗数据可视化")
        
        # 左右两列布局
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("#### 电耗趋势")
            
            # 电耗趋势筛选条件
            electricity_time_range = st.selectbox("时间范围", ["今日", "本周", "本月", "自定义"], key="electricity_time", index=2)
            
            # 根据时间范围生成数据
            if electricity_time_range == "今日":
                dates = ["04月11日"]
                electricity_data = [118]
            elif electricity_time_range == "本周":
                dates = pd.date_range('2026-04-05', '2026-04-11').strftime('%m月%d日')
                electricity_data = [112, 108, 115, 120, 118, 95, 88]
            elif electricity_time_range == "本月":
                dates = pd.date_range('2026-04-01', '2026-04-11').strftime('%m月%d日')
                electricity_data = [125, 118, 122, 115, 120, 118, 112, 108, 115, 120, 118]
            else:  # 自定义
                dates = pd.date_range('2026-04-01', '2026-04-11').strftime('%m月%d日')
                electricity_data = [125, 118, 122, 115, 120, 118, 112, 108, 115, 120, 118]
            
            fig_electricity = go.Figure()
            fig_electricity.add_trace(go.Scatter(
                x=dates,
                y=electricity_data,
                mode='lines+markers',
                name='电耗 (kWh)',
                line=dict(color='#fa8c16', width=3),
                marker=dict(size=8)
            ))
            fig_electricity.update_layout(
                xaxis_title='日期',
                yaxis_title='电耗 (kWh)',
                height=400,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_electricity, use_container_width=True)
        
        with col_chart2:
            st.markdown("#### 水耗趋势")
            
            # 水耗趋势筛选条件
            water_time_range = st.selectbox("时间范围", ["今日", "本周", "本月", "自定义"], key="water_time", index=2)
            
            # 根据时间范围生成数据
            if water_time_range == "今日":
                dates = ["04月11日"]
                water_data = [2.3]
            elif water_time_range == "本周":
                dates = pd.date_range('2026-04-05', '2026-04-11').strftime('%m月%d日')
                water_data = [2.0, 2.2, 2.3, 2.4, 2.3, 1.8, 1.6]
            elif water_time_range == "本月":
                dates = pd.date_range('2026-04-01', '2026-04-11').strftime('%m月%d日')
                water_data = [2.5, 2.3, 2.4, 2.2, 2.3, 2.1, 2.0, 2.2, 2.3, 2.4, 2.3]
            else:  # 自定义
                dates = pd.date_range('2026-04-01', '2026-04-11').strftime('%m月%d日')
                water_data = [2.5, 2.3, 2.4, 2.2, 2.3, 2.1, 2.0, 2.2, 2.3, 2.4, 2.3]
            
            fig_water = go.Figure()
            fig_water.add_trace(go.Scatter(
                x=dates,
                y=water_data,
                mode='lines+markers',
                name='水耗 (吨)',
                line=dict(color='#1890ff', width=3),
                marker=dict(size=8)
            ))
            fig_water.update_layout(
                xaxis_title='日期',
                yaxis_title='水耗 (吨)',
                height=400,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_water, use_container_width=True)
        
        st.markdown("---")
        
        # 能耗对比分析
        st.subheader("📊 能耗对比分析")
        
        col_compare1, col_compare2 = st.columns(2)
        
        with col_compare1:
            st.markdown("#### 本周 vs 上周电耗对比")
            
            week_days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            this_week = [125, 118, 122, 115, 120, 85, 72]
            last_week = [132, 128, 130, 125, 128, 90, 78]
            
            fig_compare = go.Figure()
            fig_compare.add_trace(go.Bar(
                name='本周',
                x=week_days,
                y=this_week,
                marker_color='#52c41a'
            ))
            fig_compare.add_trace(go.Bar(
                name='上周',
                x=week_days,
                y=last_week,
                marker_color='#1890ff'
            ))
            fig_compare.update_layout(
                barmode='group',
                xaxis_title='日期',
                yaxis_title='电耗 (kWh)',
                height=400,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_compare, use_container_width=True)
        
        with col_compare2:
            st.markdown("#### 能耗分布")
            
            # 能耗分布饼图
            energy_distribution = {
                "照明": 35,
                "空调": 40,
                "电脑设备": 15,
                "其他": 10
            }
            
            fig_pie = go.Figure()
            fig_pie.add_trace(go.Pie(
                labels=list(energy_distribution.keys()),
                values=list(energy_distribution.values()),
                hoverinfo='label+percent',
                textinfo='percent',
                textfont=dict(size=14),
                marker=dict(colors=['#1890ff', '#52c41a', '#fa8c16', '#722ed1'])
            ))
            fig_pie.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown("---")
        
        # 行政楼耗能数据监测系统
        st.subheader("🏢 行政楼耗能数据监测系统")
        
        # 楼层能耗详情
        st.markdown("#### 各楼层能耗详情")
        
        floor_data = [
            {"楼层": "1楼", "电耗 (kWh)": 25.5, "水耗 (吨)": 0.5, "状态": "正常", "节能率": "12%"},
            {"楼层": "2楼", "电耗 (kWh)": 28.3, "水耗 (吨)": 0.6, "状态": "正常", "节能率": "15%"},
            {"楼层": "3楼", "电耗 (kWh)": 32.1, "水耗 (吨)": 0.7, "状态": "偏高", "节能率": "8%"},
            {"楼层": "4楼", "电耗 (kWh)": 22.8, "水耗 (吨)": 0.4, "状态": "正常", "节能率": "18%"},
            {"楼层": "5楼", "电耗 (kWh)": 18.5, "水耗 (吨)": 0.3, "状态": "优秀", "节能率": "25%"}
        ]
        
        df_floor = pd.DataFrame(floor_data)
        
        # 根据状态设置样式
        def highlight_status(val):
            if val == "优秀":
                return 'background-color: #52c41a; color: white'
            elif val == "正常":
                return 'background-color: #1890ff; color: white'
            elif val == "偏高":
                return 'background-color: #fa8c16; color: white'
            elif val == "异常":
                return 'background-color: #ff4d4f; color: white'
            else:
                return ''
        
        styled_df = df_floor.style.applymap(highlight_status, subset=["状态"])
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # 实时设备监测
        st.markdown("#### 实时设备监测")
        
        col_device1, col_device2, col_device3 = st.columns(3)
        
        with col_device1:
            st.markdown("""
            <div style='background-color: #f0f8ff; padding: 15px; border-radius: 10px; border-left: 4px solid #1890ff;'>
                <h5 style='margin: 0 0 10px 0; color: #1890ff;'>💡 照明系统</h5>
                <p style='margin: 0; font-size: 14px;'>运行状态：<strong style='color: #52c41a;'>正常</strong></p>
                <p style='margin: 0; font-size: 14px;'>当前功率：<strong>12.5 kW</strong></p>
                <p style='margin: 0; font-size: 14px;'>开启设备：<strong>45/60</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_device2:
            st.markdown("""
            <div style='background-color: #f0f8ff; padding: 15px; border-radius: 10px; border-left: 4px solid #52c41a;'>
                <h5 style='margin: 0 0 10px 0; color: #52c41a;'>❄️ 空调系统</h5>
                <p style='margin: 0; font-size: 14px;'>运行状态：<strong style='color: #52c41a;'>正常</strong></p>
                <p style='margin: 0; font-size: 14px;'>当前功率：<strong>35.2 kW</strong></p>
                <p style='margin: 0; font-size: 14px;'>开启设备：<strong>12/15</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_device3:
            st.markdown("""
            <div style='background-color: #f0f8ff; padding: 15px; border-radius: 10px; border-left: 4px solid #fa8c16;'>
                <h5 style='margin: 0 0 10px 0; color: #fa8c16;'>🚰 供水系统</h5>
                <p style='margin: 0; font-size: 14px;'>运行状态：<strong style='color: #52c41a;'>正常</strong></p>
                <p style='margin: 0; font-size: 14px;'>当前流量：<strong>2.3 吨/日</strong></p>
                <p style='margin: 0; font-size: 14px;'>水压：<strong>0.35 MPa</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 异常设备提醒
        st.markdown("#### ⚠️ 异常设备提醒")
        
        abnormal_devices = [
            {"设备": "3楼会议室空调", "问题": "温度设置过低", "当前值": "18℃", "建议值": "26℃", "状态": "待处理"},
            {"设备": "2楼走廊照明", "问题": "白天未关闭", "当前值": "开启", "建议值": "关闭", "状态": "待处理"},
            {"设备": "4楼饮水机", "问题": "长时间待机", "当前值": "待机12小时", "建议值": "及时关闭", "状态": "已提醒"}
        ]
        
        df_abnormal = pd.DataFrame(abnormal_devices)
        st.dataframe(df_abnormal, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # 智能节能建议
        st.markdown("#### 💡 智能节能建议")
        
        suggestions = [
            "建议将3楼会议室空调温度调整至26℃，预计可节约15%电耗",
            "建议关闭2楼走廊白天照明，利用自然光照明",
            "建议4楼饮水机设置定时开关，避免长时间待机",
            "建议下班后统一关闭非必要设备，可节约20%能耗"
        ]
        
        for i, suggestion in enumerate(suggestions, 1):
            st.markdown(f"**{i}.** {suggestion}")
    
    # 学生耗电异常申诉
    elif st.session_state.teacher_selected_page == "学生耗电异常申诉":
        st.subheader("⚠️ 学生耗电异常申诉")
        
        # 统计卡片
        st.markdown("### 申诉统计")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
                <h4 style='margin: 0 0 10px 0; color: #1a1a1a; font-size: 18px;'>今日申诉量 📊</h4>
                <p style='margin: 0; font-size: 28px; font-weight: bold; color: #1890ff;'>5</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
                <h4 style='margin: 0 0 10px 0; color: #1a1a1a; font-size: 18px;'>待处理申诉 ⏳</h4>
                <p style='margin: 0; font-size: 28px; font-weight: bold; color: #faad14;'>3</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
                <h4 style='margin: 0 0 10px 0; color: #1a1a1a; font-size: 18px;'>历史处理率 📈</h4>
                <p style='margin: 0; font-size: 28px; font-weight: bold; color: #52c41a;'>85%</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 模拟申诉数据
        if 'appeals' not in st.session_state:
            st.session_state.appeals = [
                {'日期': '2024-01-16', '学生': '张三', '宿舍': '1号楼101', '耗电异常值': '5.2 kWh', '状态': '待处理'},
                {'日期': '2024-01-16', '学生': '李四', '宿舍': '1号楼102', '耗电异常值': '4.8 kWh', '状态': '待处理'},
                {'日期': '2024-01-15', '学生': '王五', '宿舍': '2号楼201', '耗电异常值': '6.1 kWh', '状态': '待处理'},
                {'日期': '2024-01-15', '学生': '赵六', '宿舍': '2号楼202', '耗电异常值': '3.9 kWh', '状态': '已通过'},
                {'日期': '2024-01-14', '学生': '钱七', '宿舍': '3号楼301', '耗电异常值': '4.5 kWh', '状态': '已驳回'}
            ]
        
        # 所有申诉数据
        filtered_appeals = st.session_state.appeals
        
        # 显示申诉表格
        st.markdown("### 申诉列表")
        if filtered_appeals:
            # 准备表格数据
            table_data = {
                '日期': [],
                '学生姓名': [],
                '宿舍号': [],
                '耗电异常值': [],
                '待处理': []
            }
            
            for appeal in filtered_appeals:
                table_data['日期'].append(appeal['日期'])
                table_data['学生姓名'].append(appeal['学生'])
                table_data['宿舍号'].append(appeal['宿舍'])
                table_data['耗电异常值'].append(appeal['耗电异常值'])
                table_data['待处理'].append(appeal['状态'] == '待处理')
            
            df_appeals = pd.DataFrame(table_data)
            st.dataframe(df_appeals, use_container_width=True)
            
            # 审核功能
            st.markdown("### 审核申诉")
            appeal_index = st.selectbox("选择要审核的申诉", options=range(len(filtered_appeals)), format_func=lambda x: f"{filtered_appeals[x]['学生']} - {filtered_appeals[x]['日期']}")
            
            if appeal_index is not None:
                appeal = filtered_appeals[appeal_index]
                # 找到原始索引
                original_index = st.session_state.appeals.index(appeal)
                
                st.markdown(f"**学生**: {appeal['学生']}")
                st.markdown(f"**宿舍**: {appeal['宿舍']}")
                st.markdown(f"**日期**: {appeal['日期']}")
                st.markdown(f"**耗电异常值**: {appeal['耗电异常值']}")
                st.markdown(f"**当前状态**: {appeal['状态']}")
                
                # 审核按钮
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("通过申诉", type="primary"):
                        import datetime
                        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        st.session_state.appeals[original_index]['状态'] = '已通过'
                        st.session_state.appeals[original_index]['处理时间'] = now
                        st.session_state.appeals[original_index]['处理人'] = st.session_state.user_name
                        st.success("申诉已通过！")
                        st.rerun()
                with col2:
                    if st.button("驳回申诉", type="secondary"):
                        import datetime
                        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        st.session_state.appeals[original_index]['状态'] = '已驳回'
                        st.session_state.appeals[original_index]['处理时间'] = now
                        st.session_state.appeals[original_index]['处理人'] = st.session_state.user_name
                        st.success("申诉已驳回！")
                        st.rerun()
        else:
            st.markdown("暂无申诉记录")
        
        # 申诉处理记录
        st.markdown("### 📋 申诉处理记录")
        
        # 筛选已处理的申诉
        processed_appeals = [appeal for appeal in st.session_state.appeals if appeal['状态'] in ['已通过', '已驳回']]
        
        if processed_appeals:
            # 整理处理记录数据
            processing_records = []
            for appeal in processed_appeals:
                processing_records.append({
                    '日期': appeal.get('日期', ''),
                    '学生': appeal.get('学生', ''),
                    '宿舍': appeal.get('宿舍', ''),
                    '耗电异常值': appeal.get('耗电异常值', ''),
                    '处理状态': appeal.get('状态', ''),
                    '处理时间': appeal.get('处理时间', '未知'),
                    '处理人': appeal.get('处理人', '未知')
                })
            
            df_processing_records = pd.DataFrame(processing_records)
            st.dataframe(df_processing_records, use_container_width=True)
        else:
            st.markdown("暂无处理记录")
        
        st.markdown("---")
        
        # 数据可视化
        st.markdown("### 申诉数据分析")
        col1, col2 = st.columns(2)
        
        with col1:
            # 近七日申诉趋势图
            st.markdown("#### 近七日申诉趋势")
            dates = ['1月10日', '1月11日', '1月12日', '1月13日', '1月14日', '1月15日', '1月16日']
            appeal_counts = [1, 2, 0, 3, 1, 2, 2]
            
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(
                x=dates,
                y=appeal_counts,
                mode='lines+markers',
                line=dict(color='#1890ff', width=2),
                marker=dict(size=6, color='#1890ff')
            ))
            fig_trend.update_layout(
                xaxis_title='日期',
                yaxis_title='申诉数量',
                height=300
            )
            st.plotly_chart(fig_trend, use_container_width=True)
        
        with col2:
            # 班级申诉占比饼图
            st.markdown("#### 班级申诉占比")
            class_data = {
                '班级': ['23级财务管理01班', '23级财务管理02班', '23级会计01班', '23级会计02班', '23级审计01班'],
                '申诉数量': [3, 1, 0, 1, 0]
            }
            df_class = pd.DataFrame(class_data)
            
            fig_pie = go.Figure()
            fig_pie.add_trace(go.Pie(
                labels=df_class['班级'],
                values=df_class['申诉数量'],
                hole=0.3
            ))
            fig_pie.update_layout(
                height=300
            )
            st.plotly_chart(fig_pie, use_container_width=True)

# 主函数
if __name__ == "__main__":
    # 初始化会话状态
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_position' not in st.session_state:
        st.session_state.user_position = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'user_name' not in st.session_state:
        st.session_state.user_name = None
    if 'dormitory' not in st.session_state:
        st.session_state.dormitory = None
    
    # 登录页面
    if not st.session_state.logged_in:
        st.set_page_config(
            page_title="校园能耗监测与智能节能系统",
            page_icon="🔐",
            layout="centered"
        )
        
        st.title("🔐 校园能耗监测与智能节能系统")
        st.markdown("<h2 style='text-align: center;'>登录页面</h2>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>欢迎使用，校园能耗监测与智能节能系统</h3>", unsafe_allow_html=True)
        
        # 两列布局，设置为相同宽度
        col1, col2 = st.columns([1, 1], gap="medium")
        
        with col1:
            # 系统功能（垂直居中）
            st.markdown("""
            <div style='height: 400px; display: flex; align-items: center;'>
                <div style='background-color: #f0f8ff; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); width: 100%;'>
                    <h3 style='margin: 0 0 16px 0; color: #1890ff;'>系统功能</h3>
                    <ul style='margin: 0; padding-left: 20px;'>
                        <li>水电气热综合监测</li>
                        <li>智能节能调控</li>
                        <li>碳积分小程序</li>
                        <li>AI实时分析</li>
                        <li>数据上传与管理</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # 登录方式选择
            st.markdown("<h3 style='margin-bottom: 0px;'>选择登录方式</h3>", unsafe_allow_html=True)
            login_method = st.radio(
                "登录方式",
                options=["账号密码登录", "手机号码登录", "企业微信扫码登录"],
                index=0,
                horizontal=True
            )
            
            # 登录表单（更紧凑）
            st.markdown("<div style='margin-top: -15px;'>", unsafe_allow_html=True)
            with st.form("login_form"):
                if login_method == "账号密码登录":
                    username = st.text_input("用户名", label_visibility="visible")
                    password = st.text_input("密码", type="password", label_visibility="visible")
                elif login_method == "手机号码登录":
                    phone = st.text_input("手机号码", label_visibility="visible")
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        verification_code = st.text_input("验证码", label_visibility="visible")
                    with col2:
                        if st.form_submit_button("获取验证码", use_container_width=True):
                            # 生成随机6位验证码
                            import random
                            verify_code = ''.join(random.choices('0123456789', k=6))
                            st.session_state.verification_code = verify_code
                            st.info(f"验证码已发送到您的手机，验证码为：{verify_code}")
                elif login_method == "企业微信扫码登录":
                    st.markdown("<h3 style='margin-bottom: 10px;'>请使用企业微信扫码登录</h3>", unsafe_allow_html=True)
                    st.image("https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=login", width=200)
                    st.markdown("<div style='text-align: center;'>请使用企业微信扫描上方二维码</div>", unsafe_allow_html=True)
                
                submitted = st.form_submit_button("登录", type="primary")
            st.markdown("</div>", unsafe_allow_html=True)
                
            if submitted:
                # 简单的登录验证（实际应用中应该从数据库验证）
                # 根据账号自动判断身份
                if login_method == "账号密码登录":
                    # 验证用户名和密码
                    if not username:
                        st.error("请输入用户名")
                        st.stop()
                    if not password:
                        st.error("请输入密码")
                        st.stop()
                    user_id = username
                elif login_method == "手机号码登录":
                    # 验证手机号和验证码
                    if not phone:
                        st.error("请输入手机号码")
                        st.stop()
                    if not verification_code:
                        st.error("请输入验证码")
                        st.stop()
                    # 验证验证码
                    if 'verification_code' not in st.session_state:
                        st.error("请先获取验证码")
                        st.stop()
                    if verification_code != st.session_state.verification_code:
                        st.error("验证码错误")
                        st.stop()
                    user_id = phone
                else:
                    # 企业微信扫码登录，默认使用admin账号
                    user_id = "admin"
                
                # 从用户数据中验证
                users_data = st.session_state.users_data
                if user_id in users_data:
                    # 验证密码（账号密码登录时）
                    if login_method == "账号密码登录":
                        if password != users_data[user_id].get('password', '12345678'):
                            st.error("密码错误")
                            st.stop()
                    
                    # 登录成功
                    st.session_state.logged_in = True
                    st.session_state.user_position = users_data[user_id]['role']
                    st.session_state.username = user_id
                    st.session_state.user_id = user_id  # 添加user_id属性
                    st.session_state.user_name = users_data[user_id]['name']
                    
                    if users_data[user_id]['role'] == '学生':
                        st.session_state.dormitory = users_data[user_id].get('dormitory', '1号楼101')
                        
                        # 初始化学生积分信息
                        scores_data = st.session_state.scores_data
                        if user_id in scores_data:
                            score_info = scores_data[user_id]
                            st.session_state.weekly_score = score_info.get('weekly_score', 0)
                            st.session_state.monthly_score = score_info.get('monthly_score', 0)
                            st.session_state.student_class = score_info.get('class', '未分配班级')
                            # 当前积分使用月积分
                            st.session_state.current_points = st.session_state.monthly_score
                        else:
                            # 如果没有积分数据，设置默认值
                            st.session_state.weekly_score = 0
                            st.session_state.monthly_score = 0
                            st.session_state.student_class = '未分配班级'
                            st.session_state.current_points = 0
                        
                        # 初始化积分明细，让最后一条记录的余额与当前积分一致
                        if 'points_detail' not in st.session_state or not st.session_state.points_detail:
                            st.session_state.points_detail = [
                                {
                                    '时间': '2024-01-01 00:00:00',
                                    '来源': '初始积分',
                                    '积分变动': f'+{st.session_state.current_points}',
                                    '余额': st.session_state.current_points
                                }
                            ]
                        else:
                            # 更新最后一条记录的余额，确保与当前积分一致
                            last_record = st.session_state.points_detail[-1]
                            last_record['余额'] = st.session_state.current_points
                    elif users_data[user_id]['role'] == '老师' or users_data[user_id]['role'] == '辅导员':
                        st.session_state.classes = users_data[user_id].get('class_info', users_data[user_id].get('classes', ''))
                    
                    st.rerun()
                else:
                    st.error("用户名不存在")
                    st.stop()
        
        # 测试账号信息
        st.markdown("### 测试账号")
        st.markdown("管理者: admin / 12345678")
        st.markdown("学生: zhangshan / 12345678")
        st.markdown("老师: wang / 12345678 (王老师 - 23级财务管理01班,23级财务管理02班)")
        st.markdown("老师: deng / 12345678 (邓老师 - 22级会计01班,22级会计02班)")
    else:
        # 根据用户身份显示不同页面
        if st.session_state.user_position == "学生":
            student_page()
        elif st.session_state.user_position == "老师" or st.session_state.user_position == "辅导员":
            teacher_page()
        elif st.session_state.user_position == "管理者":
            admin_page()