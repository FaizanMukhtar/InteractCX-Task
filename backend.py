from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)
baseURL = 'https://orderstatusapi-dot-organization-project-311520.uc.r.appspot.com/api/getOrderStatus'

@app.route('/', methods=['GET'])
def home():
    return "working"

@app.route('/', methods=['POST'])
def process_request():
    data = request.get_json()
    order_id = data.get('order_id', '')
    result = requests.post(baseURL, json={"orderId": order_id})
    result_data = result.json()
    print(result_data)
    shipmentDate = result_data.get('shipmentDate', '')
    shipmentDate_obj = datetime.strptime(shipmentDate, '%Y-%m-%dT%H:%M:%S.%fZ')
    newshipmentDate = shipmentDate_obj.strftime('%A, %d %b %Y')
    res = {
        "fulfillmentText": f"{newshipmentDate}",
        "fulfillmentMessages": [{
            "text": {
                "text": [f"{newshipmentDate}"]
            }
        }]
    }
    return jsonify(res)

if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 3000)))