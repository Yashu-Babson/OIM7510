import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    return


@app.cell
def _():
    print("Hello, playground")
    return


@app.cell
def _():
    orders = [
        {"OrderID": 10248, "ShipCountry": "France"},
        {"OrderID": 10249, "ShipCountry": "Germany"},
        {"OrderID": 10250, "ShipCountry": "France"},
    ]

    orders[1]
    return (orders,)


@app.cell
def _(orders):
    countries = []

    for _order in orders:
        _country = _order["ShipCountry"]
        countries.append(_country)

    countries
    return


@app.cell
def _():
    allowed_countries = {"China", "France", "USA", "Germany"}
    students = ["India", "France", "USA"]

    for _student in students:
        if _student in allowed_countries:
            print("Yes")
        else:
            print("No")
    return


@app.cell
def _():
    orders_by_id = {
        10248: {"total": 440.0},
        10249: {"total": 200.0},
    }

    orders_by_id[10248]["total"]  # 440.0
    return


@app.cell
def _():
    order_with_lines = {
        "order_id": 10248,
        "lines": [
            {"product": "Tea", "quantity": 2},
            {"product": "Honey", "quantity": 1},
        ],
    }

    order_with_lines["lines"][0]["product"]  # "Tea"
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
