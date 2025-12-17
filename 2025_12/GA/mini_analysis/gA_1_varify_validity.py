import pandas as pd

# CSVの読み込み
CSV_FILE = "/Users/mizuki/team_discussion/2025_12/analysis_csv/analysis_csv_gA_1.csv"
df = pd.read_csv(CSV_FILE)

# --- 人手によるラベル付け (あなたの判断) ---
# D: Divergence (発散・アイデア出し・話題転換)
# C: Convergence (収束・まとめ・決定・合意)
# O: Other (雑談・事務連絡・準備・脱線)

# ログに基づいた推奨ラベル設定:
manual_labels = [
    'O', # Seg 1: [準備] 見る、聞こえる
    'D', # Seg 2: [発散] テーマ選定、大雑把
    'D', # Seg 3: [発散] 農業、つながる話題
    'D', # Seg 4: [発散] 地域、統一、生活
    'D', # Seg 5: [発散] 作る、それぞれ
    'O', # Seg 6: [事務] Slack、Notion、書く
    'C', # Seg 7: [収束] IT、地域、決定
    'D', # Seg 8: [発散] 壮大すぎる、社会
    'D', # Seg 9: [発散] サービス開発、支援
    'D', # Seg 10: [発散] 教育、学校生活
    'D', # Seg 11: [発散] 過疎、学校
    'D', # Seg 12: [発散] AI、送る、技術
    'C', # Seg 13: [収束] 地域課題、問題定義
    'D', # Seg 14: [発散] ITを入れる、範囲
    'D', # Seg 15: [発散] 前提定義、言葉
    'O', # Seg 16: [脱線] 思い出、英語、パソコン
    'O', # Seg 17: [脱線] 地域定義、千葉、論外
    'D', # Seg 18: [発散] 人数、学年、難しい
    'C', # Seg 19: [収束] 考えるベース、一般化
    'C'  # Seg 20: [収束] 活用、できる、終了
]

# ラベルをデータに追加
df['Label'] = manual_labels

# --- 検証：ラベルごとのスコア平均を出す ---
# 「DのときはNoveltyが高い」「CのときはRepresentativenessが高い」はず
summary = df.groupby('Label')[['Novelty', 'Representativeness']].mean()
count = df['Label'].value_counts()

print("--- gA_1_検証結果（論文の3.3に記載する数値） ---")
print(summary)
print("\n--- 各ラベルのデータ数 ---")
print(count)

# 詳細確認用（保存）
df.to_csv("/Users/mizuki/team_discussion/2025_12/GA/mini_analysis/gA_1_validation_result.csv", index=False)