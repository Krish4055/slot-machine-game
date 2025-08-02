import random

ROWS, COLS = 3, 3
SYMBOLS = ["A", "B", "C", "D"]

def spin_machine(lines, bet, balance):
    total_bet = lines * bet
    if total_bet > balance:
        return {"error": "Not enough balance"}
    
    # Spin
    reels = [[random.choice(SYMBOLS) for _ in range(COLS)] for _ in range(ROWS)]

    # Check wins (example: row-wise)
    winnings = 0
    winning_lines = []
    for i in range(lines):
        if len(set(reels[i])) == 1:  # All same in the row
            winnings += bet * 5
            winning_lines.append(i + 1)

    return {
        "reels": reels,
        "winnings": winnings,
        "winning_lines": winning_lines,
        "balance": balance - total_bet + winnings
    }
