import os
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def getFile():

    try:
        request_data = request.get_json()
        file = request_data["file"]
        product = request_data["product"]

        # validate file
        if not file:
            return jsonify({"file": file, "error": "Invalid JSON input."})
    
        elif not os.path.isfile('/usr/data/app/' + file):
            return jsonify({"file": file, "error": "File not found"})

        params = {"file": file, "product": product}


        response = requests.get(url="http://webapp2:6001/parse", params=params)

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