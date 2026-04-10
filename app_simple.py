import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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
        
        # 功能分类 - 能耗管理
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            <div style='margin-top: 20px;'>
                <h4 style='margin: 0 0 10px 0; display: flex; align-items: center;'>
                    <span style='color: #52c41a; margin-right: 8px;'>💡</span>
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
            if st.button("寝室能耗", use_container_width=True):
                st.session_state.selected_page = "寝室能耗"
                st.rerun()
            if st.button("耗能排名", use_container_width=True):
                st.session_state.selected_page = "耗能排名"
                st.rerun()
            if st.button("异常打卡申诉", use_container_width=True):
                st.session_state.selected_page = "异常打卡申诉"
                st.rerun()
        
        # 功能分类 - 节能行动
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            <div style='margin-top: 20px;'>
                <h4 style='margin: 0 0 10px 0; display: flex; align-items: center;'>
                    <span style='color: #faad14; margin-right: 8px;'>🌱</span>
                    节能行动
                </h4>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("▼" if st.session_state.energy_action_expanded else "▶", key="energy_action_toggle", use_container_width=True):
                st.session_state.energy_action_expanded = not st.session_state.energy_action_expanded
                st.rerun()
        
        # 节能行动功能
        if st.session_state.energy_action_expanded:
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
                        '行为': '节能打卡'  # 默认行为
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
                # 检查今日打卡状态
                today = '2024-01-16'  # 模拟今天日期
                is_checked_in = st.session_state.last_checkin_date == today
                
                if not is_checked_in:
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
                    
                    # 更新打卡状态
                    st.session_state.last_checkin_date = today
                    st.session_state.checkin_streak += 1
                    
                    st.success("打卡成功！获得10积分奖励！")
                    st.balloons()
                else:
                    st.info("今日已打卡，请勿重复打卡")
        
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
    st.title("📊 能碳管理平台 (AcrelEMS-EDU)")
    st.markdown("## 屏统管水、电、气、热，AI实时分析 + 碳排放可视化，哪里浪费一目了然！")
    
    st.markdown("---")
    
    # 功能亮点
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown("""
        <div style='background-color: #f0f8ff; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
            <div style='font-size: 24px; margin-bottom: 12px;'>💡 智能节能调控</div>
            <p style='margin: 0; line-height: 1.5;'>空调、照明、水泵全部智能联动，人走灯灭、按需供能，告别无效耗电！</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color: #f0f8ff; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
            <div style='font-size: 24px; margin-bottom: 12px;'>🌍 碳积分小程序</div>
            <p style='margin: 0; line-height: 1.5;'>宿舍用电数据变碳积分，可换学分、餐券、奖品！学生主动节能，氛围拉满！</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background-color: #f0f8ff; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
            <div style='font-size: 24px; margin-bottom: 12px;'>🤖 AI实时分析</div>
            <p style='margin: 0; line-height: 1.5;'>智能识别能耗异常，自动生成节能建议，让节能变得简单高效！</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    with st.sidebar:
        st.header("系统导航")
        page = st.radio(
            "选择功能模块",
            ["首页概览", "能耗监测", "智能调控", "碳积分系统", "数据接口"],
            label_visibility="collapsed"
        )
        
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
    
    if page == "首页概览":
        st.header("📊 系统概览")
        
        # 水、电、气、热综合监测指标
        st.subheader("🌊💡🔥 水电气热综合监测")
        col_water, col_electricity, col_gas, col_heat = st.columns(4, gap="medium")
        
        with col_water:
            st.markdown("""
            <div style='background-color: #e6f7ff; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #1890ff; font-size: 18px;'>水耗</h4>
                <p style='margin: 0 0 8px 0; font-size: 28px; font-weight: bold;'>125.6</p>
                <p style='margin: 0 0 12px 0; font-size: 14px; color: #666;'>吨</p>
                <div style='background-color: #4CAF50; color: white; font-size: 16px; font-weight: bold; padding: 6px 12px; border-radius: 6px; display: inline-block;'>↓ 2.8%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_electricity:
            st.markdown("""
            <div style='background-color: #fff7e6; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #fa8c16; font-size: 18px;'>电耗</h4>
                <p style='margin: 0 0 8px 0; font-size: 28px; font-weight: bold;'>12,580</p>
                <p style='margin: 0 0 12px 0; font-size: 14px; color: #666;'>kWh</p>
                <div style='background-color: #4CAF50; color: white; font-size: 16px; font-weight: bold; padding: 6px 12px; border-radius: 6px; display: inline-block;'>↓ 3.2%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_gas:
            st.markdown("""
            <div style='background-color: #f6ffed; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #52c41a; font-size: 18px;'>气耗</h4>
                <p style='margin: 0 0 8px 0; font-size: 28px; font-weight: bold;'>85.2</p>
                <p style='margin: 0 0 12px 0; font-size: 14px; color: #666;'>m³</p>
                <div style='background-color: #4CAF50; color: white; font-size: 16px; font-weight: bold; padding: 6px 12px; border-radius: 6px; display: inline-block;'>↓ 1.5%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_heat:
            st.markdown("""
            <div style='background-color: #fff1f0; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #f5222d; font-size: 18px;'>热耗</h4>
                <p style='margin: 0 0 8px 0; font-size: 28px; font-weight: bold;'>45.8</p>
                <p style='margin: 0 0 12px 0; font-size: 14px; color: #666;'>GJ</p>
                <div style='background-color: #4CAF50; color: white; font-size: 16px; font-weight: bold; padding: 6px 12px; border-radius: 6px; display: inline-block;'>↓ 2.1%</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 原有指标卡片
        col1, col2, col3, col4 = st.columns(4, gap="medium")
        
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
                <h4 style='margin: 0 0 12px 0; color: #333; font-size: 16px;'>本月累计</h4>
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
        
        with col4:
            st.markdown("""
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 12px 0; color: #333; font-size: 16px;'>碳排放量</h4>
                <p style='margin: 0 0 12px 0; font-size: 28px; font-weight: bold;'>156.8</p>
                <div style='background-color: #4CAF50; color: white; font-size: 16px; font-weight: bold; padding: 6px 12px; border-radius: 6px; display: inline-block;'>↓ 12.3%</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 能耗趋势分析
        st.subheader("📈 能耗趋势分析")
        
        # 能耗趋势图
        energy_trend = {
            '日期': ['1月1日', '1月2日', '1月3日', '1月4日', '1月5日', '1月6日', '1月7日'],
            '能耗值': [1250, 1180, 1120, 1080, 1050, 1020, 980]
        }
        df_energy = pd.DataFrame(energy_trend)
        
        fig_energy = go.Figure()
        fig_energy.add_trace(go.Scatter(x=df_energy['日期'], y=df_energy['能耗值'], mode='lines+markers', name='能耗值'))
        fig_energy.update_layout(
            title="本周能耗趋势",
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
    
    elif page == "能耗监测":
        st.header("📊 能耗监测中心")
        
        # 能耗总览
        st.subheader("📈 能耗总览")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("今日能耗", "12,580 kWh", "↓ 3.2%")
        
        with col2:
            st.metric("本周能耗", "85,420 kWh", "↓ 5.8%")
        
        with col3:
            st.metric("本月能耗", "358,420 kWh", "↓ 7.2%")
        
        st.markdown("---")
        
        # 区域能耗排名
        st.subheader("🏢 区域能耗排名")
        
        area_energy = {
            '排名': [1, 2, 3, 4, 5, 6],
            '区域': ['宿舍区', '食堂', '图书馆', '教学楼A', '教学楼B', '行政楼'],
            '能耗 (kWh)': [4200, 3100, 2400, 2100, 1850, 1080],
            '节能率': [15, 12, 18, 10, 8, 5]
        }
        df_area = pd.DataFrame(area_energy)
        st.dataframe(df_area, use_container_width=True, hide_index=True)
    
    elif page == "智能调控":
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
    
    elif page == "碳积分系统":
        st.header("🌍 碳积分系统")
        
        st.markdown("""
        宿舍用电数据变碳积分，可换学分、餐券、奖品！学生主动节能，氛围拉满！
        """)
        
        # 碳积分统计
        st.subheader("📊 碳积分统计")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("总积分", "125,680", "↑ 8.5%")
        
        with col2:
            st.metric("本月发放", "12,450", "↑ 12.3%")
        
        with col3:
            st.metric("参与学生", "1,240", "↑ 5.2%")
        
        with col4:
            st.metric("兑换次数", "358", "↑ 15.8%")
    
    elif page == "数据接口":
        st.header("🔌 能耗数据接口")
        
        st.markdown("""
        数据导入与导出功能，支持能耗数据的批量管理
        """)
        
        st.markdown("---")
        
        # 能耗数据导出
        st.subheader("📤 能耗数据导出")
        
        export_type = st.selectbox("选择导出类型", ["能耗数据", "节能打卡记录", "积分表", "用户管理"])
        
        if export_type == "能耗数据":
            # 模拟能耗数据
            energy_export_data = {
                '日期': ['2024-01-10', '2024-01-11', '2024-01-12', '2024-01-13', '2024-01-14', '2024-01-15'],
                '区域': ['教学楼A', '教学楼B', '图书馆', '食堂', '宿舍区', '行政楼'],
                '电力 (kWh)': [2100, 1850, 2400, 3100, 4200, 1080],
                '水耗 (吨)': [500, 450, 600, 800, 1100, 280],
                '燃气 (m³)': [200, 150, 200, 200, 300, 70],
                '热耗 (GJ)': [15.2, 12.8, 18.5, 22.3, 28.6, 8.9]
            }
            df_energy_export = pd.DataFrame(energy_export_data)
            st.dataframe(df_energy_export, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # 能耗数据导入
        st.subheader("📥 能耗数据导入")
        
        uploaded_file = st.file_uploader("选择CSV文件上传", type="csv")
        if uploaded_file is not None:
            # 读取上传的文件
            df_uploaded = pd.read_csv(uploaded_file)
            st.dataframe(df_uploaded, use_container_width=True)
            
            if st.button("导入数据", type="primary"):
                st.success("数据导入成功！")
                st.balloons()

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
        
        # 功能分类 - 概览管理
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            <div style='margin-top: 20px;'>
                <h4 style='margin: 0 0 10px 0; display: flex; align-items: center;'>
                    <span style='color: #1890ff; margin-right: 8px;'>📊</span>
                    概览管理
                </h4>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("▼" if st.session_state.overview_management_expanded else "▶", key="overview_management_toggle", use_container_width=True):
                st.session_state.overview_management_expanded = not st.session_state.overview_management_expanded
                st.rerun()
        
        # 概览管理功能
        if st.session_state.overview_management_expanded:
            if st.button("首页", use_container_width=True):
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
        # 顶部数据概览
        st.subheader("📊 数据概览")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div style='background-color: #e8f5e8; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 8px 0; color: #2e7d32;'>总学生数</h4>
                <p style='margin: 0; font-size: 24px; font-weight: bold;'>240</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background-color: #e3f2fd; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 8px 0; color: #1565c0;'>今日打卡率</h4>
                <p style='margin: 0; font-size: 24px; font-weight: bold;'>85%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style='background-color: #fff3e0; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 8px 0; color: #ef6c00;'>平均能耗</h4>
                <p style='margin: 0; font-size: 24px; font-weight: bold;'>3.2 kWh</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style='background-color: #f3e5f5; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h4 style='margin: 0 0 8px 0; color: #7b1fa2;'>总积分</h4>
                <p style='margin: 0; font-size: 24px; font-weight: bold;'>12,500</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 能耗趋势图表
        st.subheader("📈 能耗趋势")
        date_range = pd.date_range(start='2024-01-10', end='2024-01-31')
        energy_data = {
            '日期': [d.strftime('%m月%d日') for d in date_range],
            '电量 (kWh)': [5.2, 4.8, 4.5, 4.2, 3.8, 3.5, 3.3, 3.2, 3.0, 2.9, 2.8, 2.7, 2.6, 2.5, 2.4, 2.3, 2.2, 2.1, 2.0, 1.9, 1.8, 1.7],
            '水量 (吨)': [1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.7, 0.6, 0.6, 0.5, 0.5, 0.5, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.1]
        }
        df_energy = pd.DataFrame(energy_data)
        
        fig_energy = go.Figure()
        fig_energy.add_trace(go.Scatter(x=df_energy['日期'], y=df_energy['电量 (kWh)'], mode='lines+markers', name='电量'))
        fig_energy.add_trace(go.Scatter(x=df_energy['日期'], y=df_energy['水量 (吨)'], mode='lines+markers', name='水量'))
        fig_energy.update_layout(
            title="全校能耗趋势",
            xaxis_title="日期",
            yaxis_title="消耗量",
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig_energy, use_container_width=True)
    
    # 学生管理
    elif st.session_state.teacher_selected_page == "学生管理":
        st.subheader("👥 学生管理")
        
        # 学生列表
        student_data = {
            '学号': ['20230101', '20230102', '20230103', '20230104', '20230105'],
            '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
            '班级': ['23级财务管理01班', '23级财务管理01班', '23级财务管理02班', '23级财务管理02班', '23级财务管理01班'],
            '宿舍': ['1号楼101', '1号楼102', '2号楼201', '2号楼202', '1号楼103'],
            '积分': [850, 780, 920, 650, 720]
        }
        df_students = pd.DataFrame(student_data)
        st.dataframe(df_students, use_container_width=True)
    
    # 能耗管理
    elif st.session_state.teacher_selected_page == "能耗管理":
        st.subheader("💡 能耗管理")
        
        # 宿舍能耗排名
        dorm_energy_data = {
            '排名': [1, 2, 3, 4, 5],
            '宿舍': ['3号楼301', '1号楼103', '1号楼101', '2号楼202', '1号楼102'],
            '当日能耗 (kWh)': [2.8, 3.2, 3.5, 3.8, 4.0],
            '节能率': [35, 30, 25, 20, 15]
        }
        df_dorm_energy = pd.DataFrame(dorm_energy_data)
        st.dataframe(df_dorm_energy, use_container_width=True)
    
    # 打卡管理
    elif st.session_state.teacher_selected_page == "打卡管理":
        st.subheader("✅ 打卡管理")
        
        # 打卡记录
        checkin_records = {
            '日期': ['2024-01-16', '2024-01-16', '2024-01-16', '2024-01-15', '2024-01-15'],
            '学生': ['张三', '李四', '王五', '张三', '李四'],
            '宿舍': ['1号楼101', '1号楼102', '2号楼201', '1号楼101', '1号楼102'],
            '行为': ['节能打卡', '关灯节能', '关空调节能', '节能打卡', '关水龙头'],
            '积分': [10, 10, 10, 10, 10]
        }
        df_checkin_records = pd.DataFrame(checkin_records)
        st.dataframe(df_checkin_records, use_container_width=True)
    
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
    
    # 学生耗电异常申诉
    elif st.session_state.teacher_selected_page == "学生耗电异常申诉":
        st.subheader("⚠️ 学生耗电异常申诉")
        
        # 模拟申诉数据（实际应用中应该从数据库获取）
        if 'appeals' not in st.session_state:
            st.session_state.appeals = []
        
        # 显示申诉列表
        if st.session_state.appeals:
            df_appeals = pd.DataFrame(st.session_state.appeals)
            st.dataframe(df_appeals, use_container_width=True)
            
            # 审核功能
            st.markdown("### 审核申诉")
            appeal_index = st.selectbox("选择要审核的申诉", options=range(len(st.session_state.appeals)), format_func=lambda x: f"{st.session_state.appeals[x]['学生']} - {st.session_state.appeals[x]['日期']}")
            
            if appeal_index is not None:
                appeal = st.session_state.appeals[appeal_index]
                st.markdown(f"**学生**: {appeal['学生']}")
                st.markdown(f"**宿舍**: {appeal['宿舍']}")
                st.markdown(f"**日期**: {appeal['日期']}")
                st.markdown(f"**原因**: {appeal['原因']}")
                st.markdown(f"**当前状态**: {appeal['状态']}")
                
                # 审核按钮
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("通过申诉", type="primary"):
                        st.session_state.appeals[appeal_index]['状态'] = '已通过'
                        st.success("申诉已通过！")
                        st.rerun()
                with col2:
                    if st.button("驳回申诉", type="secondary"):
                        st.session_state.appeals[appeal_index]['状态'] = '已驳回'
                        st.success("申诉已驳回！")
                        st.rerun()
        else:
            st.markdown("暂无申诉记录")

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
                "",
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