import pandas as pd
import streamlit as st

# ページの設定
st.set_page_config(
    page_title="DIAF_OUNA_ANALYSER", page_icon="🎰", layout="centered"
)

# Teenage Engineering風デザインのCSS適用
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
</style>
""",
    unsafe_allow_html=True,
)

st.markdown("### // SYSTEM: DIAF_OUNA_ANALYSER")
st.markdown(
    '<div class="te-header">ジアス大船 特設データ解析ダッシュボード</div>',
    unsafe_allow_html=True,
)

# サンプルデータ（複数台のデータ）
data = {
    "台番": [
        501,
        502,
        503,
        504,
        505,
        511,
        512,
        513,
        521,
        522,
        523,
        601,
        602,
        603,
        604,
        611,
        612,
        613,
        621,
        622,
        623,
        631,
        632,
        633,
        641,
        642,
        643,
    ],
    "カテゴリ": [
        "Aタイプ",
        "Aタイプ",
        "Aタイプ",
        "Aタイプ",
        "Aタイプ",
        "Aタイプ",
        "Aタイプ",
        "Aタイプ",
        "Aタイプ",
        "Aタイプ",
        "Aタイプ",
        "スマスロ",
        "スマスロ",
        "スマスロ",
        "スマスロ",
        "スマスロ",
        "スマスロ",
        "スマスロ",
        "スマスロ",
        "スマスロ",
        "スマスロ",
        "スマスロ",
        "スマスロ",
        "スマスロ",
        "スマスロ",
        "スマスロ",
        "スマスロ",
    ],
    "機種名": [
        "マイジャグラーV",
        "マイジャグラーV",
        "マイジャグラーV",
        "マイジャグラーV",
        "マイジャグラーV",
        "ゴーゴージャグラー3",
        "ゴーゴージャグラー3",
        "ゴーゴージャグラー3",
        "ファンキージャグラー2",
        "ファンキージャグラー2",
        "ファンキージャグラー2",
        "甲鉄城のカバネリ海門決戦",
        "甲鉄城のカバネリ海門決戦",
        "甲鉄城のカバネリ海門決戦",
        "甲鉄城のカバネリ海門決戦",
        "東京喰種",
        "東京喰種",
        "東京喰種",
        "ゴッドイーター",
        "ゴッドイーター",
        "ゴッドイーター",
        "ヴァルヴレイヴ2",
        "ヴァルヴレイヴ2",
        "ヴァルヴレイヴ2",
        "Lゴジラ対エヴァンゲリオン 2S",
        "Lゴジラ対エヴァンゲリオン 2S",
        "Lゴジラ対エヴァンゲリオン 2S",
    ],
    "総回転数": [
        8400,
        6200,
        7500,
        4300,
        9100,
        7100,
        5200,
        8300,
        8900,
        5100,
        7800,
        9200,
        4800,
        7800,
        8600,
        4500,
        6700,
        3100,
        7900,
        8500,
        6200,
        8600,
        9400,
        5300,
        6900,
        9100,
        4200,
    ],
    "差枚数": [
        3100,
        -800,
        1600,
        -1400,
        4200,
        1800,
        -1100,
        2600,
        3800,
        -1200,
        1500,
        4500,
        -1900,
        2400,
        5200,
        -1500,
        800,
        -2200,
        2100,
        3900,
        -500,
        5200,
        6100,
        -1800,
        -400,
        4100,
        -2300,
    ],
    "BB/RB": [
        "40/36",
        "22/20",
        "31/27",
        "18/15",
        "44/39",
        "32/29",
        "20/18",
        "38/33",
        "45/38",
        "19/18",
        "33/28",
        "AT 35回",
        "AT 6回",
        "AT 22回",
        "AT 42回",
        "AT 5回",
        "AT 12回",
        "AT 3回",
        "AT 19回",
        "AT 31回",
        "AT 9回",
        "AT 40回",
        "AT 48回",
        "AT 11回",
        "AT 11回",
        "AT 36回",
        "AT 4回",
    ],
}

df = pd.DataFrame(data)

# セレクトボックス
col1, col2 = st.columns(2)
with col1:
    cat_select = st.selectbox(
        "CAT", ["すべて"] + list(df["カテゴリ"].unique())
    )

with col2:
    if cat_select != "すべて":
        available_machines = list(
            df[df["カテゴリ"] == cat_select]["機種名"].unique()
        )
    else:
        available_machines = list(df["機種名"].unique())
    mach_select = st.selectbox("MODEL", ["すべて"] + available_machines)

# フィルタリング
filtered_df = df.copy()
if cat_select != "すべて":
    filtered_df = filtered_df[filtered_df["カテゴリ"] == cat_select]
if mach_select != "すべて":
    filtered_df = filtered_df[filtered_df["機種名"] == mach_select]

st.markdown(
    f"<p style='color: #ff6600;'>// 該当台数: {len(filtered_df)} 台</p>",
    unsafe_allow_html=True,
)

# テーブルを確実に表示するシンプルな描画
if not filtered_df.empty:
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
else:
    st.info("データがありません。")
