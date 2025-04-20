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

# --- Streamlit UI ---

# データ出典注記
st.caption("Source: National Cancer Center Japan, Cancer Information Service (https://ganjoho.jp/reg_stat/statistics/data/dl/index.html)")
st.title("All-Cancer Age-Adjusted Mortality Rate")

# サイドバーで選択
gender = st.sidebar.selectbox("Select gender", gender_list)
pref = st.sidebar.selectbox("Select prefecture", pref_list)
year = st.sidebar.selectbox("Select year (for comparison)", sorted(years))

# 選択都道府県データ
data_pref = asr_df[(asr_df["都道府県"] == pref) & (asr_df["性別"] == gender)]
data_pref_yearly = data_pref[year_columns].T
data_pref_yearly.columns = ["Prefecture"]

# 全国データ（比較対象）
data_nation = asr_df[(asr_df["都道府県"] == "全国") & (asr_df["性別"] == gender)]
data_nation_yearly = data_nation[year_columns].T
data_nation_yearly.columns = ["Japan"]

# 折れ線グラフ
st.subheader(f"{pref} ({gender}) vs Japan: Age-adjusted Mortality Rate")
fig, ax = plt.subplots()

if pref == "全国":
    ax.plot(data_nation_yearly.index.astype(int), data_nation_yearly["Japan"], label="Japan", color="#E69F00", linewidth=2)
else:
    data_combined = pd.concat([data_pref_yearly.rename(columns={"Prefecture": pref}), data_nation_yearly], axis=1)
    data_combined.index = data_combined.index.astype(int)
    ax.plot(data_combined.index, data_combined["Japan"], label="Japan", color="#999999", linewidth=2)
    ax.plot(data_combined.index, data_combined[pref], label=pref, color="#E69F00", linewidth=2)

ax.set_ylabel("Age-adjusted mortality rate (per 100,000)", fontsize=12)
ax.set_xlabel("Year", fontsize=12)
ax.legend(fontsize=10)
st.pyplot(fig)

# 特定年の都道府県比較（棒グラフ）
st.subheader(f"{year} - Prefecture-level Age-adjusted Mortality Rate ({gender})")
fig2, ax2 = plt.subplots(figsize=(10, 5))
data_year = asr_df[(asr_df["性別"] == gender) & (asr_df["都道府県"] != "全国")][["都道府県", str(year)]]
data_year_sorted = data_year.sort_values(by=str(year), ascending=False)
ax2.bar(range(len(data_year_sorted)), data_year_sorted[str(year)], color="#0072B2")
ax2.set_ylabel("Rate (per 100,000)", fontsize=12)
ax2.set_xlabel("Prefecture", fontsize=12)
ax2.set_xticks(range(len(data_year_sorted)))
ax2.set_xticklabels([str(p) for p in data_year_sorted["都道府県"]], rotation=90, fontsize=8)
st.pyplot(fig2)
