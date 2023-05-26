from flask import Flask, jsonify, request
import csv

app = Flask(__name__)

@app.route('/parse', methods=["GET"])
def parse():

    try:
        file = request.args.get("file")
        product = request.args.get("product")

        with open("/usr/data/app/" + file, 'r') as csv_file:

            reader = csv.reader(csv_file)
            # extract fields through the first row
            header = next(reader)

            if header[0] != "product" or header[1] != "amount":
                return jsonify({"file": file, "error": "Input file not in CSV foramt."}), 400
        
            total = 0
            for row in reader:
                if (row[0] == product):
                    total += int(0 if row[1] == "" else row[1])
    
        return jsonify({"sum": total})

    except csv.Error as e:
        return jsonify({"file": file, "error": "Input file not in CSV format."}), 400
    except Exception as e:
        return jsonify({"error: {}".format(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)