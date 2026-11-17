import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    return


@app.cell
def _(mo):
    import duckdb

    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            _result = _con.execute(sql)
            _columns = [column[0] for column in _result.description]
            return [dict(zip(_columns, row)) for row in _result.fetchall()]

    return (ask,)


@app.cell
def _(ask):
    as_of = "2026-11-16"

    ask(f"""
        SELECT p.portfolio_id, p.name AS portfolio, a.ticker,
               SUM(h.unit_change) AS units_held
        FROM holding_movements AS h
        JOIN portfolios AS p ON p.portfolio_id = h.portfolio_id
        JOIN assets AS a ON a.asset_id = h.asset_id
        WHERE h.trade_date <= DATE '{as_of}'
        GROUP BY p.portfolio_id, p.name, a.asset_id, a.ticker
        HAVING SUM(h.unit_change) > 0
        ORDER BY p.portfolio_id, a.ticker
    """)
    return (as_of,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As of November 16, 2026, the Balanced portfolio held 43 units of EVRG, 36 of FRGE, and 25 of ORBT; the table lists all positive holdings by portfolio.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Q1 · Trading Activity by Portfolio — Last 30 Days
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT p.portfolio_id, p.name AS portfolio,
               COUNT(t.trade_id) AS trade_count,
               SUM(CASE WHEN t.side = 'BUY'
                        THEN t.quantity * t.trade_price + t.fee
                        ELSE 0 END) AS spent_on_buys,
               SUM(CASE WHEN t.side = 'SELL'
                        THEN t.quantity * t.trade_price - t.fee
                        ELSE 0 END) AS received_from_sells
        FROM portfolios AS p
        LEFT JOIN trades AS t
          ON t.portfolio_id = p.portfolio_id
         AND t.trade_date BETWEEN DATE '{as_of}' - INTERVAL '29 days'
                              AND DATE '{as_of}'
        GROUP BY p.portfolio_id, p.name
        ORDER BY p.portfolio_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the 30 days ending November 16, 2026, the three portfolios made 19 trades, spent $19,468.12 on buys including fees, and received $13,659.98 from sells after fees.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Q2 · Portfolios and Total Value Bought by Member
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT m.member_id, m.first_name, m.last_name,
               COUNT(DISTINCT p.portfolio_id) AS portfolio_count,
               COALESCE(SUM(t.quantity * t.trade_price), 0) AS total_value_bought
        FROM members AS m
        LEFT JOIN portfolios AS p ON p.member_id = m.member_id
        LEFT JOIN trades AS t
          ON t.portfolio_id = p.portfolio_id
         AND t.side = 'BUY'
         AND t.trade_date <= DATE '{as_of}'
        GROUP BY m.member_id, m.first_name, m.last_name
        ORDER BY m.member_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result includes all 15 members, including members without portfolios; for example, member 15 had zero portfolios and $0 in purchases.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Q3 · Holdings by Portfolio as of November 16, 2026
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT p.portfolio_id, p.name AS portfolio, a.ticker,
               SUM(h.unit_change) AS units_held
        FROM holding_movements AS h
        JOIN portfolios AS p ON p.portfolio_id = h.portfolio_id
        JOIN assets AS a ON a.asset_id = h.asset_id
        WHERE h.trade_date <= DATE '{as_of}'
        GROUP BY p.portfolio_id, p.name, a.asset_id, a.ticker
        HAVING SUM(h.unit_change) > 0
        ORDER BY p.portfolio_id, a.ticker
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As of November 16, 2026, the Balanced portfolio held 43 units of EVRG, 36 of FRGE, 25 of ORBT, and 29 of ALPN.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Q4 · Trade Prices vs. Closing Prices
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT t.trade_id, t.trade_date, a.ticker, t.trade_price,
               c.close_price,
               ROUND(100.0 * (t.trade_price - c.close_price)
                     / c.close_price, 2) AS pct_vs_close
        FROM trades AS t
        JOIN assets AS a ON a.asset_id = t.asset_id
        LEFT JOIN closing_prices AS c
            ON c.asset_id = t.asset_id
           AND c.price_date = t.trade_date
        WHERE t.trade_date BETWEEN DATE '{as_of}' - INTERVAL '89 days'
                               AND DATE '{as_of}'
        ORDER BY t.trade_date DESC, t.trade_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The query returned 70 trades in the 90 days ending November 16, 2026. For example, trade 179 executed at $160.11 per unit for CRST, 0.88% above its October 9 closing price of $158.72.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Q5 · Assets Never Traded
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT a.asset_id, a.ticker
        FROM assets AS a
        WHERE NOT EXISTS (
            SELECT 1 FROM trades AS t
            WHERE t.asset_id = a.asset_id
        )
        ORDER BY a.asset_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    NOVA (asset 12) was the only asset that no portfolio ever traded.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Q6 · Value Traded Across the Ticker Change
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT t.asset_id,
               COUNT(*) AS trade_count,
               SUM(t.quantity * t.trade_price) AS total_value_traded
        FROM trades AS t
        WHERE t.asset_id IN (
            SELECT asset_id
            FROM ticker_history
            GROUP BY asset_id
            HAVING COUNT(DISTINCT ticker) > 1
        )
          AND t.trade_date <= DATE '{as_of}'
        GROUP BY t.asset_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Across the year of data, asset 1 traded 60 times under ALPS and ALPN, for a combined traded value of $79,123.89 before fees.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Q7 · Trades Missing a Closing Price
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT t.trade_id, t.portfolio_id, t.asset_id, t.trade_date
        FROM trades AS t
        LEFT JOIN closing_prices AS c
            ON c.asset_id = t.asset_id
           AND c.price_date = t.trade_date
        WHERE c.asset_id IS NULL
        ORDER BY t.trade_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Two trades in portfolio 1 had no matching closing price for asset 7: trade 31 on November 21, 2025, and trade 32 on December 2, 2025.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Q8 · What is each open position worth on the as_of date, using the latest available closing price on or before that date?
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        WITH positions AS (
            SELECT portfolio_id, asset_id, SUM(unit_change) AS units_held
            FROM holding_movements
            WHERE trade_date <= DATE '{as_of}'
            GROUP BY portfolio_id, asset_id
            HAVING SUM(unit_change) > 0
        ),
        latest_prices AS (
            SELECT asset_id, price_date, close_price
            FROM closing_prices
            WHERE price_date <= DATE '{as_of}'
            QUALIFY ROW_NUMBER() OVER (
                PARTITION BY asset_id ORDER BY price_date DESC
            ) = 1
        )
        SELECT p.name AS portfolio, a.ticker, h.units_held,
               c.price_date, c.close_price,
               DATE_DIFF('day', c.price_date, DATE '{as_of}') AS price_age_days,
               ROUND(h.units_held * c.close_price, 2) AS position_value
        FROM positions AS h
        JOIN portfolios AS p ON p.portfolio_id = h.portfolio_id
        JOIN assets AS a ON a.asset_id = h.asset_id
        LEFT JOIN latest_prices AS c ON c.asset_id = h.asset_id
        ORDER BY p.portfolio_id, position_value DESC NULLS LAST
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As of November 16, 2026, the Balanced portfolio held 25 units of ORBT. Using its latest available close of $164.93 on November 2, the position was worth $4,123.25.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## How I Know These Numbers Are Right
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT COUNT(*) AS trade_count
        FROM trades
        WHERE trade_date BETWEEN DATE '{as_of}' - INTERVAL '29 days'
                             AND DATE '{as_of}'
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Counting directly from trades gives 19, matching the sum of the Q1 portfolio counts: 9 + 5 + 5.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT t.trade_id
        FROM trades AS t
        WHERE NOT EXISTS (
            SELECT 1
            FROM closing_prices AS c
            WHERE c.asset_id = t.asset_id
              AND c.price_date = t.trade_date
        )
        ORDER BY t.trade_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The NOT EXISTS check found trades 31 and 32, the same two exceptions as the Q7 LEFT JOIN
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Working With the Agent
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    the LEFT JOIN found the two missing prices my documented in Part A, and a separate NOT EXISTS query returned the same trade IDs.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reading It Back

    For question 3, I expect 360 rows before grouping. I’m using November 16, 2026 as my as_of date, and I expect all 360 trades to have happened on or before that date. Each trade matches exactly one portfolio and one asset, so the joins keep one row per trade.
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT COUNT(*) AS rows_before_grouping
        FROM holding_movements AS h
        JOIN portfolios AS p ON p.portfolio_id = h.portfolio_id
        JOIN assets AS a ON a.asset_id = h.asset_id
        WHERE h.trade_date <= DATE '{as_of}'
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The joins returned 360 rows before grouping, matching my prediction. All 360 trades were included, and each matched one portfolio and one asset. In the final result, each row shows one asset that a portfolio still holds and how many units remain as of November 16, 2026.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Going Further
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Balanced’s ORBT position used a close 14 calendar days before the valuation date.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Time Spent

    4h
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
