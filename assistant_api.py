from flask import Flask, request, jsonify
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Azure SQL connection
conn_str = (
    f"Driver={{ODBC Driver 18 for SQL Server}};"
    f"Server={os.getenv('AZURE_SERVER')};"
    f"Database={os.getenv('AZURE_DB')};"
    f"Uid={os.getenv('AZURE_USER')};"
    f"Pwd={os.getenv('AZURE_PASSWORD')};"
    "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
)

@app.route("/ask", methods=["POST"])
def answer():
    user_input = request.json.get("query", "").lower()
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    if "payroll" in user_input:
        cursor.execute("SELECT SUM(Salary) FROM HRData")
        total = cursor.fetchone()[0]
        return jsonify(answer=f"Total payroll is ${total:.2f}")

    elif "how many" in user_input and "r&d" in user_input:
        cursor.execute("SELECT COUNT(*) FROM HRData WHERE Department = 'R&D'")
        count = cursor.fetchone()[0]
        return jsonify(answer=f"There are {count} employees in R&D.")

    elif "satisfaction" in user_input and "sales" in user_input:
        cursor.execute("SELECT AVG(Satisfaction) FROM HRData WHERE Department = 'Sales'")
        avg = cursor.fetchone()[0]
        return jsonify(answer=f" Average satisfaction in Sales is {avg:.2f}")

    else:
        return jsonify(answer=" Sorry, I don't understand that question.")

if __name__ == "__main__":
    app.run(debug=True, port=5002)