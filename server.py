from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

balance = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/deposit', methods=['POST'])
def deposit():
    global balance
    data = request.get_json()
    amount = int(data.get("amount", 0))
    if amount <= 0:
        return jsonify({"error": "Invalid deposit amount"})
    balance += amount
    return jsonify({"balance": balance})

@app.route('/spin', methods=['POST'])
def spin():
    global balance
    data = request.get_json()
    lines = int(data.get("lines", 1))
    bet = int(data.get("bet", 1))
    total_bet = lines * bet
    if total_bet > balance:
        return {"error": "Insufficient balance"}
    balance -= total_bet

    symbols = ["A", "B", "C", "D"]
    PAYOUTS = {"A": 2, "B": 5, "C": 10, "D": 20}
    reels = [[random.choice(symbols) for _ in range(3)] for _ in range(3)]
    winnings = 0
    winning_lines = []

    for i in range(lines):
        if reels[i][0] == reels[i][1] == reels[i][2]:
            symbol = reels[i][0]
            winnings += bet * PAYOUTS[symbol]
            winning_lines.append(i + 1)

    balance += winnings
    return {
        "balance": balance,
        "reels": reels,
        "winnings": winnings,
        "winning_lines": winning_lines
    }


if __name__ == "__main__":
    app.run(debug=True)
