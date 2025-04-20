import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CSVの読み込み（同じフォルダ内）
asr_df = pd.read_csv("./asr75.csv", encoding="utf-8")

# 年の列だけ抽出して年リストに変換（int化）
year_columns = [col for col in asr_df.columns if col.isdigit()]
years = list(map(int, year_columns))

# 都道府県と性別の選択肢を取得
pref_list = asr_df["都道府県"].unique()
gender_list = asr_df["性別"].unique()

# 都道府県と性別の表示用変換辞書
pref_map = {
    "北海道": "Hokkaido", "青森": "Aomori", "岩手": "Iwate", "宮城": "Miyagi", "秋田": "Akita",
    "山形": "Yamagata", "福島": "Fukushima", "茨城": "Ibaraki", "栃木": "Tochigi", "群馬": "Gunma",
    "埼玉": "Saitama", "千葉": "Chiba", "東京": "Tokyo", "神奈川": "Kanagawa", "新潟": "Niigata",
    "富山": "Toyama", "石川": "Ishikawa", "福井": "Fukui", "山梨": "Yamanashi", "長野": "Nagano",
    "岐阜": "Gifu", "静岡": "Shizuoka", "愛知": "Aichi", "三重": "Mie", "滋賀": "Shiga",
    "京都": "Kyoto", "大阪": "Osaka", "兵庫": "Hyogo", "奈良": "Nara", "和歌山": "Wakayama",
    "鳥取": "Tottori", "島根": "Shimane", "岡山": "Okayama", "広島": "Hiroshima", "山口": "Yamaguchi",
    "徳島": "Tokushima", "香川": "Kagawa", "愛媛": "Ehime", "高知": "Kochi", "福岡": "Fukuoka",
    "佐賀": "Saga", "長崎": "Nagasaki", "熊本": "Kumamoto", "大分": "Oita", "宮崎": "Miyazaki",
    "鹿児島": "Kagoshima", "沖縄": "Okinawa", "全国": "Japan"
}

gender_map = {"男女計": "Both", "男": "Male", "女": "Female"}

# --- Streamlit UI ---

# データ出典注記
st.caption("Source: National Cancer Center Japan, Cancer Information Service (https://ganjoho.jp/reg_stat/statistics/data/dl/index.html)")
st.title("All-Cancer Age-Adjusted Mortality Rate")

# サイドバーで選択
gender = st.sidebar.selectbox("Select gender", gender_list)
pref = st.sidebar.selectbox("Select prefecture", pref_list)
year = st.sidebar.selectbox("Select year (for comparison)", sorted(years))

display_pref = pref_map.get(pref, pref)
display_gender = gender_map.get(gender, gender)

# 選択都道府県データ
data_pref = asr_df[(asr_df["都道府県"] == pref) & (asr_df["性別"] == gender)]
data_pref_yearly = data_pref[year_columns].T
data_pref_yearly.columns = [display_pref]

# 全国データ（比較対象）
data_nation = asr_df[(asr_df["都道府県"] == "全国") & (asr_df["性別"] == gender)]
data_nation_yearly = data_nation[year_columns].T
data_nation_yearly.columns = ["Japan"]

# 折れ線グラフ
st.subheader(f"{display_pref} ({display_gender}) vs Japan: Age-adjusted Mortality Rate")
fig, ax = plt.subplots()

if pref == "全国":
    ax.plot(data_nation_yearly.index.astype(int), data_nation_yearly["Japan"], label="Japan", color="#E69F00", linewidth=2)
else:
    data_combined = pd.concat([data_pref_yearly, data_nation_yearly], axis=1)
    data_combined.index = data_combined.index.astype(int)
    ax.plot(data_combined.index, data_combined["Japan"], label="Japan", color="#999999", linewidth=2)
    ax.plot(data_combined.index, data_combined[display_pref], label=display_pref, color="#E69F00", linewidth=2)

ax.set_ylabel("Age-adjusted mortality rate (per 100,000)", fontsize=12)
ax.set_xlabel("Year", fontsize=12)
ax.legend(fontsize=10)
st.pyplot(fig)

# 特定年の都道府県比較（棒グラフ）
st.subheader(f"{year} - Prefecture-level Age-adjusted Mortality Rate ({display_gender})")
fig2, ax2 = plt.subplots(figsize=(14, 6))
data_year = asr_df[(asr_df["性別"] == gender) & (asr_df["都道府県"] != "全国")][["都道府県", str(year)]]
data_year["英語県名"] = data_year["都道府県"].map(pref_map)
data_year_sorted = data_year.sort_values(by=str(year), ascending=False)
ax2.bar(range(len(data_year_sorted)), data_year_sorted[str(year)], color="#0072B2")
ax2.set_ylabel("Rate (per 100,000)", fontsize=12)
ax2.set_xlabel("Prefecture", fontsize=12)
ax2.set_xticks(range(len(data_year_sorted)))
ax2.set_xticklabels(data_year_sorted["英語県名"], rotation=60, ha='right', fontsize=10)
st.pyplot(fig2)
