import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib  # 日本語表示用ライブラリ

# 1. データの準備
data = [
    ("A-1", 2.06, 0.378),
    ("A-2", 1.91, 0.389),
    ("A-3", 1.99, 0.346),
    ("A-4", 2.09, 0.196),
    ("B-1", 2.17, 0.308),
    ("B-2", 2.57, 0.532), 
    ("B-3", 3.11, 0.397), 
    ("B-4", 2.49, 0.296),
    ("C-1", 2.88, 0.336),
    ("C-2", 3.06, 0.346), 
    ("C-3", 3.31, 0.415), 
    ("C-4", 3.26, 0.387)  
]
df = pd.DataFrame(data, columns=["Session", "Score", "Final_Conv"])

# 2. グループ分け
df["Group"] = df["Score"].apply(lambda x: "高評価群\n(≧3.0)" if x >= 3.0 else "低評価群\n(<3.0)")

# 3. グラフの描画
plt.figure(figsize=(6, 5))

# ---【重要】修正ポイント ---
# set_styleを実行するとフォント設定がリセットされるため、
# その後に必ず日本語フォントを再指定します。
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'IPAexGothic' 
# ------------------------

palette = ["#E0E0E0", "#E0E0E0"]

# 箱ひげ図
ax = sns.boxplot(x="Group", y="Final_Conv", data=df, palette=palette, fliersize=0, width=0.5)

# データ点のプロット
sns.swarmplot(x="Group", y="Final_Conv", data=df, color="#333333", size=8, alpha=0.8)

# ラベルとタイトルの設定
plt.title("高評価群と低評価群における最終収束度の比較", fontsize=14, pad=15)
plt.ylabel("最終収束度 ($S_{final}$)", fontsize=12)
plt.xlabel("グループ（講師評価スコア）", fontsize=12)

plt.tight_layout()
plt.savefig("boxplot_final_convergence.png", dpi=300)
plt.show()

print("グラフを保存しました")