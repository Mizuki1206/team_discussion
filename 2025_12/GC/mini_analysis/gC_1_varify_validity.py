import pandas as pd

# CSVの読み込み
CSV_FILE = "/Users/mizuki/team_discussion/2025_12/analysis_csv/analysis_csv_gC_1.csv"
df = pd.read_csv(CSV_FILE)

# --- 人手によるラベル付け (20セグメント版) ---
# CSVの各行（Main_Topics）の内容に基づいて再割り当てしました
# D: Divergence (発散), C: Convergence (収束), O: Other (その他)

manual_labels = [
    'O', # Seg 1: [準備] 入る、オッケー、SDGs基礎
    'D', # Seg 2: [発散] サンゴ礁、社会課題、やる方法
    'D', # Seg 3: [発散] みんなで話す、意見を掘り下げる
    'D', # Seg 4: [発散] 実生活、解決策、プラスチック
    'D', # Seg 5: [発散] ゴミ問題、学校生活、規模がでかい
    'D', # Seg 6: [発散] キャリア、つながる話題、有働くん
    'O', # Seg 7: [その他] マイクが入らない、地域、話しやすい
    'O', # Seg 8: [その他] 時間確認、まとめる、実行できるか
    'D', # Seg 9: [発散] 防災マップ、津波、逃げる場所
    'D', # Seg 10: [発散] ゴール設定、外部知識、議論の意義
    'D', # Seg 11: [発散] 解決案が出しやすい、話題選び
    'C', # Seg 12: [収束] 「生徒が考える校則」に決定
    'O', # Seg 13: [その他] ヘッドホン、マイク設定、聞こえる？
    'D', # Seg 14: [発散] 話題を掘り下げる、さっきの話
    'D', # Seg 15: [発散] 小中高の違い、大学の話
    'D', # Seg 16: [発散] 具体的な禁止事項、ツーブロック、高校
    'D', # Seg 17: [発散] 意味のわからない校則、小中の例
    'D', # Seg 18: [発散] 校則を作る、遊び、深める
    'D', # Seg 19: [発散] 鉛筆・シャーペン禁止の謎
    'C'  # Seg 20: [収束] まとめ、テーマ決定の再確認、終了
]

# ラベル数の整合性チェック
if len(manual_labels) != len(df):
    print(f"Warning: Label count ({len(manual_labels)}) matches DataFrame length ({len(df)})")
else:
    print("Label count matches CSV length.")

# ラベルをデータに追加
df['Label'] = manual_labels

# --- 検証：ラベルごとのスコア平均を出す ---
summary = df.groupby('Label')[['Novelty', 'Representativeness']].mean()
count = df['Label'].value_counts()

print("--- 検証結果（論文の3.3に記載する数値 / gC_1） ---")
print(summary)
print("\n--- 各ラベルのデータ数 ---")
print(count)

# 保存
df.to_csv("/Users/mizuki/team_discussion/2025_12/GC/mini_analysis/gC_1_validation_result.csv", index=False)