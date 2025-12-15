import MeCab
import ipadic

# 形態素解析器の準備
tagger = MeCab.Tagger(ipadic.MECAB_ARGS)

# テスト用テキスト
text = "グループディスカッションにおいて、議論が深まらない課題がある。"

# 除外したい単語リスト
stop_words = {"ある", "いる", "なる", "れる", "られる", "こと", "ため", "おい"}

# 解析の実行
node = tagger.parseToNode(text)
words = []

# ノードを順番に見る
while node:
    # 単語の情報を取得
    surface = node.surface
    feature = node.feature.split(',')
    pos = feature[0]  # 品詞情報
    original = feature[6]  # 原形

    # 原形データがない場合は表層形を使用
    if original == '*':
        original = surface

    # 分析に意味のある単語のみを抽出
    if pos in ['名詞', '動詞', '形容詞']:
        if original not in stop_words and feature[1] != "数":
            words.append(original)
    node = node.next

# 結果の表示
print("元のテキスト:", text)
print("抽出された単語:", words)
print("\n空白で区切られたテキスト:", ' '.join(words))