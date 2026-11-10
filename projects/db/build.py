import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell
def _():
    import duckdb
    import marimo as mo

    project_dir = mo.notebook_dir()
    database = project_dir / "database.duckdb"
    data_dir = project_dir / "data"

    # Rebuild the generated database from the CSVs each time.
    database.unlink(missing_ok=True)

    with duckdb.connect(database) as con:
        con.execute("""
            CREATE TABLE members (
                member_id INTEGER PRIMARY KEY,
                first_name VARCHAR NOT NULL,
                last_name VARCHAR NOT NULL,
                email VARCHAR NOT NULL,
                class_year INTEGER NOT NULL,
                join_date DATE NOT NULL
            )
        """)
        con.execute("""
            CREATE TABLE portfolios (
                portfolio_id INTEGER PRIMARY KEY,
                member_id INTEGER NOT NULL REFERENCES members(member_id),
                name VARCHAR NOT NULL,
                created_date DATE NOT NULL,
                strategy VARCHAR
            )
        """)
        con.execute("""
            CREATE TABLE assets (
                asset_id INTEGER PRIMARY KEY,
                ticker VARCHAR NOT NULL,
                name VARCHAR NOT NULL,
                asset_type VARCHAR NOT NULL CHECK (asset_type IN ('stock', 'ETF', 'crypto')),
                sector VARCHAR
            );

            CREATE TABLE closing_prices (
                asset_id INTEGER REFERENCES assets(asset_id),
                price_date DATE,
                close_price DECIMAL(18, 4) NOT NULL CHECK (close_price > 0),
                PRIMARY KEY (asset_id, price_date)
            );

            CREATE TABLE ticker_history (
                asset_id INTEGER REFERENCES assets(asset_id),
                effective_from DATE,
                ticker VARCHAR NOT NULL,
                PRIMARY KEY (asset_id, effective_from)
            );

            CREATE TABLE trades (
                trade_id INTEGER PRIMARY KEY,
                portfolio_id INTEGER NOT NULL REFERENCES portfolios(portfolio_id),
                asset_id INTEGER NOT NULL REFERENCES assets(asset_id),
                trade_date DATE NOT NULL,
                side VARCHAR NOT NULL CHECK (side IN ('BUY', 'SELL')),
                quantity DECIMAL(18, 6) NOT NULL CHECK (quantity > 0),
                trade_price DECIMAL(18, 4) NOT NULL CHECK (trade_price > 0),
                fee DECIMAL(18, 4) NOT NULL DEFAULT 0 CHECK (fee >= 0),
                UNIQUE (portfolio_id, asset_id, trade_date)
            );
        """)
    
        # Load parent tables before the tables that reference them.
        tables = ("members", "portfolios", "assets", "closing_prices",
                  "ticker_history", "trades")

        for table in tables:
            con.execute(
                f"INSERT INTO {table} SELECT * FROM read_csv(?, header=true)",
                [str(data_dir / f"{table}.csv")],
            )

        row_counts = []
        for table in tables:
            count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            row_counts.append(f"- **{table}:** {count:,}")

    mo.md("## Row Counts\n\n" + "\n".join(row_counts))
    return database, duckdb, mo


@app.cell
def _(database, duckdb, mo):
    with duckdb.connect(database) as _con:
        _con.execute("BEGIN TRANSACTION")
        try:
            _con.execute("""
                INSERT INTO trades
                VALUES (9999, 2, 1, DATE '2025-11-03', 'BUY', 0, 88.65, 0)
            """)
            _message = "Unexpected: DuckDB accepted a trade with zero quantity."
        except duckdb.ConstraintException as _error:
            _message = f"DuckDB refused the trade: {_error}"
        finally:
            _con.execute("ROLLBACK")

    mo.md(f"## Row It Refuses\n\n{_message}")
    return


@app.cell
def _(database, duckdb):
    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            _result = _con.execute(sql)
            _columns = [column[0] for column in _result.description]
            return [
                dict(zip(_columns, row))
                for row in _result.fetchall()
            ]

    return (ask,)


@app.cell
def _(mo):
    mo.md("""
    ## Answers I Already Knew
    """)
    return


@app.cell
def _(ask):
    # Prediction: member 1 owns two portfolios.
    ask("""
        SELECT COUNT(*) AS portfolio_count
        FROM portfolios
        WHERE member_id = 1
    """)
    return


@app.cell
def _(ask):
    # Prediction: NOVA (asset 12) has never been traded.
    ask("""
        SELECT asset_id, ticker
        FROM assets
        WHERE asset_id NOT IN (
            SELECT asset_id FROM trades
        )
    """)
    return


@app.cell
def _(ask):
    # Prediction: asset 1 has two ticker-history records.
    ask("""
        SELECT asset_id, effective_from, ticker
        FROM ticker_history
        WHERE asset_id = 1
        ORDER BY effective_from
    """)
    return


if __name__ == "__main__":
    app.run()
