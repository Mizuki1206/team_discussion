import pandas as pd

# CSVの読み込み (ファイル名をgB_1用に変更)
CSV_FILE = "/Users/mizuki/team_discussion/2025_12/analysis_csv/analysis_csv_gB_1.csv"
df = pd.read_csv(CSV_FILE)

# --- 人手によるラベル付け (あなたの判断) ---
# D: Divergence (発散・アイデア出し・経験共有・事例列挙)
# C: Convergence (収束・決定・合意・プロセス確定)
# O: Other (雑談・事務連絡・準備・脱線)

# ログ(meeting_log_gB_1.txt)に基づいた推奨ラベル設定:
manual_labels = [
    'O', # Seg 1: [準備] 決める、テーマ、SDGs
    'D', # Seg 2: [発散] やる、興味、置く
    'D', # Seg 3: [発散] 生活、忘れる
    'D', # Seg 4: [発散] メモ、教育
    'D', # Seg 5: [発散] 学校生活、載せる
    'C', # Seg 6: [収束] 方法、決め、テーマ
    'D', # Seg 7: [発散] 高校生、出す
    'D', # Seg 8: [発散] ルート、校則
    'D', # Seg 9: [発散] 指導、見張る
    'D', # Seg 10: [発散] ダメ、ゲーム、厳しすぎ
    'D', # Seg 11: [発散] 刑務所、違う
    'D', # Seg 12: [発散] 変わる、校則、うちの学校
    'D', # Seg 13: [発散] 提出、決まる
    'D', # Seg 14: [発散] ロッカー、メイク
    'D', # Seg 15: [発散] バレる、怒る
    'D', # Seg 16: [発散] 電車、中高一貫
    'D', # Seg 17: [発散] 全員、やばい
    'D', # Seg 18: [発散] クラス、最初
    'D', # Seg 19: [発散] プール、受験
    'C'  # Seg 20: [収束] テーマ確認、リスト
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

print("--- gB_1_検証結果（論文の3.3に記載する数値） ---")
print(summary)
print("\n--- 各ラベルのデータ数 ---")
print(count)

# 保存 (ファイル名をgB_1用に変更)
df.to_csv("/Users/mizuki/team_discussion/2025_12/GB/mini_analysis/gB_1_validation_result.csv", index=False)