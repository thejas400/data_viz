import os
import csv
import sqlite3

from flask import Flask, render_template_string, request, redirect, jsonify


app = Flask(__name__)

DB_FILE = "financials.db"
CSV_FILE = "data.csv"


def init_db():
    """Initialize the SQLite schema and populate it from data.csv."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS corporate_financials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Year INTEGER,
            Company TEXT,
            Category TEXT,
            Market_Cap REAL,
            Revenue REAL,
            Gross_Profit REAL,
            Net_Income REAL,
            EPS REAL,
            EBITDA REAL,
            Equity REAL,
            Operating_Cash_Flow REAL,
            Investing_Cash_Flow REAL,
            Financial_Cash_Flow REAL,
            Current_Ratio REAL,
            Debt_Equity_Ratio REAL,
            ROE REAL,
            ROA REAL,
            ROI REAL,
            Net_Profit_Margin REAL,
            Free_Cash_Flow_Per_Share REAL,
            Tangible_Equity_Return REAL,
            Employees INTEGER,
            Inflation_Rate REAL
        )
        """
    )

    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM corporate_financials")

    if cursor.fetchone()[0] == 0 and os.path.exists(CSV_FILE):
        print("Populating SQLite Database from raw dataset...")

        with open(CSV_FILE, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)

            # Skip CSV header row
            next(reader, None)

            for row in reader:
                # The database requires 23 CSV fields
                if not row or len(row) < 23:
                    continue

                processed_row = [
                    int(row[0]),
                    row[1].strip(),
                    row[2].strip(),
                    float(row[3]) if row[3] else 0.0,
                    float(row[4]) if row[4] else 0.0,
                    float(row[5]) if row[5] else 0.0,
                    float(row[6]) if row[6] else 0.0,
                    float(row[7]) if row[7] else 0.0,
                    float(row[8]) if row[8] else 0.0,
                    float(row[9]) if row[9] else 0.0,
                    float(row[10]) if row[10] else 0.0,
                    float(row[11]) if row[11] else 0.0,
                    float(row[12]) if row[12] else 0.0,
                    float(row[13]) if row[13] else 0.0,
                    float(row[14]) if row[14] else 0.0,
                    float(row[15]) if row[15] else 0.0,
                    float(row[16]) if row[16] else 0.0,
                    float(row[17]) if row[17] else 0.0,
                    float(row[18]) if row[18] else 0.0,
                    float(row[19]) if row[19] else 0.0,
                    float(row[20]) if row[20] else 0.0,
                    int(row[21]) if row[21] else 0,
                    float(row[22]) if row[22] else 0.0,
                ]

                cursor.execute(
                    """
                    INSERT INTO corporate_financials (
                        Year,
                        Company,
                        Category,
                        Market_Cap,
                        Revenue,
                        Gross_Profit,
                        Net_Income,
                        EPS,
                        EBITDA,
                        Equity,
                        Operating_Cash_Flow,
                        Investing_Cash_Flow,
                        Financial_Cash_Flow,
                        Current_Ratio,
                        Debt_Equity_Ratio,
                        ROE,
                        ROA,
                        ROI,
                        Net_Profit_Margin,
                        Free_Cash_Flow_Per_Share,
                        Tangible_Equity_Return,
                        Employees,
                        Inflation_Rate
                    )
                    VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                    """,
                    processed_row,
                )

        conn.commit()

    conn.close()


# Run database setup immediately on launch
init_db()


# -------------------------------------------------------------------
# WEB DASHBOARD UI
# -------------------------------------------------------------------

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Financial Control Hub</title>

    <script src="https://tailwindcss.com"></script>
</head>

<body class="bg-gray-900 text-gray-100 min-h-screen">

    <!-- Navigation -->
    <nav class="bg-gray-800 border-b border-gray-700 px-6 py-4 shadow-xl">
        <div class="max-w-7xl mx-auto flex justify-between items-center">

            <h1 class="text-2xl font-black text-indigo-400 tracking-wider">
                📦 FLASK FIN-HUB
            </h1>

            <span
                class="bg-green-500/20 text-green-400 px-3 py-1 rounded-full text-xs font-semibold uppercase animate-pulse">
                ● System Connected
            </span>

        </div>
    </nav>


    <!-- Main Content -->
    <main
        class="max-w-7xl mx-auto px-4 py-8 grid grid-cols-1 lg:grid-cols-3 gap-8"
    >

        <!-- Data Intake Terminal -->
        <section
            class="bg-gray-800 p-6 rounded-2xl border border-gray-700 shadow-2xl h-fit"
        >

            <h2
                class="text-xl font-bold mb-4 text-white border-b border-gray-700 pb-2"
            >
                ✏️ Data Intake Terminal
            </h2>

            <form
                action="/add-record"
                method="POST"
                class="space-y-4"
            >

                <!-- Year / Company -->
                <div class="grid grid-cols-2 gap-3">

                    <div>
                        <label class="block text-xs uppercase font-bold mb-1">
                            Year
                        </label>

                        <input
                            type="number"
                            name="Year"
                            required
                            class="w-full bg-gray-900 border border-gray-700 rounded p-2 text-white"
                        >
                    </div>

                    <div>
                        <label class="block text-xs uppercase font-bold mb-1">
                            Company Ticker
                        </label>

                        <input
                            type="text"
                            name="Company"
                            required
                            class="w-full bg-gray-900 border border-gray-700 rounded p-2 text-white"
                        >
                    </div>

                </div>


                <!-- Category -->
                <div>
                    <label class="block text-xs uppercase font-bold mb-1">
                        Sector Category
                    </label>

                    <input
                        type="text"
                        name="Category"
                        required
                        class="w-full bg-gray-900 border border-gray-700 rounded p-2 text-white"
                    >
                </div>


                <!-- Market Cap / Revenue -->
                <div class="grid grid-cols-2 gap-3">

                    <div>
                        <label class="block text-xs uppercase font-bold mb-1">
                            Market Cap ($B)
                        </label>

                        <input
                            type="number"
                            step="any"
                            name="Market_Cap"
                            required
                            class="w-full bg-gray-900 border border-gray-700 rounded p-2 text-white"
                        >
                    </div>

                    <div>
                        <label class="block text-xs uppercase font-bold mb-1">
                            Revenue
                        </label>

                        <input
                            type="number"
                            step="any"
                            name="Revenue"
                            required
                            class="w-full bg-gray-900 border border-gray-700 rounded p-2 text-white"
                        >
                    </div>

                </div>


                <!-- Gross Profit / Net Income -->
                <div class="grid grid-cols-2 gap-3">

                    <div>
                        <label class="block text-xs uppercase font-bold mb-1">
                            Gross Profit
                        </label>

                        <input
                            type="number"
                            step="any"
                            name="Gross_Profit"
                            required
                            class="w-full bg-gray-900 border border-gray-700 rounded p-2 text-white"
                        >
                    </div>

                    <div>
                        <label class="block text-xs uppercase font-bold mb-1">
                            Net Income
                        </label>

                        <input
                            type="number"
                            step="any"
                            name="Net_Income"
                            required
                            class="w-full bg-gray-900 border border-gray-700 rounded p-2 text-white"
                        >
                    </div>

                </div>


                <!-- EPS / EBITDA -->
                <div class="grid grid-cols-2 gap-3">

                    <div>
                        <label class="block text-xs uppercase font-bold mb-1">
                            EPS
                        </label>

                        <input
                            type="number"
                            step="any"
                            name="EPS"
                            required
                            class="w-full bg-gray-900 border border-gray-700 rounded p-2 text-white"
                        >
                    </div>

                    <div>
                        <label class="block text-xs uppercase font-bold mb-1">
                            EBITDA
                        </label>

                        <input
                            type="number"
                            step="any"
                            name="EBITDA"
                            required
                            class="w-full bg-gray-900 border border-gray-700 rounded p-2 text-white"
                        >
                    </div>

                </div>


                <!-- Submit -->
                <button
                    type="submit"
                    class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold p-3 rounded-lg mt-2 shadow-lg transition"
                >
                    ⚡ Inject Into SQLite DB
                </button>

            </form>

        </section>


        <!-- Live Database Monitor -->
        <section
            class="lg:col-span-2 bg-gray-800 p-6 rounded-2xl border border-gray-700 shadow-2xl flex flex-col"
        >

            <div class="flex justify-between items-center mb-4">

                <h2 class="text-xl font-bold text-white">
                    📊 Live View Database Records
                </h2>

                <a
                    href="/api/data"
                    target="_blank"
                    class="text-xs text-indigo-400 bg-indigo-500/10 px-3 py-1.5 rounded-lg border border-indigo-500/20 hover:bg-indigo-500/20 transition"
                >
                    🔗 Open Power BI Stream
                </a>

            </div>


            <!-- Table -->
            <div class="overflow-x-auto max-h-[500px]">

                <table class="w-full text-left">

                    <thead>

                        <tr
                            class="bg-gray-900 sticky top-0 border-b border-gray-700 text-gray-400 text-xs font-semibold uppercase"
                        >

                            <th class="p-3">Year</th>
                            <th class="p-3">Company</th>
                            <th class="p-3">Sector</th>
                            <th class="p-3">Market Cap</th>
                            <th class="p-3">Revenue</th>
                            <th class="p-3">Net Income</th>

                        </tr>

                    </thead>


                    <tbody class="divide-y divide-gray-700">

                        {% for r in records %}

                        <tr
                            class="hover:bg-gray-700/40 transition text-sm text-gray-300"
                        >

                            <td class="p-3 font-semibold text-white">
                                {{ r[1] }}
                            </td>

                            <td class="p-3 text-indigo-400 font-mono font-bold">
                                {{ r[2] }}
                            </td>

                            <td class="p-3">
                                <span
                                    class="bg-gray-900 px-2 py-1 rounded text-xs text-gray-400"
                                >
                                    {{ r[3] }}
                                </span>
                            </td>

                            <td class="p-3 text-green-400 font-mono">
                                ${{ r[4] }}B
                            </td>

                            <td class="p-3 font-mono">
                                {{ r[5] }}
                            </td>

                            <td
                                class="p-3 font-mono
                                {% if r[7]|float < 0 %}
                                    text-red-400
                                {% else %}
                                    text-emerald-400
                                {% endif %}"
                            >
                                {{ r[7] }}
                            </td>

                        </tr>

                        {% endfor %}

                    </tbody>

                </table>

            </div>

        </section>

    </main>

</body>

</html>
"""


# -------------------------------------------------------------------
# DASHBOARD ROUTE
# -------------------------------------------------------------------

@app.route("/")
def dashboard_home():
    """Display the financial dashboard."""

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM corporate_financials
        ORDER BY Year DESC, Company ASC
        """
    )

    records = cursor.fetchall()

    conn.close()

    return render_template_string(
        HTML_TEMPLATE,
        records=records,
    )


# -------------------------------------------------------------------
# ADD RECORD ROUTE
# -------------------------------------------------------------------

@app.route("/add-record", methods=["POST"])
def append_record():
    """Add a new financial record to the SQLite database."""

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO corporate_financials (
            Year,
            Company,
            Category,
            Market_Cap,
            Revenue,
            Gross_Profit,
            Net_Income,
            EPS,
            EBITDA,
            Equity,
            Operating_Cash_Flow,
            Investing_Cash_Flow,
            Financial_Cash_Flow,
            Current_Ratio,
            Debt_Equity_Ratio,
            ROE,
            ROA,
            ROI,
            Net_Profit_Margin,
            Free_Cash_Flow_Per_Share,
            Tangible_Equity_Return,
            Employees,
            Inflation_Rate
        )
        VALUES (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.5,
            15.0,
            5.0,
            10.0,
            12.0,
            1.0,
            15.0,
            5000,
            3.0
        )
        """,
        (
            int(request.form["Year"]),
            request.form["Company"].upper(),
            request.form["Category"],
            float(request.form["Market_Cap"]),
            float(request.form["Revenue"]),
            float(request.form["Gross_Profit"]),
            float(request.form["Net_Income"]),
            float(request.form["EPS"]),
            float(request.form["EBITDA"]),
        ),
    )

    conn.commit()
    conn.close()

    return redirect("/")


# -------------------------------------------------------------------
# POWER BI / JSON API ROUTE
# -------------------------------------------------------------------

@app.route("/api/data", methods=["GET"])
def get_bi_stream():
    """
    Return all corporate financial records as JSON.

    This endpoint can be used as a Web source in Power BI.
    """

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM corporate_financials
        """
    )

    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()

    conn.close()

    # Convert database rows into JSON-compatible dictionaries
    data_stream = [
        dict(zip(columns, row))
        for row in rows
    ]

    return jsonify(data_stream)


# -------------------------------------------------------------------
# APPLICATION ENTRY POINT
# -------------------------------------------------------------------

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8000,
        debug=True,
    )