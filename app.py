from flask import Flask, jsonify, render_template, request
import csv
import subprocess
from flask_cors import CORS


app = Flask(__name__)

CORS(app)

@app.route('/data')
def serve_data():
    with open('results.csv', 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)

    # Filter out only the columns you want
    filtered_data = []
    for row in data:
        filtered_data.append({
            "checkbox": "",  # Add a dummy field for the checkbox
            "Timestamp": row["Timestamp"],
            "Source": row["Source"],
            "Job Title": row["Job Title"],
            "Description": row["Description"],
            "Hidden": row["Hidden"] == "1"  # Convert string to boolean
        })

    return jsonify(filtered_data)

@app.route('/update_hidden_state', methods=['POST'])
def update_hidden_state():
    hidden_rows = request.json.get('hiddenRows', [])
    with open('results.csv', 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)

    # Update the "Hidden" column based on the provided hidden rows
    for i, row in enumerate(data):
        row["Hidden"] = "1" if i in hidden_rows else "0"

    # Write the updated data back to the CSV
    with open('results.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    return jsonify({"message": "Hidden state updated successfully!"})

@app.route('/')
def index():
    return render_template('index.jinja2')

@app.route('/run_scraper', methods=['POST'])
def run_scraper():
    subprocess.call(["python", "scraper.py"])
    return jsonify({"message": "Script executed successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
