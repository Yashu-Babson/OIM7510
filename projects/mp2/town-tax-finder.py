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


if __name__ == "__main__":
    app.run()
