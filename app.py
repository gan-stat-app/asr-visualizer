import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

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
st.caption("出典：国立がん研究センターがん対策情報センター『がん統計』（https://ganjoho.jp/reg_stat/statistics/data/dl/index.html）")
st.title("全がん 年齢調整死亡率")

# サイドバーで選択
gender = st.sidebar.selectbox("性別を選択", gender_list)
pref = st.sidebar.selectbox("都道府県を選択", pref_list)
year = st.sidebar.selectbox("年を選択（都道府県別比較）", sorted(years))

# 選択都道府県データ
data_pref = asr_df[(asr_df["都道府県"] == pref) & (asr_df["性別"] == gender)]
data_pref_yearly = data_pref[year_columns].T
data_pref_yearly.columns = [f"{pref}"]

# 全国データ（比較対象）
data_nation = asr_df[(asr_df["都道府県"] == "全国") & (asr_df["性別"] == gender)]
data_nation_yearly = data_nation[year_columns].T
data_nation_yearly.columns = ["全国"]

# 折れ線グラフ（matplotlibで色指定＋日本語フォント）
st.subheader(f"{pref}（{gender}）と全国の年齢調整死亡率推移")
fig, ax = plt.subplots()

if pref == "全国":
    ax.plot(data_nation_yearly.index.astype(int), data_nation_yearly["全国"], label="全国", color="#E69F00", linewidth=2)
else:
    # 2つを結合
    data_combined = pd.concat([data_pref_yearly, data_nation_yearly], axis=1)
    data_combined.index = data_combined.index.astype(int)
    ax.plot(data_combined.index, data_combined["全国"], label="全国", color="#999999", linewidth=2)
    ax.plot(data_combined.index, data_combined[pref], label=pref, color="#E69F00", linewidth=2)

ax.set_ylabel("年齢調整死亡率（人口10万対）", fontsize=12, family="MS Gothic")
ax.set_xlabel("年（西暦）", fontsize=12, family="MS Gothic")
ax.legend(prop={"family": "MS Gothic", "size": 10})
st.pyplot(fig)

# 特定年の都道府県比較（棒グラフ）
st.subheader(f"{year}年の都道府県別 年齢調整死亡率（{gender}）")
fig2, ax2 = plt.subplots(figsize=(10, 5))
data_year = asr_df[(asr_df["性別"] == gender) & (asr_df["都道府県"] != "全国")][["都道府県", str(year)]]
data_year_sorted = data_year.sort_values(by=str(year), ascending=False)
ax2.bar(data_year_sorted["都道府県"], data_year_sorted[str(year)], color="#0072B2")
ax2.set_ylabel("年齢調整死亡率（人口10万対）", fontsize=12, family="MS Gothic")
ax2.set_xlabel("都道府県", fontsize=12, family="MS Gothic")
ax2.set_xticks(range(len(data_year_sorted["都道府県"])))
ax2.set_xticklabels(data_year_sorted["都道府県"], rotation=90, fontsize=8, family="MS Gothic")
st.pyplot(fig2)
