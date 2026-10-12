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

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


if __name__ == "__main__":
    app.run()
