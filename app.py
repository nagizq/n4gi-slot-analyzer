import pandas as pd
import streamlit as st

# ページの設定
st.set_page_config(
    page_title="DIAF_OUNA_ANALYSER", page_icon="🎰", layout="centered"
)

# Teenage Engineering風デザインのCSS
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
    padding: 10px;
    font-size: 13px;
    margin-bottom: 15px;
    color: #ffcc99;
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

# 1. 拡張データ（日付、CZ確率、AT確率、差枚数など）
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
    ],
    "台番": [601, 602, 603, 604, 501, 502, 511, 521],
    "カテゴリ": [
        "スマスロ",
        "スマスロ",
        "スマスロ",
        "スマスロ",
        "Aタイプ",
        "Aタイプ",
        "Aタイプ",
        "Aタイプ",
    ],
    "機種名": [
        "甲鉄城のカバネリ海門決戦",
        "甲鉄城のカバネリ海門決戦",
        "甲鉄城のカバネリ海門決戦",
        "甲鉄城のカバネリ海門決戦",
        "マイジャグラーV",
        "マイジャグラーV",
        "ゴーゴージャグラー3",
        "ファンキージャグラー2",
    ],
    "総回転数": [9200, 4800, 7800, 8600, 8400, 6200, 7100, 8900],
    "差枚数": [4500, -1900, 2400, 5200, 3100, -800, 1800, 3800],
    "CZ確率": [
        "1/112",
        "1/240",
        "1/145",
        "1/108",
        "-",
        "-",
        "-",
        "-",
    ],  # スマスロ用
    "BB/AT確率": [
        "1/280",
        "1/520",
        "1/310",
        "1/265",
        "BB 1/230 / RB 1/250",
        "BB 1/310 / RB 1/340",
        "BB 1/240 / RB 1/270",
        "BB 1/220 / RB 1/260",
    ],
    "設定期待度": ["高設定濃厚🔥", "低設定", "中〜高期待", "高設定濃厚🔥", "高設定濃厚🔥", "低設定", "中期待", "高設定濃厚🔥"],
}

df = pd.DataFrame(data)

# サイドバーや選択UI
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

# 2. 複数台の傾向・クセの表示（トレンド分析）
st.markdown(
    """
<div class="trend-box">
<b>【本日のホール傾向分析】</b><br>
・角台（601番や各シマの端）に高設定が寄る傾向あり。<br>
・カバネリ海門決戦は並びで強い挙動を確認。全体的にベースが高め。
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"<p style='color: #ff6600;'>// 該当台数: {len(filtered_df)} 台</p>",
    unsafe_allow_html=True,
)


# 3. 差枚グラフの簡易テキスト表現（プラスなら📈、マイナスなら📉）
def add_graph_emoji(val):
    if val >= 3000:
        return f"{val:+d}枚 🚀"
    elif val >= 1000:
        return f"{val:+d}枚 📈"
