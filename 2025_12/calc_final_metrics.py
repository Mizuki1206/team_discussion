import pandas as pd
import numpy as np
from scipy.signal import find_peaks

# 設定
CSV_FILE = "/Users/mizuki/team_discussion/2025_12/analysis_csv/analysis_result_v2.csv"
OVERLAP_THRESHOLD = 0.2  # 鮮度と代表度の差がこれ以下なら「重なっている」とみなす
PEAK_DISTANCE = 3        # ピーク検出の最小間隔

def main():
    df = pd.read_csv(CSV_FILE)
    
    # 鮮度・代表度重複時間 (T_overlap)
    # 差の絶対値をとる
    df["Diff"] = abs(df["Novelty"] - df["Representativeness"])
    
    # 閾値以下のセグメント数をカウント（1セグメント=1分相当と仮定）
    overlap_segments = df[df["Diff"] <= OVERLAP_THRESHOLD]
    t_overlap = len(overlap_segments)
    
    print(f"--- 分析結果 ---")
    print(f"1. 重複時間 (T_overlap): {t_overlap} 分 (閾値: {OVERLAP_THRESHOLD})")
    
    # 発散・収束サイクル数 (C_cycle)
    # 鮮度のピークを探す
    novelty_peaks, _ = find_peaks(df["Novelty"], distance=PEAK_DISTANCE, prominence=0.1)
    # 代表度のピークを探す
    rep_peaks, _ = find_peaks(df["Representativeness"], distance=PEAK_DISTANCE, prominence=0.05)
    
    # サイクル数の定義: 両方のピーク数の平均、または「代表度のピーク数」を採用
    # ここでは「収束しようとした回数」として代表度のピーク数を採用
    c_cycle = len(rep_peaks)
    
    print(f"2. サイクル数 (C_cycle): {c_cycle} 回")
    print(f"   - 鮮度ピーク位置(分): {novelty_peaks + 1}")
    print(f"   - 代表度ピーク位置(分): {rep_peaks + 1}")

    # 最終収束度 (S_final)
    # ラスト3セグメント（18, 19, 20）の代表度の平均
    last_3_df = df.tail(3)
    s_final = last_3_df["Representativeness"].mean()
    
    print(f"3. 最終収束度 (S_final): {s_final:.3f}")
    print("-" * 20)

if __name__ == "__main__":
    main()