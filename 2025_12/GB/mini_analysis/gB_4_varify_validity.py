import pandas as pd

# CSVの読み込み (ファイル名をgB_4用に変更)
CSV_FILE = "/Users/mizuki/team_discussion/2025_12/analysis_csv/analysis_csv_gB_4.csv"
df = pd.read_csv(CSV_FILE)

# --- 人手によるラベル付け (あなたの判断) ---
# D: Divergence (発散・アイデア出し・手法の検討・背景確認)
# C: Convergence (収束・まとめ・決定・合意・プロセスの確定)
# O: Other (雑談・事務連絡・準備・機材調整・脱線)

# ログ(meeting_log_gB_4.txt)に基づいた推奨ラベル設定:
manual_labels = [
    'D', # Seg 1: [発散] 実現、会議
    'D', # Seg 2: [発散] 先生、生徒、外部
    'D', # Seg 3: [発散] 問題理解、評価
    'D', # Seg 4: [発散] 暴言、戻す
    'D', # Seg 5: [発散] 段階、代表
    'C', # Seg 6: [収束] まとまる、一致
    'D', # Seg 7: [発散] 地域、電車
    'D', # Seg 8: [発散] 違う、集める
    'D', # Seg 9: [発散] 大人、話し合い
    'D', # Seg 10: [発散] ストライキ、効果
    'D', # Seg 11: [発散] 期間、絶対
    'D', # Seg 12: [発散] 抜き打ち、厳しい
    'D', # Seg 13: [発散] 優しい、やる
    'C', # Seg 14: [収束] 納得、教育
    'C', # Seg 15: [収束] 作る、いける
    'O', # Seg 16: [脱線] 体罰、ノイキャン
    'C', # Seg 17: [収束] 視点、解決
    'D', # Seg 18: [発散] 平成、ブラック
    'D', # Seg 19: [発散] 議論、校内
    'C'  # Seg 20: [収束] 価値、一緒、結論
]

# データ行数とラベル数が合わない場合のエラーハンドリング
if len(df) != len(manual_labels):
    print(f"Warning: CSV rows ({len(df)}) do not match label count ({len(manual_labels)}). Truncating or padding.")
    if len(df) < len(manual_labels):
        manual_labels = manual_labels[:len(df)]
    else:
        manual_labels += ['O'] * (len(df) - len(manual_labels))

# ラベルをデータに追加
df['Label'] = manual_labels

# --- 検証：ラベルごとのスコア平均を出す ---
summary = df.groupby('Label')[['Novelty', 'Representativeness']].mean()
count = df['Label'].value_counts()

print("--- gB_4_検証結果（論文の3.3に記載する数値） ---")
print(summary)
print("\n--- 各ラベルのデータ数 ---")
print(count)

# 保存 (ファイル名をgB_4用に変更)
df.to_csv("/Users/mizuki/team_discussion/2025_12/GB/mini_analysis/gB_4_validation_result.csv", index=False)