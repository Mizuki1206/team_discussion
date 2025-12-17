import pandas as pd

# CSVの読み込み (gC_3)
CSV_FILE = "/Users/mizuki/team_discussion/2025_12/analysis_csv/analysis_csv_gC_3.csv"
df = pd.read_csv(CSV_FILE)

# --- 人手によるラベル付け (gC_3 / 20セグメント版) ---
# D: Divergence (発散), C: Convergence (収束), O: Other (その他)

manual_labels = [
    'D', # Seg 1: [発散] クラスごとのルール作りというアイデア
    'D', # Seg 2: [発散] 生徒同士で決める、対立の懸念
    'D', # Seg 3: [発散] クラス間の不公平、ルールの違い
    'D', # Seg 4: [発散] 連帯責任、不具合の懸念
    'D', # Seg 5: [発散] 日本国憲法をベースにするというアイデア
    'D', # Seg 6: [発散] 憲法だと広すぎる、表現の自由
    'D', # Seg 7: [発散] 生徒を守るための校則、近隣苦情
    'D', # Seg 8: [発散] バイト禁止、寄り道禁止の是非
    'D', # Seg 9: [発散] 校則がない学校、悪い学校の例
    'D', # Seg 10: [発散] 成功事例の共有（生徒会が変えた話）
    'D', # Seg 11: [発散] 先生の権力構造、髪染め禁止
    'D', # Seg 12: [発散] 署名活動、外堀を埋める
    'C', # Seg 13: [収束] 「複数人を巻き込む場を作る」という解決策への合意
    'D', # Seg 14: [発散] ハードルの低いものから変える（靴下など）
    'C', # Seg 15: [収束] PTAや地域住民を入れる会議体の提案
    'D', # Seg 16: [発散] 会議の頻度、プレゼン形式
    'C', # Seg 17: [収束] 他校や教育委員会への提案活動
    'D', # Seg 18: [発散] 地域ごとの特色、マニュアル化
    'O', # Seg 19: [その他] 時間確認、終わり？
    'C'  # Seg 20: [収束] 最終確認、次回への接続
]

# ラベルをデータに追加
df['Label'] = manual_labels

# 検証と保存
summary = df.groupby('Label')[['Novelty', 'Representativeness']].mean()
print("--- 検証結果（gC_3） ---")
print(summary)
df.to_csv("/Users/mizuki/team_discussion/2025_12/GC/mini_analysis/gC_3_validation_result.csv", index=False)