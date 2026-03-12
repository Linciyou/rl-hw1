// ===== State =====
let gridSize = 5;
let step = -1;        // -1: not started, 0: pick start, 1: pick end, 2: pick obstacles, 3: done
let startCell = null;  // [row, col]
let endCell = null;
let obstacles = [];
let maxObstacles = 0;

const arrowMap = {
    'up': '↑',
    'down': '↓',
    'left': '←',
    'right': '→'
};

// ===== Grid Generation =====
function generateGrid() {
    const input = document.getElementById('gridSize');
    const n = parseInt(input.value);
    if (isNaN(n) || n < 5 || n > 9) {
        alert('請輸入 5 到 9 之間的數字！');
        return;
    }

    gridSize = n;
    maxObstacles = n - 2;
    startCell = null;
    endCell = null;
    obstacles = [];
    step = 0;

    const container = document.getElementById('gridContainer');
    container.innerHTML = '';
    container.style.gridTemplateColumns = `repeat(${n}, 60px)`;

    for (let r = 0; r < n; r++) {
        for (let c = 0; c < n; c++) {
            const cell = document.createElement('div');
            cell.className = 'grid-cell';
            cell.id = `cell-${r}-${c}`;
            cell.textContent = r * n + c + 1;
            cell.addEventListener('click', () => onCellClick(r, c));
            container.appendChild(cell);
        }
    }

    document.getElementById('gridTitle').textContent = `${n} x ${n} Square:`;
    document.getElementById('gridTitle').style.display = 'block';
    document.getElementById('evalSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';

    updateInstructions();
}

// ===== Cell Click Handler =====
function onCellClick(r, c) {
    const cellKey = [r, c];

    if (step === 0) {
        // Pick start
        startCell = cellKey;
        const el = document.getElementById(`cell-${r}-${c}`);
        el.className = 'grid-cell start';
        el.textContent = '起點';
        step = 1;
    } else if (step === 1) {
        // Pick end — must not be start
        if (r === startCell[0] && c === startCell[1]) return;
        endCell = cellKey;
        const el = document.getElementById(`cell-${r}-${c}`);
        el.className = 'grid-cell end';
        el.textContent = '終點';
        step = 2;
        if (maxObstacles === 0) {
            step = 3;
        }
    } else if (step === 2) {
        // Pick obstacle — must not be start or end or already obstacle
        if (r === startCell[0] && c === startCell[1]) return;
        if (r === endCell[0] && c === endCell[1]) return;
        if (obstacles.some(o => o[0] === r && o[1] === c)) return;

        obstacles.push(cellKey);
        const el = document.getElementById(`cell-${r}-${c}`);
        el.className = 'grid-cell obstacle';
        el.textContent = '障礙';

        if (obstacles.length >= maxObstacles) {
            step = 3;
        }
    }

    updateInstructions();

    if (step === 3) {
        document.getElementById('evalSection').style.display = 'block';
    }
}

// ===== Instructions =====
function updateInstructions() {
    const box = document.getElementById('instructions');
    const text = document.getElementById('instructionText');
    box.classList.remove('success');

    if (step === 0) {
        text.textContent = '步驟 1：請點擊網格中的一個單元格設定 起始點（綠色）';
    } else if (step === 1) {
        text.textContent = '步驟 2：請點擊網格中的一個單元格設定 終點（紅色）';
    } else if (step === 2) {
        const remaining = maxObstacles - obstacles.length;
        text.textContent = `步驟 3：請點擊網格設定障礙物（灰色），還需選擇 ${remaining} 個`;
    } else if (step === 3) {
        box.classList.add('success');
        text.textContent = '✅ 設定完成！請點擊下方「執行策略評估」按鈕。';
    }
}

// ===== Policy Evaluation (AJAX) =====
function runPolicyEvaluation() {
    const btn = document.getElementById('btnEval');
    btn.disabled = true;
    btn.textContent = '⏳ 計算中...';

    const payload = {
        n: gridSize,
        start: startCell,
        end: endCell,
        obstacles: obstacles
    };

    fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
        .then(res => res.json())
        .then(data => {
            renderResults(data.value_matrix, data.policy_matrix);
            btn.disabled = false;
            btn.textContent = '🚀 執行策略評估';
        })
        .catch(err => {
            alert('計算失敗：' + err);
            btn.disabled = false;
            btn.textContent = '🚀 執行策略評估';
        });
}

// ===== Render Results =====
function renderResults(valueMatrix, policyMatrix) {
    const n = gridSize;

    document.getElementById('resultsSection').style.display = 'block';

    // Value Matrix
    const vmContainer = document.getElementById('valueMatrix');
    vmContainer.innerHTML = '';
    vmContainer.style.gridTemplateColumns = `repeat(${n}, 60px)`;

    // Policy Matrix
    const pmContainer = document.getElementById('policyMatrix');
    pmContainer.innerHTML = '';
    pmContainer.style.gridTemplateColumns = `repeat(${n}, 60px)`;

    for (let r = 0; r < n; r++) {
        for (let c = 0; c < n; c++) {
            // Determine cell type
            const isStart = startCell && r === startCell[0] && c === startCell[1];
            const isEnd = endCell && r === endCell[0] && c === endCell[1];
            const isObs = obstacles.some(o => o[0] === r && o[1] === c);

            let extraClass = '';
            if (isStart) extraClass = ' m-start';
            else if (isEnd) extraClass = ' m-end';
            else if (isObs) extraClass = ' m-obstacle';

            // Value cell
            const vCell = document.createElement('div');
            vCell.className = 'matrix-cell' + extraClass;
            if (!isEnd && !isObs) {
                vCell.textContent = valueMatrix[r][c].toFixed(2);
            }
            vmContainer.appendChild(vCell);

            // Policy cell
            const pCell = document.createElement('div');
            pCell.className = 'matrix-cell' + extraClass;
            if (!isEnd && !isObs) {
                const span = document.createElement('span');
                span.className = 'arrow';
                span.textContent = arrowMap[policyMatrix[r][c]] || '?';
                pCell.appendChild(span);
            }
            pmContainer.appendChild(pCell);
        }
    }

    // Smooth scroll to results
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

// ===== Reset =====
function resetGrid() {
    step = -1;
    startCell = null;
    endCell = null;
    obstacles = [];

    document.getElementById('gridContainer').innerHTML = '';
    document.getElementById('gridTitle').style.display = 'none';
    document.getElementById('evalSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';

    const box = document.getElementById('instructions');
    box.classList.remove('success');
    document.getElementById('instructionText').textContent = '請先輸入網格大小並點擊「Generate Square」。';
}
