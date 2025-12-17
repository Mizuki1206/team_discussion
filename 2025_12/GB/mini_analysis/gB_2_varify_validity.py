import pandas as pd

# CSVの読み込み (ファイル名をgB_2用に変更)
CSV_FILE = "/Users/mizuki/team_discussion/2025_12/analysis_csv/analysis_csv_gB_2.csv"
df = pd.read_csv(CSV_FILE)

# --- 人手によるラベル付け (あなたの判断) ---
# D: Divergence (発散・アイデア出し・事例列挙・要因探索)
# C: Convergence (収束・まとめ・決定・合意)
# O: Other (雑談・事務連絡・準備・脱線)

# ログ(meeting_log_gB_2.txt)に基づいた推奨ラベル設定:
manual_labels = [
    'O', # Seg 1: [その他] マイク、お願い
    'D', # Seg 2: [発散] 髪型、やばい
    'D', # Seg 3: [発散] ツーブロック、普通
    'D', # Seg 4: [発散] バス、場所
    'D', # Seg 5: [発散] 核心、大学
    'C', # Seg 6: [収束] ブランディング、結果
    'D', # Seg 7: [発散] 自己、禁止
    'D', # Seg 8: [発散] 全部
    'D', # Seg 9: [発散] 先生、考え
    'D', # Seg 10: [発散] 歴史、校則
    'D', # Seg 11: [発散] 指定
    'D', # Seg 12: [発散] 式典、靴下
    'C', # Seg 13: [収束] 評判、評価、Google
    'C', # Seg 14: [収束] ブランド
    'D', # Seg 15: [発散] 意外、集める
    'D', # Seg 16: [発散] 憲法、決まる
    'D', # Seg 17: [発散] 選挙、生徒
    'D', # Seg 18: [発散] 学期、目安
    'D', # Seg 19: [発散] 権力、大丈夫
    'O'  # Seg 20: [その他] 終了、やる
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

print("--- gB_2_検証結果（論文の3.3に記載する数値） ---")
print(summary)
print("\n--- 各ラベルのデータ数 ---")
print(count)

# 保存 (ファイル名をgB_2用に変更)
df.to_csv("/Users/mizuki/team_discussion/2025_12/GB/mini_analysis/gB_2_validation_result.csv", index=False)