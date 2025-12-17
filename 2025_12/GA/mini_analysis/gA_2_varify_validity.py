import pandas as pd

# CSVの読み込み (ファイル名をgA_2用に変更)
CSV_FILE = "/Users/mizuki/team_discussion/2025_12/analysis_csv/analysis_csv_gA_2.csv"
df = pd.read_csv(CSV_FILE)

# --- 人手によるラベル付け (あなたの判断) ---
# D: Divergence (発散・アイデア出し・話題転換・要因探索)
# C: Convergence (収束・まとめ・決定・合意・定義付け)
# O: Other (雑談・事務連絡・準備・脱線)

# ログ(meeting_log_gA_2.txt)に基づいた推奨ラベル設定:
manual_labels = [
    'D', # Seg 1: [発散] 核心とは、田舎、本質
    'D', # Seg 2: [発散] 時間、予算、難しい
    'D', # Seg 3: [発散] 人員不足、IT
    'D', # Seg 4: [発散] 解決策、予算、全て
    'D', # Seg 5: [発散] 都市と地方、格差
    'D', # Seg 6: [発散] 遠隔授業、都市
    'C', # Seg 7: [収束] 意見を絞る、インフラ
    'D', # Seg 8: [発散] iPad、学校単位
    'D', # Seg 9: [発散] システムを変える、教育
    'D', # Seg 10: [発散] オンライン、実地、科目
    'D', # Seg 11: [発散] ITと先生、教科書
    'D', # Seg 12: [発散] 電子書籍、価格
    'D', # Seg 13: [発散] 先生の責任、学年
    'D', # Seg 14: [発散] 難しい、学校の事情
    'D', # Seg 15: [発散] 教科書、理由
    'D', # Seg 16: [発散] 問題、責任、政治
    'D', # Seg 17: [発散] 学歴、やる気、環境
    'C', # Seg 18: [収束] 国民、核心、問題の特定
    'C', # Seg 19: [収束] 教育意識、問題意識
    'O'  # Seg 20: [その他] 終了、保護
]

# データ行数とラベル数が合わない場合のエラーハンドリング(念のため)
if len(df) != len(manual_labels):
    print(f"Warning: CSV rows ({len(df)}) do not match label count ({len(manual_labels)}). Truncating or padding.")
    # 行数が足りない場合はラベルをカット、多い場合は'O'で埋めるなどの処置
    if len(df) < len(manual_labels):
        manual_labels = manual_labels[:len(df)]
    else:
        manual_labels += ['O'] * (len(df) - len(manual_labels))

# ラベルをデータに追加
df['Label'] = manual_labels

# --- 検証：ラベルごとのスコア平均を出す ---
summary = df.groupby('Label')[['Novelty', 'Representativeness']].mean()
count = df['Label'].value_counts()

print("--- gA_2_検証結果（論文の3.3に記載する数値） ---")
print(summary)
print("\n--- 各ラベルのデータ数 ---")
print(count)

# 保存 (ファイル名をgA_2用に変更)
df.to_csv("/Users/mizuki/team_discussion/2025_12/GA/mini_analysis/gA_2_validation_result.csv", index=False)