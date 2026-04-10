import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 全局变量
checkin_data = []

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
    # 初始化积分明细
    if 'points_detail' not in st.session_state:
        st.session_state.points_detail = [
            {'时间': '2024-01-10 08:00:00', '来源': '日常打卡', '积分变动': '+10', '余额': 810},
            {'时间': '2024-01-11 08:30:00', '来源': '日常打卡', '积分变动': '+10', '余额': 820},
            {'时间': '2024-01-12 09:00:00', '来源': '日常打卡', '积分变动': '+10', '余额': 830},
            {'时间': '2024-01-13 08:15:00', '来源': '日常打卡', '积分变动': '+10', '余额': 840},
            {'时间': '2024-01-14 08:45:00', '来源': '日常打卡', '积分变动': '+10', '余额': 850},
        ]  # 积分明细
    
    # 首页页面
    if st.session_state.selected_page == "首页":
        # 首页 - 个人信息
        st.subheader("👤 个人信息")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='background-color: #f0f8ff; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #1890ff;'>基本信息</h4>
                <p><strong>姓名:</strong> {}</p>
                <p><strong>宿舍:</strong> {}</p>
                <p><strong>职务:</strong> 学生</p>
                <p><strong>年级:</strong> 23级</p>
                <p><strong>班级:</strong> 财务管理01班</p>
                <p><strong>学号:</strong> 20230123</p>
            </div>
            """
            .format(st.session_state.user_name, st.session_state.dormitory), unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background-color: #e3f2fd; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #1976D2;'>积分信息</h4>
                <p><strong>当前积分:</strong> {st.session_state.current_points}</p>
                <p><strong>本月获得:</strong> 120</p>
                <p><strong>本月积分排名:</strong> 第3名</p>
                <p><strong>总积分排名:</strong> 第5名</p>
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
                    
                    # 添加打卡记录到全局打卡数据
                    new_checkin = {
                        '日期': today,
                        '学生': st.session_state.user_name,
                        '宿舍': st.session_state.dormitory,
                        '班级': '23级财务管理01班',  # 模拟班级
                        '积分': 10,
                        '行为': '日常打卡'  # 日常打卡行为
                    }
                    checkin_data.append(new_checkin)
                    
                    st.success("打卡成功！获得10积分奖励！")
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
        
        # 时间选择 - 改为开始日期和结束日期
        st.markdown("### 班级能耗统计")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("开始日期", value=pd.to_datetime('2024-01-10'))
        with col2:
            end_date = st.date_input("结束日期", value=pd.to_datetime('2024-01-15'))
        
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
                    # 添加打卡记录到全局打卡数据
                    new_checkin = {
                        '日期': today,
                        '学生': st.session_state.user_name,
                        '宿舍': st.session_state.dormitory,
                        '班级': '23级财务管理01班',  # 模拟班级
                        '积分': 10,
                        '行为': action
                    }
                    checkin_data.append(new_checkin)
                    
                    # 更新节能打卡状态
                    st.session_state.last_energy_checkin_date = today
                    
                    st.success("节能打卡成功！获得10积分奖励！")
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
                        # 扣除积分
                        st.session_state.current_points -= 300
                        # 记录兑换历史
                        import datetime
                        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        st.session_state.exchange_history.append({
                            '时间': now,
                            '商品': '素拓0.1',
                            '消耗积分': 300,
                            '剩余积分': st.session_state.current_points
                        })
                        # 记录积分明细
                        st.session_state.points_detail.append({
                            '时间': now,
                            '来源': '兑换素拓0.1',
                            '积分变动': '-300',
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
                        # 扣除积分
                        st.session_state.current_points -= 200
                        # 记录兑换历史
                        import datetime
                        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        st.session_state.exchange_history.append({
                            '时间': now,
                            '商品': '劳动时长0.5',
                            '消耗积分': 200,
                            '剩余积分': st.session_state.current_points
                        })
                        # 记录积分明细
                        st.session_state.points_detail.append({
                            '时间': now,
                            '来源': '兑换劳动时长0.5',
                            '积分变动': '-200',
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
        
        # 本周和本月排行
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
                "数据接口": "数据接口"
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
            water_dates = pd.date_range('2024-01-01', '2024-01-15').strftime('%m-%d')
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
            power_dates = pd.date_range('2024-01-01', '2024-01-15').strftime('%m-%d')
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
        
        st.markdown("---")
        
        # 筛选条件
        st.subheader("🔍 筛选条件")
        
        col_filter1, col_filter2 = st.columns(2)
        
        with col_filter1:
            warning_level = st.selectbox("预警级别", ["全部", "一级预警", "二级预警", "三级预警"])
        
        with col_filter2:
            building_status = st.selectbox("处理状态", ["全部", "待处理", "处理中", "已处理"])
        
        st.markdown("---")
        
        # 电耗监测过高值数据表
        st.subheader("🏢 电耗监测过高值数据表")
        
        # 模拟预警数据
        warning_data = [
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
        
        df_warning = pd.DataFrame(warning_data)
        
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
        
        # 预警详情操作
        st.subheader("⚡ 预警处理")
        
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
                    st.success(f"{selected_building} 已标记为处理中！")
                elif action_type == "标记已处理":
                    st.success(f"{selected_building} 已标记为已处理！")
                elif action_type == "发送通知":
                    st.success(f"已向 {selected_building} 发送预警通知！")
                    st.balloons()
        
        st.markdown("---")
        
        # 预警趋势分析
        st.subheader("📈 预警趋势分析")
        
        # 模拟预警趋势数据
        warning_dates = pd.date_range('2026-04-01', '2026-04-11').strftime('%m-%d')
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
        
        import_type = st.selectbox("选择导入类型", ["学生信息", "教师信息", "能耗数据"])
        
        uploaded_file = st.file_uploader("选择文件上传", type=["csv", "xlsx"])
        if uploaded_file is not None:
            # 读取上传的文件
            if uploaded_file.name.endswith('.csv'):
                df_uploaded = pd.read_csv(uploaded_file)
                st.dataframe(df_uploaded, use_container_width=True)
                
                if st.button("导入数据", type="primary"):
                    st.success(f"{import_type}导入成功！")
                    st.balloons()
            else:
                # Excel文件 - 获取所有sheet
                excel_file = pd.ExcelFile(uploaded_file)
                sheet_names = excel_file.sheet_names
                
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
                            st.success(f"{import_type}导入成功！共导入 {len(selected_sheets)} 个工作表")
                            st.balloons()
                        else:
                            st.warning("请至少选择一个工作表")
                else:
                    df_uploaded = pd.read_excel(uploaded_file, sheet_name=sheet_names[0])
                    st.markdown("---")
                    st.markdown(f"### 工作表：{sheet_names[0]}")
                    st.dataframe(df_uploaded, use_container_width=True)
                    
                    if st.button("导入数据", type="primary"):
                        st.success(f"{import_type}导入成功！")
                        st.balloons()
        
        st.markdown("---")
        
        # 数据导出
        st.subheader("📤 数据导出")
        
        export_type = st.selectbox("选择导出类型", ["学生信息", "教师信息", "能耗数据", "节能打卡记录", "积分表"])
        
        if export_type == "学生信息":
            # 模拟学生信息数据
            student_data = {
                '学号': ['20230101', '20230102', '20230103', '20230104', '20230105'],
                '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
                '班级': ['23级财务管理01班', '23级财务管理01班', '23级财务管理02班', '23级财务管理02班', '23级财务管理01班'],
                '宿舍': ['1号楼101', '1号楼102', '2号楼201', '2号楼202', '1号楼103'],
                '积分': [850, 780, 920, 650, 720],
                '联系电话': ['13800138001', '13800138002', '13800138003', '13800138004', '13800138005']
            }
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
        
        elif export_type == "教师信息":
            # 模拟教师信息数据
            teacher_data = {
                '工号': ['T001', 'T002', 'T003', 'T004', 'T005'],
                '姓名': ['王老师', '邓老师', '李老师', '张老师', '刘老师'],
                '职务': ['辅导员', '辅导员', '教师', '教师', '行政人员'],
                '管理班级': ['23级财务管理01班,23级财务管理02班', '22级会计01班,22级会计02班', '23级审计01班', '23级审计02班', '无'],
                '办公室': ['行政楼302', '行政楼303', '教学楼A301', '教学楼A302', '行政楼201'],
                '联系电话': ['13900139001', '13900139002', '13900139003', '13900139004', '13900139005']
            }
            df_teacher = pd.DataFrame(teacher_data)
            st.dataframe(df_teacher, use_container_width=True, hide_index=True)
            
            # 导出为CSV
            csv = df_teacher.to_csv(index=False)
            st.download_button(
                label="导出教师信息",
                data=csv,
                file_name="教师信息.csv",
                mime="text/csv"
            )
            
            # 导出为Excel
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output) as writer:
                df_teacher.to_excel(writer, index=False, sheet_name='教师信息')
            output.seek(0)
            st.download_button(
                label="导出教师信息 (Excel)",
                data=output,
                file_name="教师信息.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        elif export_type == "能耗数据":
            # 模拟能耗数据
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
                "节能建议": "节能建议"
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
        # 教师基本信息
        st.subheader("👨‍🏫 基本信息")
        
        # 模拟教师信息数据
        # 将来可以从Excel文件或API接口获取实际数据
        # 例如：从Excel读取教师所带班级信息
        # import pandas as pd
        # df = pd.read_excel('teacher_classes.xlsx')
        # teacher_classes = df[df['教师姓名'] == st.session_state.user_name]['班级'].tolist()
        # 或者通过API接口获取
        # import requests
        # response = requests.get(f'http://api.example.com/teacher/{st.session_state.user_name}/classes')
        # teacher_classes = response.json()
        
        # 模拟5个班级数据
        teacher_classes = ['23级财务管理01班', '23级财务管理02班', '23级会计01班', '23级会计02班', '23级审计01班']
        
        teacher_info = {
            '姓名': st.session_state.user_name,
            '职务': '辅导员',
            '管理班级': '、'.join(teacher_classes),
            '办公室地点': '行政楼302室'
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
            st.markdown("""
            <div style='background-color: #e8f5e8; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1); height: 120px; display: flex; flex-direction: column; justify-content: center;'>
                <h4 style='margin: 0 0 8px 0; color: #2e7d32;'>总学生数</h4>
                <p style='margin: 0; font-size: 24px; font-weight: bold;'>240</p>
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
            else:
                # 模拟日期范围
                start_date = pd.to_datetime("2024-01-16")  # 今日
                end_date = pd.to_datetime("2024-01-16")  # 今日
            
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
        
        # 专业班级查询栏
        col1, col2 = st.columns(2)
        with col1:
            majors = st.multiselect("选择专业", ["财务管理", "会计", "审计"], default=["财务管理", "会计"])
        with col2:
            class_names = st.multiselect("选择班级", ["01班", "02班", "03班"], default=["01班", "02班"])
        
        # 班级总能耗卡片
        st.markdown("### 班级总能耗")
        
        # 模拟班级能耗数据（5个班级）
        class_energy_data = {
            '23级财务管理01班': {'总能耗': 125.5, '达标率': 85, '环比': -5.2},
            '23级财务管理02班': {'总能耗': 118.3, '达标率': 90, '环比': -3.8},
            '23级会计01班': {'总能耗': 132.7, '达标率': 78, '环比': 2.1},
            '23级会计02班': {'总能耗': 128.9, '达标率': 82, '环比': -1.5},
            '23级审计01班': {'总能耗': 115.2, '达标率': 92, '环比': -6.3}
        }
        
        # 1X5排版显示班级能耗卡片
        cols = st.columns(5)
        for i, (class_name_data, energy_info) in enumerate(class_energy_data.items()):
            with cols[i]:
                # 计算环比颜色
                rate_color = "green" if energy_info['环比'] < 0 else "red"
                rate_sign = "↓" if energy_info['环比'] < 0 else "↑"
                
                # 卡片内容
                st.markdown(f"""
                <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 15px; min-height: 120px; display: flex; flex-direction: column; justify-content: space-between;'>
                    <h5 style='margin: 0 0 8px 0; color: #1a1a1a; font-size: 14px;'>{class_name_data}</h5>
                    <div style='margin-bottom: 5px;'>
                        <span style='font-size: 12px; color: #666;'>总能耗: <strong>{energy_info['总能耗']} kWh</strong></span>
                    </div>
                    <div style='margin-bottom: 5px;'>
                        <span style='font-size: 12px; color: #666;'>达标率: <strong>{energy_info['达标率']}%</strong></span>
                    </div>
                    <div style='margin-bottom: 0;'>
                        <span style='font-size: 12px; color: #666;'>环比: <span style='color: {rate_color};'><strong>{rate_sign} {abs(energy_info['环比'])}%</strong></span></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 异常预警数
        st.markdown("### 异常预警")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style='background-color: #fff3cd; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
                <h5 style='margin: 0 0 10px 0; color: #856404;'>异常数量</h5>
                <p style='margin: 0; font-size: 24px; font-weight: bold; color: #856404;'>12</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background-color: #f8d7da; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
                <h5 style='margin: 0 0 10px 0; color: #721c24;'>疑似违规用电</h5>
                <p style='margin: 0; font-size: 24px; font-weight: bold; color: #721c24;'>5</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style='background-color: #fff3e0; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
                <h5 style='margin: 0 0 10px 0; color: #e65100;'>未打卡数量</h5>
                <p style='margin: 0; font-size: 24px; font-weight: bold; color: #e65100;'>8</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 学生列表
        student_data = {
            '学号': ['20230101', '20230102', '20230103', '20230104', '20230105', '20230201', '20230202', '20230301'],
            '姓名': ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十'],
            '班级': ['23级财务管理01班', '23级财务管理01班', '23级财务管理02班', '23级财务管理02班', '23级财务管理01班', '23级会计01班', '23级会计02班', '23级审计01班'],
            '宿舍': ['1号楼101', '1号楼102', '2号楼201', '2号楼202', '1号楼103', '3号楼301', '3号楼302', '4号楼401'],
            '积分': [850, 780, 920, 650, 720, 800, 750, 820]
        }
        df_students = pd.DataFrame(student_data)
        
        # 按专业和班级筛选
        if majors:
            # 筛选包含任何选中专业的班级
            df_students = df_students[df_students['班级'].apply(lambda x: any(major in x for major in majors))]
        if class_names:
            # 筛选包含任何选中班级的班级
            df_students = df_students[df_students['班级'].apply(lambda x: any(class_name in x for class_name in class_names))]
        
        # 排序功能
        if 'sort_order' not in st.session_state:
            st.session_state.sort_order = 'desc'
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### 积分排名")
        with col2:
            if st.button("🔄 切换排序" if st.session_state.sort_order == 'desc' else "🔄 切换排序"):
                st.session_state.sort_order = 'asc' if st.session_state.sort_order == 'desc' else 'desc'
                st.rerun()
        
        # 按积分排序
        df_students = df_students.sort_values('积分', ascending=(st.session_state.sort_order == 'asc'))
        # 添加排名列
        df_students.insert(0, '排名', range(1, len(df_students) + 1))
        
        st.dataframe(df_students, use_container_width=True)
    
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
        
        # 统计卡片
        st.markdown("### 打卡统计")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
                <h5 style='margin: 0 0 10px 0; color: #1a1a1a;'>总打卡数</h5>
                <p style='margin: 0; font-size: 24px; font-weight: bold; color: #1890ff;'>125</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
                <h5 style='margin: 0 0 10px 0; color: #1a1a1a;'>达标率</h5>
                <p style='margin: 0; font-size: 24px; font-weight: bold; color: #52c41a;'>85%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
                <h5 style='margin: 0 0 10px 0; color: #1a1a1a;'>总积分</h5>
                <p style='margin: 0; font-size: 24px; font-weight: bold; color: #faad14;'>1250</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 学生打卡明细和详情
        col1, col2 = st.columns(2)
        
        with col1:
            # 学生打卡明细
            st.markdown("### 学生打卡明细")
            checkin_records = {
                '日期': ['2024-01-16', '2024-01-16', '2024-01-16', '2024-01-15', '2024-01-15'],
                '学生': ['张三', '李四', '王五', '张三', '李四'],
                '宿舍': ['1号楼101', '1号楼102', '2号楼201', '1号楼101', '1号楼102'],
                '行为': ['节能打卡', '关灯节能', '关空调节能', '节能打卡', '关水龙头'],
                '积分': [10, 10, 10, 10, 10]
            }
            df_checkin_records = pd.DataFrame(checkin_records)
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
        
        with col2:
            # 打卡详情
            st.markdown("### 打卡详情")
            
            # 模拟打卡详情数据
            checkin_details = {
                '打卡类型': ['节能打卡', '关灯节能', '关空调节能', '关水龙头', '关电脑'],
                '积分奖励': [10, 10, 15, 5, 8],
                '参与人数': [45, 38, 25, 42, 30],
                '达标要求': ['每日1次', '每日1次', '每日1次', '每日2次', '每日1次']
            }
            df_checkin_details = pd.DataFrame(checkin_details)
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
            
            # 生成模拟数据
            dates = pd.date_range('2026-04-01', '2026-04-11').strftime('%m-%d')
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
            
            # 生成模拟数据
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
        
        # 筛选功能
        st.markdown("### 筛选条件")
        col1, col2 = st.columns(2)
        with col1:
            date_range = st.date_input("选择日期范围", value=(pd.to_datetime('2024-01-10'), pd.to_datetime('2024-01-16')), min_value=pd.to_datetime('2024-01-01'), max_value=pd.to_datetime('2024-01-31'))
        with col2:
            dorm_filter = st.multiselect("选择宿舍", ["1号楼101", "1号楼102", "1号楼103", "2号楼201", "2号楼202", "3号楼301", "3号楼302", "4号楼401"])
        
        # 模拟申诉数据
        if 'appeals' not in st.session_state:
            st.session_state.appeals = [
                {'日期': '2024-01-16', '学生': '张三', '宿舍': '1号楼101', '耗电异常值': '5.2 kWh', '状态': '待处理'},
                {'日期': '2024-01-16', '学生': '李四', '宿舍': '1号楼102', '耗电异常值': '4.8 kWh', '状态': '待处理'},
                {'日期': '2024-01-15', '学生': '王五', '宿舍': '2号楼201', '耗电异常值': '6.1 kWh', '状态': '待处理'},
                {'日期': '2024-01-15', '学生': '赵六', '宿舍': '2号楼202', '耗电异常值': '3.9 kWh', '状态': '已通过'},
                {'日期': '2024-01-14', '学生': '钱七', '宿舍': '3号楼301', '耗电异常值': '4.5 kWh', '状态': '已驳回'}
            ]
        
        # 筛选数据
        filtered_appeals = st.session_state.appeals
        if dorm_filter:
            filtered_appeals = [appeal for appeal in filtered_appeals if appeal['宿舍'] in dorm_filter]
        
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
                        st.session_state.appeals[original_index]['状态'] = '已通过'
                        st.success("申诉已通过！")
                        st.rerun()
                with col2:
                    if st.button("驳回申诉", type="secondary"):
                        st.session_state.appeals[original_index]['状态'] = '已驳回'
                        st.success("申诉已驳回！")
                        st.rerun()
        else:
            st.markdown("暂无申诉记录")
        
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
                
                # 模拟账号身份判断
                if user_id == "admin":
                    # 管理者登录
                    st.session_state.logged_in = True
                    st.session_state.user_position = "管理者"  # 管理者使用专门的管理端页面
                    st.session_state.username = user_id
                    st.session_state.user_name = "管理员"  # 简化处理，实际应该从数据库获取
                    st.rerun()
                elif user_id == "zhangshan":
                    # 学生登录
                    st.session_state.logged_in = True
                    st.session_state.user_position = "学生"
                    st.session_state.username = user_id
                    st.session_state.user_name = "张三"  # 简化处理，实际应该从数据库获取
                    st.session_state.dormitory = "1号楼101"  # 模拟宿舍
                    st.rerun()
                elif user_id in ["wang", "deng"]:
                    # 老师登录
                    st.session_state.logged_in = True
                    st.session_state.user_position = "老师"
                    st.session_state.username = user_id
                    st.session_state.user_name = "王老师" if user_id == "wang" else "邓老师"  # 简化处理，实际应该从数据库获取
                    st.rerun()
                else:
                    # 默认学生登录
                    st.session_state.logged_in = True
                    st.session_state.user_position = "学生"
                    st.session_state.username = user_id
                    st.session_state.user_name = user_id  # 简化处理，实际应该从数据库获取
                    st.session_state.dormitory = "1号楼101"  # 模拟宿舍
                    st.rerun()
        
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
        elif st.session_state.user_position == "老师":
            teacher_page()
        elif st.session_state.user_position == "管理者":
            admin_page()