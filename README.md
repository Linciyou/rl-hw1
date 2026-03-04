# 網格地圖開發與策略評估 (HW1)

這是一個基於 Streamlit 開發的強化學習 (Reinforcement Learning) 網頁應用程式，用於展示馬可夫決策過程 (MDP) 中的網格世界環境與策略評估 (Policy Evaluation)。

## 功能特點
- 支援動態調整網格大小 $n \times n$ ($n$ 範圍 5~9)。
- 互動式圖形介面，可依序點擊設定：
  - **起點** (綠色)
  - **終點** (紅色)
  - **$n-2$ 個障礙物** (灰色)
- 隨機生成每個狀態的行動策略 (上、下、左、右)。
- 自動執行**策略評估**，並利用 Matplotlib 視覺化呈現 `Value Matrix` 與 `Policy Matrix`。

## 本地端執行方式

1. 安裝必要套件：
```bash
pip install -r requirements.txt