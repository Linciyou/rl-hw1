from flask import Flask, render_template, request, jsonify
import numpy as np
import random

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    n = int(data['n'])
    start = tuple(data['start'])      # [row, col]
    end = tuple(data['end'])          # [row, col]
    obstacles = [tuple(o) for o in data['obstacles']]  # [[r,c], ...]

    # Generate random policy for each cell
    actions = ['up', 'down', 'left', 'right']
    policy = [[random.choice(actions) for _ in range(n)] for _ in range(n)]

    # Run policy evaluation
    V = policy_evaluation(n, start, end, obstacles, policy)

    # Build response
    value_matrix = [[round(float(V[r][c]), 2) for c in range(n)] for r in range(n)]
    policy_matrix = policy

    return jsonify({
        'value_matrix': value_matrix,
        'policy_matrix': policy_matrix
    })


def policy_evaluation(n, start, end, obstacles, policy, gamma=0.9, theta=1e-4):
    """
    Evaluate a deterministic policy using iterative policy evaluation.
    - Reward: +1 when transitioning INTO the goal cell, 0 otherwise.
    - Terminal state: goal cell (value stays 0).
    - Obstacles: impassable (value stays 0).
    - If action would move off-grid or into obstacle, agent stays in place.
    """
    V = np.zeros((n, n))

    while True:
        delta = 0
        for r in range(n):
            for c in range(n):
                s = (r, c)
                # Skip terminal and obstacle states
                if s == end or s in obstacles:
                    continue

                v = V[r, c]
                action = policy[r][c]

                # Determine next state
                next_r, next_c = r, c
                if action == 'up':
                    next_r -= 1
                elif action == 'down':
                    next_r += 1
                elif action == 'left':
                    next_c -= 1
                elif action == 'right':
                    next_c += 1

                # Boundary / obstacle check: stay in place
                if (next_r < 0 or next_r >= n or next_c < 0 or next_c >= n
                        or (next_r, next_c) in obstacles):
                    next_r, next_c = r, c

                # Reward
                reward = 0.0 if (next_r, next_c) == end else -1.0

                V[r, c] = reward + gamma * V[next_r, next_c]
                delta = max(delta, abs(v - V[r, c]))

        if delta < theta:
            break

    return V


if __name__ == '__main__':
    app.run(debug=True, port=5000)