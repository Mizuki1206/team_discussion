import pandas as pd

# CSVの読み込み (ファイル名をgA_4用に変更)
CSV_FILE = "/Users/mizuki/team_discussion/2025_12/analysis_csv/analysis_csv_gA_4.csv"
df = pd.read_csv(CSV_FILE)

# --- 人手によるラベル付け (あなたの判断) ---
# D: Divergence (発散・アイデア出し・懸念点の提示・分析)
# C: Convergence (収束・合意形成・決定・詳細詰め)
# O: Other (雑談・事務連絡・準備・脱線)

# ログ(meeting_log_gA_4.txt)に基づいた推奨ラベル設定:
manual_labels = [
    'O', # Seg 1: [その他] ミュート、お願い
    'D', # Seg 2: [発散] 問題、整備、普及
    'O', # Seg 3: [その他] 聞こえる、マイク
    'D', # Seg 4: [発散] 考える、社会、地域
    'D', # Seg 5: [発散] 意識、問題、責任
    'D', # Seg 6: [発散] ステージ、解決、やる
    'C', # Seg 7: [収束] 解決、一番、優先順位
    'D', # Seg 8: [発散] 怪我、担任、責任
    'D', # Seg 9: [発散] 中学校、人数、その他
    'D', # Seg 10: [発散] チューター、AI、人員
    'D', # Seg 11: [発散] 専門、問い合わせ
    'D', # Seg 12: [発散] 世間、納得、方法
    'D', # Seg 13: [発散] 教員、伝える、授業
    'D', # Seg 14: [発散] 将来、実験、データ
    'D', # Seg 15: [発散] 授業、映像、モデル
    'C', # Seg 16: [収束] オンラインモデル、第一歩
    'C', # Seg 17: [収束] 詰める、モデル作成
    'D', # Seg 18: [発散] 都市、横浜、きつい
    'D', # Seg 19: [発散] 公立、国立
    'O'  # Seg 20: [その他] 時間、ジャスト、終了
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

print("--- gA_4_検証結果（論文の3.3に記載する数値） ---")
print(summary)
print("\n--- 各ラベルのデータ数 ---")
print(count)

# 保存 (ファイル名をgA_4用に変更)
df.to_csv("/Users/mizuki/team_discussion/2025_12/GA/mini_analysis/gA_4_validation_result.csv", index=False)