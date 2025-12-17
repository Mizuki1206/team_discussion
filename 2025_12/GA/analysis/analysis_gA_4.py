import re
import MeCab
import ipadic
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 設定
LOG_FILE = "/Users/mizuki/team_discussion/2025_12/meeting_log/meeting_log_gA_4.txt"
OUTPUT_CSV = "/Users/mizuki/team_discussion/2025_12/analysis_csv/analysis_csv_gA_4.csv"
NUM_SEGMENTS = 20

# ノイズ除去リスト
IGNORE_PHRASES = [
    "ありがとうございます", "ありがとう", "お願いします", "すいません",
    "ああ", "あー", "うん", "そう", "そうですね", "なるほど", "はい", "えー", "えっと", 
    "まあ", "ですね", "という", "ていう", "聞こえる", "見えてる", "オッケー", "OK", "大丈夫", 
    "へー", "ふーん", "ね", "さ", "よ",
    "終了", "開始", "レコーディング", "録音", "分", "時間", "source", "ソース", "共有"
]

STOP_WORDS = ["ある", "いる", "なる", "れる", "られる", "こと", "ため", "おい", "くる", "いく", 
              "これ", "それ", "あれ", "さん", "の", "ん", "よう", "ない", "私", "僕", "俺"]

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
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {LOG_FILE}")
        return

    clean_docs = []
    metadata_pattern = re.compile(r'.*\[.*?\].*\d{1,2}:\d{2}:\d{2}')

    for line in lines:
        line = line.strip()
        if not line: continue
        if metadata_pattern.match(line): continue
        
        text = line
        if text in IGNORE_PHRASES: continue
        
        words = get_clean_words(text)
        if words:
            clean_docs.append(" ".join(words))

    segment_docs = [""] * NUM_SEGMENTS
    chunk_size = len(clean_docs) / NUM_SEGMENTS if clean_docs else 1

    for i, doc in enumerate(clean_docs):
        seg_idx = int(i / chunk_size)
        if seg_idx >= NUM_SEGMENTS: seg_idx = NUM_SEGMENTS - 1
        segment_docs[seg_idx] += " " + doc

    if all(not d.strip() for d in segment_docs):
        print("有効なテキストデータがありませんでした。")
        return

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(segment_docs)
    global_centroid = np.asarray(X.mean(axis=0))

    results = []
    for i in range(NUM_SEGMENTS):
        current_vec = X[i].toarray()
        if i == 0: novelty = 0.0
        else:
            prev_vec = X[i-1].toarray()
            sim = cosine_similarity(current_vec, prev_vec)[0][0]
            novelty = 1.0 - sim
        rep_sim = cosine_similarity(current_vec, global_centroid)[0][0]
        representativeness = rep_sim

        feature_names = vectorizer.get_feature_names_out()
        tfidf_scores = current_vec.flatten()
        top_indices = tfidf_scores.argsort()[::-1]
        top_words = []
        for idx in top_indices:
            if tfidf_scores[idx] > 0:
                top_words.append(feature_names[idx])
            if len(top_words) >= 5: break

        results.append({
            "Segment": i + 1,
            "Novelty": round(novelty, 3),
            "Representativeness": round(representativeness, 3),
            "Main_Topics": top_words
        })

    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8_sig')
    print(f"保存完了: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()