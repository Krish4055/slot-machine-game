from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import random
from models import create_or_get_user, update_balance, get_balance

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session

@app.route('/')
def index():
    if "user_id" not in session:
        return render_template('login.html')  # Show login page if not logged in
    return render_template('index.html', username=session["username"], balance=get_balance(session["user_id"]))

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    if not username:
        return jsonify({"error": "Username required"})
    user = create_or_get_user(username)
    session["user_id"] = user["id"]
    session["username"] = user["username"]
    return jsonify({"message": "Login successful", "balance": user["balance"], "username": user["username"]})

@app.route('/deposit', methods=['POST'])
def deposit():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"})
    data = request.get_json()
    amount = int(data.get("amount", 0))
    if amount <= 0:
        return jsonify({"error": "Invalid deposit amount"})
    new_balance = get_balance(session["user_id"]) + amount
    update_balance(session["user_id"], new_balance)
    return jsonify({"balance": new_balance})

@app.route('/spin', methods=['POST'])
def spin():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"})
    data = request.get_json()
    lines = int(data.get("lines", 1))
    bet = int(data.get("bet", 1))
    total_bet = lines * bet
    current_balance = get_balance(session["user_id"])
    if total_bet > current_balance:
        return {"error": "Insufficient balance"}
    new_balance = current_balance - total_bet

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

    new_balance += winnings
    update_balance(session["user_id"], new_balance)
    return {
        "balance": new_balance,
        "reels": reels,
        "winnings": winnings,
        "winning_lines": winning_lines
    }

# LOGOUT ROUTE - SINGLE DEFINITION
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))  # Redirect to login page

if __name__ == "__main__":
    app.run(debug=True)
