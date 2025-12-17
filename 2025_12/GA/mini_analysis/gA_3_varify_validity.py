import pandas as pd

# CSVの読み込み (ファイル名をgA_3用に変更)
CSV_FILE = "/Users/mizuki/team_discussion/2025_12/analysis_csv/analysis_csv_gA_3.csv"
df = pd.read_csv(CSV_FILE)

# --- 人手によるラベル付け (あなたの判断) ---
# D: Divergence (発散・アイデア出し・懸念点の提示)
# C: Convergence (収束・合意形成・定義の確定)
# O: Other (雑談・事務連絡・準備・脱線)

# ログ(meeting_log_gA_3.txt)に基づいた推奨ラベル設定:
manual_labels = [
    'O', # Seg 1: [準備] 解決、お願い、オッケー
    'D', # Seg 2: [発散] 具体化、責任、IT
    'D', # Seg 3: [発散] 教師、クラス、IT活用
    'D', # Seg 4: [発散] 先生の負担、減らす
    'D', # Seg 5: [発散] 利益、解決、責任
    'D', # Seg 6: [発散] 重要制度、どちら
    'C', # Seg 7: [収束] 意見がまとまる、核心
    'D', # Seg 8: [発散] 責任、進める
    'D', # Seg 9: [発散] 音楽、私的、分野
    'D', # Seg 10: [発散] 制度、割り切る、むずい
    'D', # Seg 11: [発散] 教育、国民意識、財源
    'D', # Seg 12: [発散] 使い方、分かる
    'D', # Seg 13: [発散] 歴史、AI、研究
    'D', # Seg 14: [発散] 国語、文系、経済
    'D', # Seg 15: [発散] AI、格差、平等
    'D', # Seg 16: [発散] できる、絶対、やつ
    'D', # Seg 17: [発散] 無理、経験、社会
    'D', # Seg 18: [発散] ランク、教員格差
    'D', # Seg 19: [発散] 保健、勉強
    'C'  # Seg 20: [収束] 決める、終わる、保存
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

print("--- gA_3_検証結果（論文の3.3に記載する数値） ---")
print(summary)
print("\n--- 各ラベルのデータ数 ---")
print(count)

# 保存 (ファイル名をgA_3用に変更)
df.to_csv("/Users/mizuki/team_discussion/2025_12/GA/mini_analysis/gA_3_validation_result.csv", index=False)