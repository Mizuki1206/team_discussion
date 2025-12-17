import pandas as pd

# CSVの読み込み (ファイル名をgB_3用に変更)
CSV_FILE = "/Users/mizuki/team_discussion/2025_12/analysis_csv/analysis_csv_gB_3.csv"
df = pd.read_csv(CSV_FILE)

# --- 人手によるラベル付け (あなたの判断) ---
# D: Divergence (発散・アイデア出し・議論の展開・具体例の提示)
# C: Convergence (収束・方向性の決定・まとめ・合意形成)
# O: Other (雑談・事務連絡・準備・機材トラブル・脱線)

# ログ(meeting_log_gB_3.txt)に基づいた推奨ラベル設定:
manual_labels = [
    'O', # Seg 1: [準備] 共有、画面、待つ
    'D', # Seg 2: [発散] スタート、話す
    'D', # Seg 3: [発散] 素行、良い悪い
    'D', # Seg 4: [発散] 勉強、ベクトル
    'D', # Seg 5: [発散] パスワード、ゲーム
    'D', # Seg 6: [発散] 変わる、ブランディング
    'D', # Seg 7: [発散] 老害、先生
    'D', # Seg 8: [発散] 地域、実地
    'D', # Seg 9: [発散] 言い方、良い
    'D', # Seg 10: [発散] 呼び出し、怖い
    'D', # Seg 11: [発散] アンケート
    'D', # Seg 12: [発散] 解決策、ストライキ
    'D', # Seg 13: [発散] 手段、最終
    'C', # Seg 14: [収束] まとめる、落とし所
    'O', # Seg 15: [脱線] ノイキャン、聞こえる
    'D', # Seg 16: [発散] 隔離、組合
    'D', # Seg 17: [発散] サークル、コミュニティ
    'C', # Seg 18: [収束] 解決、平和的
    'C', # Seg 19: [収束] 組合を作る、学校
    'O'  # Seg 20: [その他] 終了、民主的
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

print("--- gB_3_検証結果（論文の3.3に記載する数値） ---")
print(summary)
print("\n--- 各ラベルのデータ数 ---")
print(count)

# 保存 (ファイル名をgB_3用に変更)
df.to_csv("/Users/mizuki/team_discussion/2025_12/GB/mini_analysis/gB_3_validation_result.csv", index=False)