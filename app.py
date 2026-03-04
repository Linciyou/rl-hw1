import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# 初始化 Session State
if 'n' not in st.session_state:
    st.session_state.n = 5
if 'step' not in st.session_state:
    st.session_state.step = 0 # 0: 起點, 1: 終點, 2: 障礙物, 3: 完成
if 'start_cell' not in st.session_state:
    st.session_state.start_cell = None
if 'end_cell' not in st.session_state:
    st.session_state.end_cell = None
if 'obstacles' not in st.session_state:
    st.session_state.obstacles = []

def reset_grid():
    st.session_state.step = 0
    st.session_state.start_cell = None
    st.session_state.end_cell = None
    st.session_state.obstacles = []

st.set_page_config(page_title="HW1 網格地圖與策略評估", layout="centered")
st.title("HW1: 網格地圖開發與策略評估 🤖")

# 側邊欄設定
st.sidebar.header("環境設定")
new_n = st.sidebar.number_input("輸入網格大小 N (5~9)", min_value=5, max_value=9, value=st.session_state.n)

if new_n != st.session_state.n:
    st.session_state.n = new_n
    reset_grid()

if st.sidebar.button("🔄 重新生成地圖"):
    reset_grid()

n = st.session_state.n
max_obstacles = n - 2

# 顯示操作指示
st.subheader("地圖建構區")
if st.session_state.step == 0:
    st.info("步驟 1: 請點擊下方按鈕選擇 **起始單元格 (綠色)**")
elif st.session_state.step == 1:
    st.info("步驟 2: 請點擊下方按鈕選擇 **結束單元格 (紅色)**")
elif st.session_state.step == 2:
    st.info(f"步驟 3: 請點擊下方按鈕選擇 **{max_obstacles - len(st.session_state.obstacles)} 個障礙物 (灰色)**")
else:
    st.success("✅ 設定完成！請滑到最下方點擊「執行策略評估」。")

# 繪製互動按鈕網格
for r in range(n):
    cols = st.columns(n)
    for c in range(n):
        cell_id = (r, c)
        
        # 決定按鈕狀態
        if cell_id == st.session_state.start_cell:
            label = "🟢 起點"
        elif cell_id == st.session_state.end_cell:
            label = "🔴 終點"
        elif cell_id in st.session_state.obstacles:
            label = "⬛ 障礙"
        else:
            label = f"{r},{c}"
            
        with cols[c]:
            if st.button(label, key=f"btn_{r}_{c}", use_container_width=True):
                if st.session_state.step == 0:
                    st.session_state.start_cell = cell_id
                    st.session_state.step = 1
                    st.rerun()
                elif st.session_state.step == 1 and cell_id != st.session_state.start_cell:
                    st.session_state.end_cell = cell_id
                    st.session_state.step = 2
                    st.rerun()
                elif st.session_state.step == 2 and cell_id not in [st.session_state.start_cell, st.session_state.end_cell]:
                    if cell_id not in st.session_state.obstacles:
                        st.session_state.obstacles.append(cell_id)
                        if len(st.session_state.obstacles) >= max_obstacles:
                            st.session_state.step = 3
                    st.rerun()

st.divider()

# 策略評估演算法
def policy_evaluation(n, start, end, obstacles, policy, gamma=0.9, theta=1e-4):
    V = np.zeros((n, n))
    states = [(i, j) for i in range(n) for j in range(n)]
    
    while True:
        delta = 0
        for s in states:
            r, c = s
            if s == end or s in obstacles:
                continue
            
            v = V[r, c]
            action = policy[r][c]
            
            next_r, next_c = r, c
            if action == 'up': next_r -= 1
            elif action == 'down': next_r += 1
            elif action == 'left': next_c -= 1
            elif action == 'right': next_c += 1
            
            if next_r < 0 or next_r >= n or next_c < 0 or next_c >= n or (next_r, next_c) in obstacles:
                next_r, next_c = r, c 
            
            reward = 1 if (next_r, next_c) == end else 0
            V[r, c] = reward + gamma * V[next_r, next_c]
            delta = max(delta, abs(v - V[r, c]))
            
        if delta < theta:
            break
    return V

# 繪圖函數
def draw_matrices(n, V, policy, start, end, obstacles):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    for ax, title in zip([ax1, ax2], ["Value Matrix", "Policy Matrix"]):
        ax.set_title(title, fontsize=16)
        ax.set_xlim(0, n)
        ax.set_ylim(n, 0)
        ax.set_xticks(np.arange(n))
        ax.set_yticks(np.arange(n))
        ax.grid(color='#1f77b4', linestyle='-', linewidth=2)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.tick_params(length=0)

        for r in range(n):
            for c in range(n):
                cell = (r, c)
                if cell == start:
                    ax.add_patch(plt.Rectangle((c, r), 1, 1, color='green', alpha=0.6))
                elif cell == end:
                    ax.add_patch(plt.Rectangle((c, r), 1, 1, color='red', alpha=0.6))
                elif cell in obstacles:
                    ax.add_patch(plt.Rectangle((c, r), 1, 1, color='gray', alpha=0.8))
                
                if cell != end and cell not in obstacles:
                    if title == "Value Matrix":
                        ax.text(c + 0.5, r + 0.5, f"{V[r, c]:.2f}", va='center', ha='center', fontsize=12)
                    else:
                        a = policy[r][c]
                        arrow_map = {'up': '↑', 'down': '↓', 'left': '←', 'right': '→'}
                        ax.text(c + 0.5, r + 0.5, arrow_map[a], va='center', ha='center', fontsize=20)
    return fig

# 執行區塊
if st.session_state.step == 3:
    st.subheader("運算結果")
    if st.button("🚀 執行策略評估", type="primary", use_container_width=True):
        actions = ['up', 'down', 'left', 'right']
        policy = [[random.choice(actions) for _ in range(n)] for _ in range(n)]
        
        with st.spinner('計算中...'):
            V_matrix = policy_evaluation(n, st.session_state.start_cell, st.session_state.end_cell, st.session_state.obstacles, policy)
            fig = draw_matrices(n, V_matrix, policy, st.session_state.start_cell, st.session_state.end_cell, st.session_state.obstacles)
            st.pyplot(fig)