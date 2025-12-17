import pandas as pd

# CSVの読み込み (gC_4)
CSV_FILE = "/Users/mizuki/team_discussion/2025_12/analysis_csv/analysis_csv_gC_4.csv"
df = pd.read_csv(CSV_FILE)

# --- 人手によるラベル付け (gC_4 / 20セグメント版) ---
manual_labels = [
    'D', # Seg 1: [発散] 実現への第一歩、誰を入れるか
    'D', # Seg 2: [発散] 校長が決定権を持つ、法的な位置づけ
    'D', # Seg 3: [発散] PTA会長、自治体などを追加する案
    'D', # Seg 4: [発散] 学校への提案、売り込み
    'D', # Seg 5: [発散] 学校側のメリット提示（ブランド力）
    'D', # Seg 6: [発散] 教育委員会へのアプローチ検討
    'D', # Seg 7: [発散] メリット：思考力上昇、イメージ向上
    'D', # Seg 8: [発散] 調べていいか確認（ルールの際どいライン）
    'D', # Seg 9: [発散] 会議の現実性、時間かかる
    'O', # Seg 10: [その他] ★検索禁止ルールの確認・脱線（明確な中断）
    'D', # Seg 11: [発散] メリットの整理（偏差値、倍率）
    'D', # Seg 12: [発散] 生徒の主体性、モチベーション
    'D', # Seg 13: [発散] 学校の雰囲気、治安
    'D', # Seg 14: [発散] 地域活性化、責任感
    'C', # Seg 15: [収束] 戦略決定（江東区で実績作り→マニュアル化）
    'C', # Seg 16: [収束] 母校での実践合意
    'D', # Seg 17: [発散] メンバーの詳細詰め（手戻り：誰が集まる？）
    'D', # Seg 18: [発散] 任意参加の生徒、人数の懸念
    'D', # Seg 19: [発散] 決定権の所在、多数決？
    'C'  # Seg 20: [収束] 最終まとめ、メンバー構成の確定
]

# ラベルをデータに追加
df['Label'] = manual_labels

# 検証と保存
summary = df.groupby('Label')[['Novelty', 'Representativeness']].mean()
print("--- 検証結果（gC_4） ---")
print(summary)
df.to_csv("/Users/mizuki/team_discussion/2025_12/GC/mini_analysis/gC_4_validation_result.csv", index=False)