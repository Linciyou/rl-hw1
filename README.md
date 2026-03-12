# 網格地圖開發與策略評估 (HW1)

這是一個基於 **Flask** 開發的強化學習 (Reinforcement Learning) 網頁應用程式，用於展示馬可夫決策過程 (MDP) 中的網格世界環境與策略評估 (Policy Evaluation)。

## 功能特點

### HW1-1：網格地圖開發
- 支援動態調整網格大小 $n \times n$（$n$ 範圍 5~9）
- 互動式圖形介面，可依序點擊設定：
  - **起點**（綠色）
  - **終點**（紅色）
  - **$n-2$ 個障礙物**（灰色）

### HW1-2：策略顯示與價值評估
- 隨機生成每個狀態的行動策略（↑↓←→）
- 使用迭代式**策略評估** (Policy Evaluation) 推導每個狀態的價值 $V(s)$
- 以 HTML 表格並排呈現 `Value Matrix` 與 `Policy Matrix`

## 技術架構

- **後端**：Flask（Python）— 提供頁面渲染與策略評估 API（`/generate`）
- **前端**：HTML + CSS + JavaScript — 互動式網格、AJAX 非同步資料交換
- **演算法參數**：折扣因子 $\gamma = 0.9$，步驟成本 $= -1$，目標獎勵 $= 0$

## 專案結構

```
rl-hw1/
├── app.py                 # Flask 後端主程式
├── templates/
│   └── index.html         # 前端頁面模板
├── static/
│   ├── style.css          # 樣式表
│   └── app.js             # 前端互動邏輯
├── hw1_demo.mp4           # Demo 影片
└── requirements.txt       # 套件需求
```

## 本地端執行方式

1. 安裝必要套件：
```bash
pip install -r requirements.txt
```

2. 啟動 Flask 伺服器：
```bash
python app.py
```

3. 開啟瀏覽器前往 http://127.0.0.1:5000/