import pandas as pd

# CSVの読み込み (gC_2)
CSV_FILE = "/Users/mizuki/team_discussion/2025_12/analysis_csv/analysis_csv_gC_2.csv"
df = pd.read_csv(CSV_FILE)

# --- 人手によるラベル付け (gC_2 / 20セグメント版) ---
manual_labels = [
    'D', # Seg 1: [発散] 問題の定義、生徒が考える校則とは
    'D', # Seg 2: [発散] 定義の確認、ツーブロックの話
    'D', # Seg 3: [発散] スマホ禁止、ダメな理由
    'D', # Seg 4: [発散] 生徒を守るための校則か？
    'D', # Seg 5: [発散] 先生が決める、方向性の確認
    'D', # Seg 6: [発散] どっちの問題でいくか（作るvs既存）
    'C', # Seg 7: [収束] 「ブラック校則（既存の問題）」にフォーカス決定
    'D', # Seg 8: [発散] 人権侵害、個人の尊厳
    'D', # Seg 9: [発散] 高校生と小中学生の違い、義務教育
    'D', # Seg 10: [発散] 責任能力、自己責任論
    'D', # Seg 11: [発散] バイト、管理下、15歳以上
    'D', # Seg 12: [発散] メイク禁止、授業への影響
    'D', # Seg 13: [発散] 問題の核心探し、プールの例
    'D', # Seg 14: [発散] 新しいマナー、時代に取り残されている
    'D', # Seg 15: [発散] 社会のルールを学ぶ場、時代錯誤
    'D', # Seg 16: [発散] 学校の価値、入れ墨（正当な禁止例）
    'D', # Seg 17: [発散] 迷惑をかけるかどうか、判断基準
    'C', # Seg 18: [収束] 核心のまとめ「時代に追いついていない」
    'C', # Seg 19: [収束] 合理性がない、不透明であることで合意
    'O'  # Seg 20: [その他] 次回予告、終了、雑談
]

df['Label'] = manual_labels

# 検証と保存
summary = df.groupby('Label')[['Novelty', 'Representativeness']].mean()
print("--- 検証結果（gC_2） ---")
print(summary)
df.to_csv("/Users/mizuki/team_discussion/2025_12/GC/mini_analysis/gC_2_validation_result.csv", index=False)