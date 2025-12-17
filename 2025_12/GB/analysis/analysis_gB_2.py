import re
import MeCab
import ipadic
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- 設定 ---
LOG_FILE = "/Users/mizuki/team_discussion/2025_12/meeting_log/meeting_log_gB_2.txt"
OUTPUT_CSV = "/Users/mizuki/team_discussion/2025_12/analysis_csv/analysis_csv_gB_2.csv"
NUM_SEGMENTS = 20

# ノイズ除去リスト
IGNORE_PHRASES = [
    # 挨拶・定型句
    "ありがとうございます", "ありがとう", "お願いします", "すいません", "すみません",
    "おはようございます", "お疲れ様です", "失礼します",
    # 相槌・応答
    "ああ", "あー", "うん", "うんうん", "そう", "そうそう", "そうですね", "ですね", 
    "なるほど", "はい", "ええ", "オッケー", "OK", "大丈夫", "了解", "わかった",
    "確かに", "ほんと", "本当", "まじ", "へー", "ふーん", "ね", "さ", "よ", "の",
    # フィラー（言い淀み）
    "えー", "えっと", "え～", "あの", "あのー", "その", "んー", "うーん", "うー",
    "まあ", "なんか", "なんて", "っす", "ていうか", "っていうか", "ていう", "という",
    # 意味の薄い言葉・副詞
    "ちょっと", "一応", "多分", "結構", "かなり", "すごい", "すごく", 
    "やっぱり", "やっぱ", "かも", "しれない", "なんか", "だいたい", "色々",
    # 接続詞的な口語
    "でも", "だけど", "だから", "けど", "じゃあ", "では", "あと",
    "それこそ", "なんで", "どう", "こう",
    # 会議進行
    "聞こえる", "聞こえてる", "見えてる", "画面", "共有", "終了", "ミュート", "マイク"
]

STOP_WORDS = ["ある", "いる", "なる", "れる", "られる", "こと", "ため", "おい", "くる", "いく", 
              "これ", "それ", "あれ", "さん", "の", "ん", "よう", "ない", "私", "僕", "俺", "自分"]

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
        if metadata_pattern.match(line): continue # メタデータ行スキップ
        
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