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
    mo.md(r"""
    ## Reading It Back

    For question 3, I expect 360 rows before grouping. I’m using November 16, 2026 as my as_of date, and I expect all 360 trades to have happened on or before that date. Each trade matches exactly one portfolio and one asset, so the joins keep one row per trade.
    """)
    return


if __name__ == "__main__":
    app.run()
