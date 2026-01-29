import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. 页面整体配置 ---
st.set_page_config(
    page_title="ESG 双重重要性矩阵 Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. 自定义 CSS ---
st.markdown("""
    <style>
    .block-container {padding-top: 3.5rem; padding-bottom: 2rem;}
    h1 {font-size: 2.0rem !important;}
    
    /* 底部列表样式 */
    .category-header {
        font-size: 18px; font-weight: bold; margin-bottom: 15px; padding-bottom: 8px;
        display: flex; align-items: center; border-bottom: 2px solid;
    }
    .category-icon {font-size: 24px; margin-right: 10px; font-weight: normal;}
    .topic-item {font-family: "Microsoft YaHei", sans-serif; font-size: 14px; margin-bottom: 8px; display: flex; align-items: center;}
    .topic-id {font-weight: bold; margin-right: 8px; min-width: 30px;}
    .topic-name {color: #555;}
    </style>
    """, unsafe_allow_html=True)

st.title("📊 2024年 ESG 双重重要性议题矩阵")
st.caption("支持动态增删议题 • 自定义气泡配色 • 自定义背景风格")

# --- 3. 数据初始化 ---
if 'df_data' not in st.session_state:
    data = [
        {"ID": "01", "议题名称": "职业健康与安全", "维度": "社会 (S)"},
        {"ID": "02", "议题名称": "产品和服务安全与质量", "维度": "社会 (S)"},
        {"ID": "03", "议题名称": "创新驱动", "维度": "社会 (S)"},
        {"ID": "04", "议题名称": "可持续供应链", "维度": "社会 (S)"},
        {"ID": "05", "议题名称": "知识产权保护", "维度": "社会 (S)"},
        {"ID": "06", "议题名称": "员工权益保障", "维度": "社会 (S)"},
        {"ID": "07", "议题名称": "人力资本管理", "维度": "社会 (S)"},
        {"ID": "08", "议题名称": "客户关系管理", "维度": "社会 (S)"},
        {"ID": "09", "议题名称": "社区贡献与参与", "维度": "社会 (S)"},
        {"ID": "10", "议题名称": "气候变化减缓与适应", "维度": "环境 (E)"},
        {"ID": "11", "议题名称": "能源利用", "维度": "环境 (E)"},
        {"ID": "12", "议题名称": "环境合规管理", "维度": "环境 (E)"},
        {"ID": "13", "议题名称": "废弃物处理", "维度": "环境 (E)"},
        {"ID": "14", "议题名称": "循环经济", "维度": "环境 (E)"},
        {"ID": "15", "议题名称": "水资源利用", "维度": "环境 (E)"},
        {"ID": "16", "议题名称": "生态系统和生物多样性", "维度": "环境 (E)"},
        {"ID": "17", "议题名称": "污染物排放", "维度": "环境 (E)"},
        {"ID": "18", "议题名称": "信息安全与隐私保护", "维度": "治理 (G)"},
        {"ID": "19", "议题名称": "利益相关方沟通", "维度": "治理 (G)"},
        {"ID": "20", "议题名称": "公司治理", "维度": "治理 (G)"},
        {"ID": "21", "议题名称": "风险管理", "维度": "治理 (G)"},
        {"ID": "22", "议题名称": "商业道德", "维度": "治理 (G)"},
    ]
    # 给初始数据随机分数
    import random
    for d in data:
        d['财务重要性'] = round(random.uniform(2, 9.0), 1)
        d['影响重要性'] = round(random.uniform(2, 9.0), 1)
        d['Color'] = "" 
        
    st.session_state.df_data = pd.DataFrame(data)

# --- 4. 侧边栏设置 ---
with st.sidebar:
    st.header("🛠️ 矩阵设置")
    
    # --- 1. 气泡色系 ---
    st.markdown("### 🎨 气泡配色方案")
    theme_options = {
        "GRI 标准 (橙/绿/蓝)": {"社会 (S)": "#FF8C66", "环境 (E)": "#00C49F", "治理 (G)": "#1E90FF"},
        "商务深沉 (红/墨绿/深蓝)": {"社会 (S)": "#D9534F", "环境 (E)": "#2E7D32", "治理 (G)": "#1565C0"},
        "清新马卡龙 (粉/青/紫)": {"社会 (S)": "#FF9AA2", "环境 (E)": "#B5EAD7", "治理 (G)": "#C7CEEA"},
        "高对比度 (黄/绿/紫)": {"社会 (S)": "#F1C40F", "环境 (E)": "#2ECC71", "治理 (G)": "#9B59B6"},
        "灰度单色 (不同深浅灰)": {"社会 (S)": "#95A5A6", "环境 (E)": "#7F8C8D", "治理 (G)": "#34495E"}
    }
    selected_theme_name = st.selectbox("选择议题气泡颜色", list(theme_options.keys()))
    COLOR_MAP = theme_options[selected_theme_name] 
    
    st.markdown("---")
    
    # --- 2. 背景风格 (新增功能) ---
    st.markdown("### 🖼️ 矩阵背景风格")
    bg_theme_options = {
        "GRI 标准绿 (默认)": "0, 150, 100",  # 青绿色
        "商务冷灰 (专业)": "100, 100, 100",   # 中性灰
        "科技静谧蓝 (现代)": "65, 105, 225",  # 皇家蓝
        "暖色活力橙 (警示)": "255, 140, 0",   # 深橙色
        "纯净白板 (打印)": "255, 255, 255"    # 纯白 (边框会保留)
    }
    selected_bg_name = st.selectbox("选择矩阵背景色调", list(bg_theme_options.keys()))
    # 获取选中的 RGB 字符串
    selected_bg_rgb = bg_theme_options[selected_bg_name]

    st.markdown("---")
    
    # --- 3. 阈值设置 ---
    threshold_fin = st.slider("财务重要性阈值 (X轴)", 0.0, 10.0, 5.0, 0.5)
    threshold_imp = st.slider("影响重要性阈值 (Y轴)", 0.0, 10.0, 5.0, 0.5)

# --- 5. 数据编辑区 ---
with st.expander("📝 **议题数据管理 (支持增/删/改)**", expanded=False):
    edited_df = st.data_editor(
        st.session_state.df_data,
        num_rows="dynamic",
        column_config={
            "Color": None, 
            "ID": st.column_config.TextColumn("编号", help="例如: 23"),
            "议题名称": st.column_config.TextColumn("议题名称", required=True),
            "维度": st.column_config.SelectboxColumn(
                "所属维度",
                options=["社会 (S)", "环境 (E)", "治理 (G)"],
                required=True,
                width="medium"
            ),
            "财务重要性": st.column_config.NumberColumn(min_value=0, max_value=10, format="%.1f"),
            "影响重要性": st.column_config.NumberColumn(min_value=0, max_value=10, format="%.1f"),
        },
        width='stretch',
        hide_index=True,
        key="editor"
    )

    # 数据同步：更新颜色
    if not edited_df.empty:
        edited_df['Color'] = edited_df['维度'].map(COLOR_MAP).fillna("#999999")
        st.session_state.df_data = edited_df

# --- 6. 矩阵图绘制 ---
st.markdown("###") 
col_main_chart, _ = st.columns([1, 0.01])

with col_main_chart:
    # 过滤数据
    plot_df = edited_df[
        (edited_df['维度'].notna()) & 
        ~((edited_df['财务重要性'] == 0) & (edited_df['影响重要性'] == 0))
    ]

    fig = go.Figure()
    
    axis_color = "#00AC97" 
    # 使用用户选择的背景色 RGB 值
    base_color = selected_bg_rgb 
    axis_end = 10.5

    # --- 1. 绘制背景分区 (使用选定的 base_color) ---
    # 逻辑：如果是纯白背景，就不显示填充色，只显示网格或空白
    if selected_bg_name == "纯净白板 (打印)":
        # 白板模式：全部透明
        pass 
    else:
        # 其他模式：四个象限不同透明度
        fig.add_shape(type="rect", x0=0, y0=0, x1=threshold_fin, y1=threshold_imp, line=dict(width=0), fillcolor=f"rgba({base_color}, 0.05)", layer="below")
        fig.add_shape(type="rect", x0=0, y0=threshold_imp, x1=threshold_fin, y1=10, line=dict(width=0), fillcolor=f"rgba({base_color}, 0.12)", layer="below")
        fig.add_shape(type="rect", x0=threshold_fin, y0=0, x1=10, y1=threshold_imp, line=dict(width=0), fillcolor=f"rgba({base_color}, 0.12)", layer="below")
        fig.add_shape(type="rect", x0=threshold_fin, y0=threshold_imp, x1=10, y1=10, line=dict(width=0), fillcolor=f"rgba({base_color}, 0.25)", layer="below")

    # --- 2. 轴线 ---
    fig.add_shape(type="line", x0=0, y0=0, x1=axis_end, y1=0, line=dict(color=axis_color, width=2), layer="above")
    fig.add_shape(type="line", x0=0, y0=0, x1=0, y1=axis_end, line=dict(color=axis_color, width=2), layer="above")

    # --- 3. 散点 ---
    for cat in ["社会 (S)", "环境 (E)", "治理 (G)"]:
        df_cat = plot_df[plot_df['维度'] == cat]
        if not df_cat.empty:
            first_color = df_cat['Color'].iloc[0] if pd.notna(df_cat['Color'].iloc[0]) else "#888888"
            
            fig.add_trace(go.Scatter(
                x=df_cat['财务重要性'],
                y=df_cat['影响重要性'],
                mode='markers+text',
                marker=dict(size=18, color=first_color, line=dict(width=1, color='white')),
                text=df_cat['ID'],
                textposition="middle center",
                textfont=dict(color='white', size=10, family="Arial"),
                name=cat,
                hovertemplate="<b>%{customdata}</b><br>财务: %{x}<br>影响: %{y}<extra></extra>",
                customdata=df_cat['议题名称']
            ))

    # --- 4. 箭头 ---
    fig.add_annotation(x=axis_end, y=0, xref="x", yref="y", showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2, arrowcolor=axis_color, ax=-20, ay=0, axref="pixel", ayref="pixel")
    fig.add_annotation(x=0, y=axis_end, xref="x", yref="y", showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2, arrowcolor=axis_color, ax=0, ay=20, axref="pixel", ayref="pixel")

    # --- 5. 布局 ---
    fig.update_layout(
        xaxis=dict(title="<b>财务重要性 (Financial Materiality)</b>", range=[-0.5, 11], showgrid=False, zeroline=False, showline=False, showticklabels=False, title_font=dict(size=14, color=axis_color), title_standoff=10, constrain='domain', side='bottom'),
        yaxis=dict(title="<b>影响重要性 (Impact Materiality)</b>", range=[-0.5, 11], showgrid=False, zeroline=False, showline=False, showticklabels=False, title_font=dict(size=14, color=axis_color), title_standoff=10, scaleanchor="x", scaleratio=1),
        width=800, height=800, plot_bgcolor='white', margin=dict(l=40, r=40, t=20, b=40), showlegend=False
    )
    st.plotly_chart(fig, width='stretch')

# --- 7. 底部列表 ---
st.markdown("---")
col1, col2, col3 = st.columns(3)

def render_category_list(column, category_name, key_keyword, icon, items):
    # 颜色匹配逻辑
    matched_keys = [k for k in COLOR_MAP.keys() if key_keyword in k]
    theme_color = COLOR_MAP[matched_keys[0]] if matched_keys else "#555555"

    if items.empty:
        with column:
             st.markdown(f"""<div class="category-header" style="color: #bbb; border-bottom-color: #eee;">
            <span class="category-icon">{icon}</span> {category_name}维度 (无)</div>""", unsafe_allow_html=True)
        return
    
    with column:
        st.markdown(f"""
        <div class="category-header" style="color: {theme_color}; border-bottom-color: {theme_color};">
            <span class="category-icon">{icon}</span> {category_name}维度议题
        </div>
        """, unsafe_allow_html=True)
        
        html_content = ""
        valid_items = items[items['ID'].notna()].sort_values('ID')
        
        for _, row in valid_items.iterrows():
            row_color = row['Color'] if isinstance(row['Color'], str) else "#999"
            html_content += f"""
            <div class="topic-item">
                <span class="topic-id" style="color: {row_color}">{row['ID']}</span>
                <span class="topic-name">{row['议题名称']}</span>
            </div>
            """
        st.markdown(html_content, unsafe_allow_html=True)

render_category_list(col1, "社会", "社会", "👥", edited_df[edited_df['维度'] == "社会 (S)"])
render_category_list(col2, "环境", "环境", "🌳", edited_df[edited_df['维度'] == "环境 (E)"])
render_category_list(col3, "公司治理", "治理", "🏢", edited_df[edited_df['维度'] == "治理 (G)"])

# --- 8. 底部下载 ---
st.markdown("---")
csv = edited_df.to_csv(index=False).encode('utf-8-sig')

st.download_button("📥 下载分析数据 (CSV)", csv, "Double_Materiality_Matrix.csv", "text/csv")
