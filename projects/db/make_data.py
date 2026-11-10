from datetime import date, timedelta
from random import Random

import csv
from pathlib import Path

data_dir = Path(__file__).resolve().parent / "data"
data_dir.mkdir(exist_ok=True)

members = []
for member_id in range(1, 16):
    members.append([
        member_id, "Member", str(member_id),
        f"member{member_id}@example.com", 2027, "2025-11-01",
    ])

portfolios = [
    [1, 1, "Core ETF", "2025-11-03", "Broad market"],
    [2, 1, "Growth", "2025-11-03", "Growth stocks"],
    [3, 2, "Balanced", "2025-11-03", "Mixed assets"],
]

def write_csv(filename, columns, rows):
    with (data_dir / filename).open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(rows)

write_csv(
    "members.csv",
    ["member_id", "first_name", "last_name", "email", "class_year", "join_date"],
    members,
)
write_csv(
    "portfolios.csv",
    ["portfolio_id", "member_id", "name", "created_date", "strategy"],
    portfolios,
)

# Fictional assets and simulated prices for the class project.
assets = [
    [1, "ALPN", "Alpine Software", "stock", "Technology"],
    [2, "BRGT", "Bright Grid", "stock", "Utilities"],
    [3, "CRST", "Crest Bank", "stock", "Financials"],
    [4, "DLTA", "Delta Health", "stock", "Healthcare"],
    [5, "EVRG", "Evergreen Foods", "stock", "Consumer Staples"],
    [6, "FRGE", "Forge Industries", "stock", "Industrials"],
    [7, "CORE", "Core Market Fund", "ETF", "Broad Market"],
    [8, "GRWT", "Growth Fund", "ETF", "Growth"],
    [9, "BOND", "Bond Index Fund", "ETF", "Fixed Income"],
    [10, "INTL", "International Equity Fund", "ETF", "International"],
    [11, "ORBT", "Orbit Coin", "crypto", ""],
    [12, "NOVA", "Nova Coin", "crypto", ""],
]

write_csv(
    "assets.csv",
    ["asset_id", "ticker", "name", "asset_type", "sector"],
    assets,
)

rng = Random(7510)
start_date = date(2025, 11, 3)
as_of = date(2026, 11, 2)
closing_prices = []

for asset_id, ticker, name, asset_type, sector in assets:
    price_cents = rng.randint(2_000, 25_000)
    day = start_date

    while day <= as_of:
        if asset_type == "crypto" or day.weekday() < 5:
            price_cents = max(100, price_cents + rng.randint(-150, 150))
            closing_prices.append([asset_id, day.isoformat(), f"{price_cents / 100:.2f}"])
        day += timedelta(days=1)

write_csv(
    "closing_prices.csv",
    ["asset_id", "price_date", "close_price"],
    closing_prices,
)

print(f"Generated {len(assets)} assets and {len(closing_prices)} closing prices.")

# Each asset starts with one ticker. Asset 1 changes its ticker in May.
ticker_history = []
for asset_id, ticker, *_ in assets:
    first_ticker = "ALPS" if asset_id == 1 else ticker
    ticker_history.append([asset_id, start_date.isoformat(), first_ticker])

ticker_history.append([1, "2026-05-04", "ALPN"])

write_csv(
    "ticker_history.csv",
    ["asset_id", "effective_from", "ticker"],
    ticker_history,
)

# Give each portfolio four assets to trade. Leave asset 12 untraded.
assets_by_portfolio = {
    1: [1, 7, 9, 10],
    2: [2, 3, 4, 8],
    3: [1, 5, 6, 11],
}

trades = []
for portfolio_id, asset_ids in assets_by_portfolio.items():
    for asset_id in asset_ids:
        available_prices = [row for row in closing_prices if row[0] == asset_id]

        if asset_id == 1:
            # Guarantee trades before and after the ticker change.
            selected = [available_prices[0], available_prices[-1]]
            selected += rng.sample(available_prices[1:-1], 28)
        else:
            selected = rng.sample(available_prices, 30)

        units_held = 0
        for _, trade_date, close_price in sorted(selected, key=lambda row: row[1]):
            if units_held > 0 and rng.random() < 0.4:
                side = "SELL"
                quantity = rng.randint(1, units_held)
                units_held -= quantity
            else:
                side = "BUY"
                quantity = rng.randint(5, 25)
                units_held += quantity

            trade_price = float(close_price) * rng.uniform(0.99, 1.01)
            fee = rng.choice(["0.00", "0.50", "1.00"])
            trades.append([
                len(trades) + 1, portfolio_id, asset_id, trade_date,
                side, quantity, f"{trade_price:.2f}", fee,
            ])

write_csv(
    "trades.csv",
    ["trade_id", "portfolio_id", "asset_id", "trade_date",
     "side", "quantity", "trade_price", "fee"],
    trades,
)

print(f"Generated {len(ticker_history)} ticker history rows and {len(trades)} trades.")