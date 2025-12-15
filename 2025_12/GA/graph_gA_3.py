import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import japanize_matplotlib

# 設定
CSV_FILE = "/Users/mizuki/team_discussion/2025_12/analysis_csv/analysis_csv_gA_3.csv"
OUTPUT_IMG = "/Users/mizuki/team_discussion/2025_12/analysis_graph_gA_3.png"

def main():
    # データの読み込み
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        print(f"エラー: ファイルが見つかりません {CSV_FILE}")
        return

    # グラフの描画設定
    plt.figure(figsize=(10, 6)) # 横長で見やすく
    
    # スタイル設定
    plt.style.use('seaborn-v0_8-whitegrid')
    japanize_matplotlib.japanize()
    
    # 線グラフのプロット
    # 鮮度 (Novelty): 青色・実線
    plt.plot(df["Segment"], df["Novelty"], 
             marker='o', label='Novelty (鮮度)', color='#1f77b4', linewidth=2)
    
    # 代表度 (Representativeness): オレンジ色・実線
    plt.plot(df["Segment"], df["Representativeness"], 
             marker='s', label='Representativeness (代表度)', color='#ff7f0e', linewidth=2)

    # 論文用の装飾（日本語）
    plt.title("議論構造の分析（鮮度と代表度の時系列推移）", fontsize=14)
    plt.xlabel("セグメント（時間 1-20）", fontsize=12)
    plt.ylabel("スコア (0.0 - 1.0)", fontsize=12)
    plt.ylim(0, 1.1) # Y軸の範囲
    plt.xlim(1, 20)  # X軸の範囲
    
    # 軸の目盛りを整数にする（1, 2, 3...）
    plt.gca().get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True))

    # 凡例を表示
    plt.legend(loc='upper right', frameon=True, fontsize=11)


    # Segment 7: 代表度のピーク（収束・決定）
    # データが存在する場合のみ座標を取得して描画
    if 7 in df['Segment'].values:
        y_val_7 = df.loc[df['Segment']==7, 'Representativeness'].values[0]
        plt.annotate('収束（決定）', xy=(7, y_val_7), xytext=(7, y_val_7 + 0.15),
                     arrowprops=dict(facecolor='black', shrink=0.05),
                     ha='center', fontsize=10)

    # Segment 16: 鮮度のピーク（脱線・発散）
    if 16 in df['Segment'].values:
        y_val_16 = df.loc[df['Segment']==16, 'Novelty'].values[0]
        plt.annotate('発散（脱線）', xy=(16, y_val_16), xytext=(16, y_val_16 + 0.15),
                     arrowprops=dict(facecolor='red', shrink=0.05),
                     ha='center', fontsize=10, color='red')

    # 保存と表示
    plt.tight_layout()
    plt.savefig(OUTPUT_IMG, dpi=300) # 高画質で保存
    print(f"グラフを保存しました: {OUTPUT_IMG}")
    
    # 画面にも表示
    plt.show()

if __name__ == "__main__":
    main()