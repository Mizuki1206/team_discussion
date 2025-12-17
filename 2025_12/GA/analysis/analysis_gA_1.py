import re
import MeCab
import ipadic
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 設定
LOG_FILE = "/Users/mizuki/team_discussion/2025_12/meeting_log/meeting_log_gA_1.txt"
NUM_SEGMENTS = 20

# ノイズ除去リスト
IGNORE_PHRASES = [
    "ありがとうございます", "ありがとう", "お願いします", "すいません",
    "ああ", "あー", "うん", "そう", "そうですね", "なるほど", "はい", "えー", "えっと", 
    "まあ", "ですね", "という", "ていう", "聞こえる", "見えてる", "オッケー", "OK", "大丈夫", 
    "終了", "ボタ", "チンク", "まじ", "へー", "ふーん", "ね", "さ"
]

STOP_WORDS = ["ある", "いる", "なる", "れる", "られる", "こと", "ため", "おい", "くる", "いく", 
              "これ", "それ", "あれ", "さん", "の", "ん", "よう", "ない"]

def get_clean_words(text):
    tagger = MeCab.Tagger(ipadic.MECAB_ARGS)
    node = tagger.parseToNode(text)
    words = []
    while node:
        parts = node.feature.split(",")
        pos = parts[0]
        if pos in ["名詞", "動詞", "形容詞"]:
            original = parts[6]
            if original == "*": original = node.surface
            if len(original) > 1 and original not in STOP_WORDS:
                words.append(original)
        node = node.next
    return words

def main():
    # ログファイルの読み込みとクリーニング
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    clean_docs = [] # 全発話リスト

    # 正規表現: [名前] 発言内容  または [名前] 発言内容
    line_pattern = re.compile(r'(?:\\s*)?\[(.*?)\]\s*(.*)')

    for line in lines:
        line = line.strip()
        if not line: continue
        
        match = line_pattern.match(line)
        if match:
            text = match.group(2)
            
            # 完全一致での除外
            if text in IGNORE_PHRASES: continue
            
            # 形態素解析
            words = get_clean_words(text)
            if words:
                clean_docs.append(" ".join(words))

    print(f"有効発話数: {len(clean_docs)} 行")

    # データを「区間 (Segment)」単位でまとめる
    segment_docs = [""] * NUM_SEGMENTS
    chunk_size = len(clean_docs) / NUM_SEGMENTS

    for i, doc in enumerate(clean_docs):
        # 現在の発話がどの区間(0〜19)に入るか計算
        seg_idx = int(i / chunk_size)
        if seg_idx >= NUM_SEGMENTS: seg_idx = NUM_SEGMENTS - 1
        
        segment_docs[seg_idx] += " " + doc

    # ベクトル化 (TF-IDF)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(segment_docs)
    
    global_centroid = np.asarray(X.mean(axis=0))

    # 指標の計算
    results = []
    for i in range(NUM_SEGMENTS):
        current_vec = X[i].toarray()
        
        # 鮮度
        if i == 0:
            novelty = 0.0 # 最初は比較対象なし
        else:
            prev_vec = X[i-1].toarray()
            sim = cosine_similarity(current_vec, prev_vec)[0][0]
            novelty = 1.0 - sim
            
        # 代表度
        rep_sim = cosine_similarity(current_vec, global_centroid)[0][0]
        representativeness = rep_sim

        # 代表単語の抽出
        # ※TF-IDF値が高い単語を表示する簡易ロジック
        feature_names = vectorizer.get_feature_names_out()
        tfidf_scores = current_vec.flatten()
        top_indices = tfidf_scores.argsort()[-5:][::-1]
        top_words = [feature_names[idx] for idx in top_indices]

        results.append({
            "Segment": i + 1, # 1分目, 2分目...という意味
            "Novelty": round(novelty, 3),
            "Representativeness": round(representativeness, 3),
            "Main_Topics": top_words
        })

    # 結果表示
    df = pd.DataFrame(results)
    print("-" * 60)
    print(df[["Segment", "Novelty", "Representativeness", "Main_Topics"]])
    
    # CSV保存
    df.to_csv("analysis_csv_gA_1.csv", index=False, encoding='utf-8_sig')
    print("\nanalysis_csv_gA_1.csv に保存しました。")

if __name__ == "__main__":
    main()