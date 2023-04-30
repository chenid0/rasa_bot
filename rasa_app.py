from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import requests

app = Flask(__name__)
api = Api(app)

class Chatbot(Resource):
    def post(self):
        data = request.get_json()
        response = requests.post("http://localhost:5005/webhooks/rest/webhook", json={"message": data["message"]}).json()
        return {"message": response[0]["text"]}

api.add_resource(Chatbot, "/api/messages")

if __name__ == "__main__":
    app.run(debug=True)
