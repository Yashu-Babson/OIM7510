# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of option, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who will use my tool: This tool helps traders and fund managers rebalance portfolios toward their cileints' target stock weights. It calculates how many shares to buy or sell for each stock. Trades use whole shares, with selling adjustment first then buying based on available cash.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI
    My plan before AI:
    Step 1: Calculate each holding value first: shares pultiplied by price;
    Step 2: Sum hoding values plus starting cash to get total value of underling portfolio;
    Step 3: Calculate each holding's current portion, and compare each against its target weight;
    Step 4: Multiply total portfolio value by each target weight to calculate its target value;
    Step 5: Calculate target shares: target value divided by stock price and round down to integer;
    Step 6: Compare target shares with current shares to determin how many to buy or to sell;
    Step 7: Execute sell orders first, after selling, calculate total available cash;
    Step 8: Execute buy orders, checking available cash;
    Step 9: Calculate adjusted holding values and remaining cash;
    Step 10: Calculate final weights and gaps.

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    My loop carries calculating total holding values, available cash.
    I would check cash constantly; I would also check final shares multiplied by current prices plus remaining cash, and compare the total value with original total value plus starting cash.


    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your option from the Mini Project 1 page. If you chose D, your own option, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    holdings = [
        ("AAPL", 100, 173.93),
        ("MSFT", 50, 319.53),
        ("GOOG", 80, 131.36),
        ("AMZN", 200, 129.33),
        ("NVDA", 20, 410.17),
        ("TSLA", 150, 255.70),
    ]

    cash = 5000.00

    target_weights = {
        "AAPL": 0.20,
        "MSFT": 0.20,
        "GOOG": 0.15,
        "AMZN": 0.15,
        "NVDA": 0.15,
        "TSLA": 0.15,}

    return cash, holdings, target_weights


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(cash, holdings):
    total = 0

    for _ticker, _shares, _price in holdings:
        total = total + _shares * _price

    portfolio_value = total + cash

    print(f"Stocks value: ${total:,.2f}")
    print(f"Total including cash: ${portfolio_value:,.2f}")
    return (portfolio_value,)


@app.cell
def _(holdings, portfolio_value, target_weights):
    trades = []

    for _ticker, _shares, _price in holdings:
        _target_value = portfolio_value * target_weights[_ticker]
        _target_shares = int(_target_value // _price)
        _trade = _target_shares - _shares

        trades.append((_ticker, _shares, _price, _target_shares, _trade))
        print(f"{_ticker}: target {_target_shares} shares, trade {_trade:+d}")
    return (trades,)


@app.cell
def _(cash, trades):
    cash_after = cash

    # Sell first: negative trade quantities generate cash.
    for _ticker, _shares, _price, _target_shares, _trade in trades:
        if _trade < 0:
            cash_after = cash_after - _trade * _price

    print(f"Cash after sales: ${cash_after:,.2f}")

    # Buy next: positive trade quantities use cash.
    for _ticker, _shares, _price, _target_shares, _trade in trades:
        if _trade > 0:
            _purchase_cost = _trade * _price
            if _purchase_cost <= cash_after:
                cash_after = cash_after - _purchase_cost
            else:
                raise ValueError(f"Not enough cash to buy {_ticker}")

    print(f"Cash remaining: ${cash_after:,.2f}")
    return (cash_after,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    Selling 60 AMZN and 79 TSLA shares funds the purchases shown in the table, leaving $725.62 in cash and every stock within 0.245 percentage points of its target, which I consider close enough given the whole-share constraint.
    """)
    return


@app.cell
def _(cash_after, portfolio_value, target_weights, trades):
    print(f"{'Ticker':<7} {'Now':>6} {'Target':>7} {'Trade':>7} "
          f"{'Value after':>13} {'Weight':>9} {'Gap (pp)':>10}")

    for _ticker, _shares, _price, _target_shares, _trade in trades:
        _value_after = _target_shares * _price
        _weight_after = _value_after / portfolio_value
        _gap = (_weight_after - target_weights[_ticker]) * 100

        print(f"{_ticker:<7} {_shares:>6} {_target_shares:>7} {_trade:>+7d} "
              f"{_value_after:>13,.2f} {_weight_after:>9.2%} {_gap:>10.3f}")

    print(f"\nCash remaining: ${cash_after:,.2f}")
    print(f"Cash weight: {cash_after / portfolio_value:.2%}")
    print("Positive trades = BUY; negative trades = SELL.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    I compared the original portfolio value, including starting cash, with the final holdings’ value plus remaining cash. I rebuilt final shares as current shares plus trade quantity, then multiplied by the stock prices and added cash. Both totals were $121,302.70, giving a difference of $0.00 to the nearest cent. Remaining cash was $725.62, so the cash balance was nonnegative.
    """)
    return


@app.cell
def _(cash_after, portfolio_value, trades):
    _check_after = cash_after

    for _ticker, _shares, _price, _target_shares, _trade in trades:
        _final_shares = _shares + _trade
        _check_after = _check_after + _final_shares * _price

    _difference = _check_after - portfolio_value

    print(f"Value before: ${portfolio_value:,.2f}")
    print(f"Value after:  ${_check_after:,.2f}")
    print(f"Difference:   ${_difference:,.2f}")
    print(f"Value preserved: {abs(_difference) < 0.01}")
    print(f"Cash nonnegative: {cash_after >= 0}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    I used AI to help translate my rebalancing plan into Python, including loops, whole-share rounding, and formatted output. The generated calculation code ran successfully after I corrected my copying errors. I checked the results using the value-conservation check in Section 6: final holdings plus cash equaled the original $121,302.70, and remaining cash was nonnegative. It checks the cash accounting, although it does not alone prove that every target weight is correct.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further
    In reality, buy and sell stocks exist fees(at lease from my knowledge in mainland China, usually selling fees are 0.1% higher than buying fees), so my first attempt would add back those fees.
    Another apply for me would be, adding a drift threshold to avoid high frequency adjustment, a 5%~7% drift for example(in order to test different results).

    Summary:
    For my extension test in Section 8, I added hypothetical transaction fees of 0.1% for buying and 0.2% for selling, plus a drift threshold to avoid trading when a holding is already close to its target weight. These fees are experiment assumptions, not actual U.S. fee rates. I used AI to help implement the code.

    I tested thresholds of 5, 6, and 7 percentage points. At 5, all six stocks traded. At 6, AAPL stayed unchanged and the other five traded, leaving $7,427.52 in cash with $81.37 in fees. At 7, only NVDA and TSLA traded, leaving $15,305.98 in cash with $50.24 in fees.

    I chose 6 percentage points because it left less cash uninvested than 7, while avoiding the AAPL trade. This experiment showed the tradeoff between reducing trading costs and keeping holdings closer to their target weights. For the final run, account value after trading was $121,221.33; adding back $81.37 in fees matched the original $121,302.70 to the nearest cent, and the reconciliation returned True.

    I totally don't know how to run it btw, my assistant gave me a whole bunch of long codes
    """)
    return


@app.cell
def _():
    # Section 8 experiment assumptions—not actual U.S. fee rates.
    drift_threshold = 0.06  # 0.60%
    buy_fee_rate = 0.001    # 0.10%
    sell_fee_rate = 0.002   # 0.20%
    return buy_fee_rate, drift_threshold, sell_fee_rate


@app.cell
def _(
    buy_fee_rate,
    cash,
    drift_threshold,
    holdings,
    portfolio_value,
    sell_fee_rate,
    target_weights,
):
    extension_trades = []
    extension_cash = cash
    extension_fees = 0

    # Select trades using weights before any trading.
    for _ticker, _shares, _price in holdings:
        _weight = _shares * _price / portfolio_value
        _trade = 0

        if abs(_weight - target_weights[_ticker]) > drift_threshold:
            _target = int(portfolio_value * target_weights[_ticker] // _price)
            _trade = _target - _shares

        extension_trades.append((_ticker, _shares, _price, _trade))
        print(_ticker, "threshold:", drift_threshold, "trade:", _trade)

    # Sell first, subtracting selling fees.
    for _ticker, _shares, _price, _trade in extension_trades:
        if _trade < 0:
            _sale_value = -_trade * _price
            _fee = _sale_value * sell_fee_rate
            extension_cash = extension_cash + _sale_value - _fee
            extension_fees = extension_fees + _fee

    # Buy only what available cash can cover, including fees.
    extension_results = []

    for _ticker, _shares, _price, _trade in extension_trades:
        if _trade > 0:
            _affordable = int(
                extension_cash // (_price * (1 + buy_fee_rate))
            )
            _trade = min(_trade, _affordable)
            _purchase_value = _trade * _price
            _fee = _purchase_value * buy_fee_rate
            extension_cash = extension_cash - _purchase_value - _fee
            extension_fees = extension_fees + _fee

        extension_results.append(
            (_ticker, _shares + _trade, _price, _trade)
        )

    # Value the final account after fees.
    _extension_value = extension_cash
    for _ticker, _shares, _price, _trade in extension_results:
        _extension_value = _extension_value + _shares * _price

    print(f"{'Ticker':<7} {'Trade':>7} {'Final shares':>13} {'Weight':>9}")
    for _ticker, _shares, _price, _trade in extension_results:
        _weight = _shares * _price / _extension_value
        print(f"{_ticker:<7} {_trade:>+7d} {_shares:>13} {_weight:>9.2%}")

    print(f"\nRemaining cash: ${extension_cash:,.2f}")
    print(f"Total fees: ${extension_fees:,.2f}")
    print(f"Final account value: ${_extension_value:,.2f}")
    _check = abs(_extension_value + extension_fees - portfolio_value) < 0.01
    print(f"Value plus fees matches start: {_check}")
    return


if __name__ == "__main__":
    app.run()
