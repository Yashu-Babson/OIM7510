import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question
    Who will use this tool? What decision will it help them make?

    A: Those families choosing towns within their home budget and annual property-tax limit would like to use this tool. It can help them find towns with the lowest average property-tax bill, among those meeting both limits.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    1. Fetch the towns history data of middlesex, using fiscal year of 2026;
    2. Rank and Filter the towns that have avg single family value dollars within $700000 and annual tax bill below $8000;
    3. Sort qualifying towns by average annual tax bill, lowest first, before highlighting three towns.
    4. Highlight the first 3 town names as suggestion;
    5. Save fetched records to csv.


    ## Questions to aswer:
    ### Functions
    What functions will I need? What goes into each, and what comes out?

    1.Get the county's towns:

    Input: county name;

    Output: a list of towns in that county, including each town's indentifying code.

    2. Get one town's history

    Input: one town's indentifying code
    Output: that town's yearly records, from which select 2026


    ### API addresses
    Which addresses will my functions request?

    https://oim.zhili.dev/ma/towns?county=Middlesex

    https://oim.zhili.dev/ma/towns/{dor_code}/history

    ### Complete data
    How will I know I collected every town?

    A: Number of towns collected = total towns reported by the API

    ### Verification
    Which two numbers will I compare to check my result?

    A: I would check total number of towns collected with total towns reported by the API to see if it matches.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs
    """)
    return


@app.cell
def _():
    county = "Middlesex"
    budget_dollars = 700000
    tax_limit_dollars = 8000
    fiscal_year = 2026
    return budget_dollars, county, fiscal_year, tax_limit_dollars


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work
    """)
    return


@app.cell
def _():
    import requests

    return (requests,)


@app.cell
def _(requests):
    def get_county_towns(county_name):
        towns = []
        page = 1

        while True:
            response = requests.get(
                "https://oim.zhili.dev/ma/towns",
                params={
                    "county": county_name,
                    "page": page,
                    "per_page": 100,
                },
                timeout=20,
            )
            response.raise_for_status()
            reply = response.json()
            page_towns = reply["items"]

            for town_record in page_towns:
                towns.append(town_record)

            if len(page_towns) < 100:
                break

            page += 1

        return towns

    return (get_county_towns,)


@app.cell
def _(county, get_county_towns):
    county_towns = get_county_towns(county)

    print("Towns collected:", len(county_towns))
    print(county_towns[0])
    return (county_towns,)


@app.cell
def _(requests):
    def get_town_history(dor_code):
        response = requests.get(
            f"https://oim.zhili.dev/ma/towns/{dor_code}/history",
            timeout=20,
        )
        response.raise_for_status()
        reply = response.json()

        return reply["years"]

    return (get_town_history,)


@app.cell
def _(county_towns, fiscal_year, get_town_history):
    first_town_history = get_town_history(
        county_towns[0]["dor_code"]
    )

    for _year_record in first_town_history:
        if _year_record["fiscal_year"] == fiscal_year:
            print(_year_record)
    return


@app.cell
def _(county_towns, fiscal_year, get_town_history):
    town_year_records = []
    missing_year_towns = []

    for _town in county_towns:
        _history = get_town_history(_town["dor_code"])
        _found_year = False

        for _record in _history:
            if _record["fiscal_year"] == fiscal_year:
                _town_record = {
                    "name": _town["name"],
                    "dor_code": _town["dor_code"],
                    "fiscal_year": _record["fiscal_year"],
                    "average_single_family_value_dollars":
                        _record["average_single_family_value_dollars"],
                    "residential_rate_per_thousand":
                        _record["residential_rate_per_thousand"],
                    "average_single_family_bill_dollars":
                        _record["average_single_family_bill_dollars"],
                }

                town_year_records.append(_town_record)
                _found_year = True
                break

        if not _found_year:
            missing_year_towns.append(_town["name"])

    print("Towns collected:", len(county_towns))
    print("Towns with selected-year records:", len(town_year_records))
    print("Towns missing that year:", missing_year_towns)
    return (town_year_records,)


@app.cell
def _(budget_dollars, tax_limit_dollars, town_year_records):
    qualifying_towns = []
    missing_value_towns = []

    for _town_data in town_year_records:
        _home_value = _town_data["average_single_family_value_dollars"]
        _tax_bill = _town_data["average_single_family_bill_dollars"]

        if _home_value is None or _tax_bill is None:
            missing_value_towns.append(_town_data["name"])
            continue

        if _home_value <= budget_dollars and _tax_bill < tax_limit_dollars:
            qualifying_towns.append(_town_data)

    print("Qualifying towns:", len(qualifying_towns))
    print("Towns missing home value or bill:", missing_value_towns)
    return (qualifying_towns,)


@app.cell
def _(qualifying_towns):
    def get_tax_bill(town_record):
        return town_record["average_single_family_bill_dollars"]


    ranked_towns = sorted(
        qualifying_towns,
        key=get_tax_bill,
    )

    for _ranked_town in ranked_towns:
        print(
            _ranked_town["name"],
            _ranked_town["average_single_family_bill_dollars"],
        )
    return (ranked_towns,)


@app.cell
def _(county, county_towns, fiscal_year, mo, town_year_records):
    import json

    _data_folder = mo.notebook_dir() / "data"
    _data_folder.mkdir(parents=True, exist_ok=True)

    # Save the town records returned by our fetching function.
    _towns_file = _data_folder / f"{county.lower()}-towns.json"

    with _towns_file.open("w", encoding="utf-8") as _file:
        json.dump(county_towns, _file, indent=2)

    # Save the selected-year records used for our answer.
    _year_file = (
        _data_folder
        / f"{county.lower()}-{fiscal_year}-tax-records.json"
    )

    with _year_file.open("w", encoding="utf-8") as _file:
        json.dump(town_year_records, _file, indent=2)

    print("Saved:", _towns_file)
    print("Saved:", _year_file)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer
    """)
    return


@app.cell
def _(county, fiscal_year, ranked_towns):
    print(f"{county} County — fiscal year {fiscal_year}")
    print(
        f"{'Town':<20}"
        f"{'Avg home ($)':>16}"
        f"{'Rate ($/1,000)':>18}"
        f"{'Avg bill ($)':>16}"
    )
    print("-" * 70)

    for _answer_town in ranked_towns:
        _answer_name = _answer_town["name"]
        _answer_value = _answer_town["average_single_family_value_dollars"]
        _answer_rate = _answer_town["residential_rate_per_thousand"]
        _answer_bill = _answer_town["average_single_family_bill_dollars"]

        _rate_text = "N/A"
        if _answer_rate is not None:
            _rate_text = f"{_answer_rate:.2f}"

        print(
            f"{_answer_name:<20}"
            f"{_answer_value:>16,.0f}"
            f"{_rate_text:>18}"
            f"{_answer_bill:>16,.0f}"
        )
    return


@app.cell
def _(budget_dollars, county, fiscal_year, ranked_towns, tax_limit_dollars):
    if ranked_towns:
        _best_town = ranked_towns[0]

        print(
            f"In fiscal year {fiscal_year}, "
            f"{len(ranked_towns)} towns in {county} County meet "
            f"the ${budget_dollars:,.0f} average-home-value budget "
            f"and annual average tax bill below ${tax_limit_dollars:,.0f}; "
            f"{_best_town['name']} has the lowest average bill "
            f"at ${_best_town['average_single_family_bill_dollars']:,.0f}, "
            f"with an average home value of "
            f"${_best_town['average_single_family_value_dollars']:,.0f}."
        )
    else:
        print(
            f"No towns in {county} County meet both limits "
            f"for fiscal year {fiscal_year}."
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Verification
    """)
    return


@app.cell
def _(county, county_towns, requests):
    _check_response = requests.get(
        "https://oim.zhili.dev/ma/towns",
        params={"county": county, "page": 1, "per_page": 1},
        timeout=20,
    )
    _check_response.raise_for_status()
    _check_reply = _check_response.json()

    _api_total = _check_reply["pagination"]["total"]
    _collected_total = len(county_towns)

    print("Towns collected:", _collected_total)
    print("API reported total:", _api_total)
    print("Counts match:", _collected_total == _api_total)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I compared the number of collected towns with the API’s reported total for Middlesex. Both were 54, supporting that my collection includes the expected number of towns.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Explain Two Functions

    ### get_county_towns(county_name)

    This function includes 5 steps, start from input, it receives a county name, such as "Middlesex"; then fetching requests pages of towns form the API; then collecting, adds each returned town to the town list; and stopping once a page contains fewer tan 100 towns; Finally the output, it returns the collected list of town records.

    ### get_town_history(dor_code)

    This function includes 5 steps, start from input of one town's indentifying code, such as "002"for Acton; then the request, it inserts the code into the history API address; then an error check, raise_for_status() stops the function if the HTTP request fails; then conversion, .json()converts the response into Python data; finally the output, reply["years"], the list of yearly records.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Change an Input

    Test lowering the home-value budget from $700,000 to $600,000, keeping the other inputs unchanged.

    My prediction: by lowering the home-vale from 700k to 600k, the number of qualifying towns can decrease or stay the same. It'll decrease only if some currently qualifying towns have average home values above 600k. Lowest till town remains only if its average home value is at or below 600k, cuz the lowest tax bill doesn't necessarily mena the lowest home value.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


if __name__ == "__main__":
    app.run()
