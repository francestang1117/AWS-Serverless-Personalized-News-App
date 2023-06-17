import os
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


@app.route('/store-file', methods=["POST"])
def getData():

    file_name = None

    input = request.get_json()


    if 'file' not in input:
        return jsonify({"file": file_name, "error": "Invalid JSON input."})

    file_name = input["file"]

    if file_name == None:
        return jsonify({"file": file_name, "error": "Invalid JSON input."})
    
    content = input["data"]
    directory_path = "/jiaye_PV_dir"

    file_path = os.path.join(directory_path, file_name)
    
    try:

        with open(file_path, "w") as file:
            file.write(content)

        return jsonify({"file": file_name, "message": "Success."})

    except Exception as e:
        return jsonify({"file": file_name, "error": "Error while storing the file to the storage."})


@app.route('/calculate', methods=['POST'])
def getFile():

    file = None

    request_data = request.get_json()

    # validate file
    if 'file' not in request_data:
        return jsonify({"file": file, "error": "Invalid JSON input."})
    
    file = request_data["file"]
    product = request_data["product"]

    if not file:
        return jsonify({"file": file, "error": "Invalid JSON input."})
    
    if not os.path.isfile('/jiaye_PV_dir/' + file):
        return jsonify({"file": file, "error": "File not found."})

    params = {"file": file, "product": product}

    try:
        response = requests.get(url="http://app2-service:6001/parse", params=params)

        data = response.json()
        if data:
            if response.status_code == 200:
                return jsonify({"file": file, "sum": data["sum"]})
            
            if response.status_code == 400:
                return jsonify({"file": file, "error": data["error"]})
            
            if response.status_code == 500:
                return jsonify({"file": file, "error": data["error"]})
    
    except Exception as e:
        return jsonify({"file": file, "error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)