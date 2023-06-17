import os
from flask import Flask, jsonify, request
import csv

app = Flask(__name__)

@app.route('/parse', methods=["GET"])
def parse():

    try:
        file = request.args.get("file")
        product = request.args.get("product")

        directory_path = "/jiaye_PV_dir"

        file_path = os.path.join(directory_path, file)

        with open(file_path, 'r') as csv_file:

            reader = csv.reader(csv_file)
            # extract fields through the first row
            header = next(reader)

            if 'product' not in header[0] or 'amount' not in header[1]:

                return jsonify({"file": file, "error": "Input file not in CSV format."}), 400
        
            total = 0
            for row in reader:
                if (row[0] == product):
                    total += int(0 if row[1] == "" else row[1])
    
        return jsonify({"sum": str(total)})

    except csv.Error as e:
        return jsonify({"file": file, "error": "Input file not in CSV format."}), 400
    except Exception as e:
        return jsonify({"file": file, "error": "Input file not in CSV format."}), 500

if __name__ == "__main__":
    app.run(debug=True)