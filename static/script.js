// Deposit button logic
document.getElementById("add-money").addEventListener("click", async () => {
    const amount = document.getElementById("deposit").value;
    const response = await fetch("/deposit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ amount })
    });
    const data = await response.json();
    if (data.error) {
        alert(data.error);
        return;
    }
    document.getElementById("balance").innerText = data.balance;
});

// Spin button logic
document.getElementById("spin-button").addEventListener("click", async () => {
    const lines = document.getElementById("lines").value;
    const bet = document.getElementById("bet").value;
    const response = await fetch("/spin", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ lines, bet })
    });
    const data = await response.json();
    if (data.error) {
        alert(data.error);
        return;
    }
    document.getElementById("balance").innerText = data.balance;

    // Only update result section (not the whole container)
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = `
        <p>Reels:</p>
        <pre>${data.reels.map(row => row.join(" | ")).join("\n")}</pre>
        <p>Winnings: $${data.winnings}</p>
        <p>Winning Lines: ${data.winning_lines.join(", ") || "None"}</p>
    `;
});
