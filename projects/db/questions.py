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


@app.cell
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


if __name__ == "__main__":
    app.run()
