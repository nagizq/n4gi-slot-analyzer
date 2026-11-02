import pandas as pd
import streamlit as st

# ページの設定
st.set_page_config(
    page_title="DIAF_OUNA_ANALYSER", page_icon="🎰", layout="centered"
)

# Teenage Engineering風デザインのCSS（レトロフューチャー・ガジェット感）
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

.stApp {
    background-color: #1a1a1a;
    color: #e0e0e0;
    font-family: 'Share Tech Mono', monospace;
}

h1, h2, h3 {
    color: #ff6600 !important;
    letter-spacing: 2px;
}

.te-header {
    font-size: 14px;
    letter-spacing: 2px;
    color: #ff6600;
    border-bottom: 1px dashed #444;
    padding-bottom: 8px;
    margin-bottom: 12px;
    text-transform: uppercase;
}

.trend-box {
    background-color: #262626;
    border-left: 4px solid #ff6600;
    padding: 12px;
    font-size: 13px;
    margin-bottom: 15px;
    color: #ffcc99;
    line-height: 1.5;
}

/* 1台ごとのカードデザイン（手書き風・レトロガジェット感） */
.unit-card {
    background-color: #222222;
    border: 1px solid #3d3d3d;
    border-radius: 4px;
    padding: 12px;
    margin-bottom: 10px;
}
.unit-header {
    font-size: 14px;
    color: #ff6600;
    font-weight: bold;
    margin-bottom: 5px;
}
.unit-info {
    font-size: 12px;
    color: #cccccc;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown("### // SYSTEM: DIAF_OUNA_ANALYSER")
st.markdown(
    '<div class="te-header">ジアス大船 特設データ解析ダッシュボード</div>',
    unsafe_allow_html=True,
)

# 1. 複数機種のデータ（スマスロ・Aタイプを網羅）
data = {
    "日付": [
        "2026-11-02",
        "2026-11-02",
        "2026-11-02",
        "2026-11-02",
        "2026-11-02",
        "2026-11-02",
        "2026-11-02",
        "2026-11-02",
        "2026-11-02",
        "2026-11-02",
    ],
    "台番": [
        601,
        602,
        603,
        604,
        611,
        621,
        631,
        501,
        511,
        521,
    ],
    "カテゴリ": [
        "スマスロ",
        "スマスロ",
        "スマスロ",
        "スマスロ",
        "スマスロ",
        "スマスロ",
        "スマスロ",
        "Aタイプ",
        "Aタイプ",
        "Aタイプ",
    ],
    "機種名": [
        "甲鉄城のカバネリ海門決戦",
        "甲鉄城のカバネリ海門決戦",
        "甲鉄城のカバネリ海門決戦",
        "甲鉄城のカバネリ海門決戦",
        "東京喰種",
        "ゴッドイーター",
        "ヴァルヴレイヴ2",
        "マイジャグラーV",
        "ゴーゴージャグラー3",
        "ファンキージャグラー2",
    ],
    "総回転数": [
        9200,
        4800,
        7800,
        8600,
        5400,
        8100,
        8900,
        8400,
        7100,
        8900,
    ],
    "差枚数": [
        4500,
        -1900,
        2400,
        5200,
        -1200,
        3100,
        6100,
        3100,
        1800,
        3800,
    ],
    "強弱判定": ["強 🔥", "弱 💧", "中 ⚡", "強 🔥", "弱 💧", "中 ⚡", "強 🔥", "強 🔥", "中 ⚡", "強 🔥"],
}

df = pd.DataFrame(data)

# 選択UI
col1, col2, col3 = st.columns(3)
with col1:
    date_select = st.selectbox("DATE", ["すべて"] + list(df["日付"].unique()))
with col2:
    cat_select = st.selectbox(
        "CAT", ["すべて"] + list(df["カテゴリ"].unique())
    )
with col3:
    if cat_select != "すべて":
        available_machines = list(
            df[df["カテゴリ"] == cat_select]["機種名"].unique()
        )
    else:
        available_machines = list(df["機種名"].unique())
    mach_select = st.selectbox("MODEL", ["すべて"] + available_machines)

# フィルタリング
filtered_df = df.copy()
if date_select != "すべて":
    filtered_df = filtered_df[filtered_df["日付"] == date_select]
if cat_select != "すべて":
    filtered_df = filtered_df[filtered_df["カテゴリ"] == cat_select]
if mach_select != "すべて":
    filtered_df = filtered_df[filtered_df["機種名"] == mach_select]

# 2. 自動統計データの計算
total_units = len(filtered_df)
if total_units > 0:
    avg_diff = int(filtered_df["差枚数"].mean())
    win_count = len(filtered_df[filtered_df["差枚数"] > 0])
    win_rate = (win_count / total_units) * 100
    max_diff = filtered_df["差枚数"].max()
else:
    avg_diff, win_rate, max_diff = 0, 0, 0

# 統計情報の表示
st.markdown(
    f"""
<div class="trend-box">
<b>【自動統計サマリー】</b><br>
・対象台数: <b>{total_units} 台</b> ｜ 勝率: <b>{win_rate:.1f}%</b><br>
・平均差枚: <b>{avg_diff:+d} 枚</b> ｜ 最高差枚: <b>{max_diff:+d} 枚</b><br>
<hr style="border:0; border-top:1px dashed #444; margin:8px 0;">
<b>【本日のホール傾向分析】</b><br>
・角台（各シマの端）に高設定が寄る傾向あり。<br>
・全体的にベースが高めの配分。
</div>
""",
    unsafe_allow_html=True,
)

# 3. 差枚グラフの描画（Streamlit標準のバーチャート）
if not filtered_df.empty:
    st.markdown(
        "<p style='color: #ff6600; font-size:13px;'>// 差枚数ビジュアライズ</p>",
        unsafe_allow_html=True,
    )
    chart_data = filtered_df.set_index("台番")["差枚数"]
    st.bar_chart(chart_data, color="#ff6600")

    # 4. 1台ごとのカード形式（強弱・詳細）表示
    st.markdown(
        "<p style='color: #ff6600; font-size:13px; margin-top:15px;'>// 1台別 詳細カード</p>",
        unsafe_allow_html=True,
    )

    for _, row in filtered_df.iterrows():
        # 強弱に応じたカラーバリエーション
        badge_color = (
            "#ff9999"
            if "強" in row["強弱判定"]
            else ("#ffeb99" if "中" in row["強弱判定"] else "#99ccff")
        )

        st.markdown(
            f"""
        <div class="unit-card">
            <div class="unit-header">台番: {row["台番"]} [ {row["機種名"]} ]</div>
            <div class="unit-info">
                判定: <span style="color: {badge_color}; font-weight:bold;">{row["強弱判定"]}</span> ｜ 
                回転数: {row["総回転数"]}G ｜ 
                差枚: <b style="color: {'#ff6600' if row['差枚数'] > 0 else '#6699ff'};">{row["差枚数"]:+d}枚</b>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
else:
    st.info("条件に一致するデータがありません。")
