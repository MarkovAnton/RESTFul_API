from flask import Flask, json
from flask_restful import Api, Resource, reqparse
import random

app = Flask(__name__)
api = Api()

promos = []


class Main(Resource):
    def post(self):
        participants = []
        prizes = []
        promo_id = len(promos) + 1
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("description", type=str)
        params = parser.parse_args()
        for promo in promos:
            if promo["name"] == params["name"]:
                return f'Promo with name {params["name"]} already exists', 400
        promo = {
            "id": promo_id,
            "name": params["name"],
            "description": params["description"],
            "participants": participants,
            "prizes": prizes
        }
        promos.append(promo)
        return promo_id, 201

    def get(self):
        promos_no_part_prizes = []
        for promo in promos:
            promo = {
                "id": promo["id"],
                "name": promo["name"],
                "description": promo["description"]
            }
            promos_no_part_prizes.append(promo)
        return promos_no_part_prizes, 200


class Main_id(Resource):
    def get(self, promo_id):
        for promo in promos:
            if promo["id"] == promo_id:
                return promo, 200
        return "Promo not found", 404

    def put(self, promo_id):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("description", type=str)
        params = parser.parse_args()
        for promo in promos:
            if promo_id == promo["id"]:
                promo["name"] = params["name"]
                promo["description"] = params["description"]
                return promo, 200

        promo = {
            "id": promo_id,
            "name": params["name"],
            "description": params["description"]
        }
        promos.append(promo)
        return promo, 201

    def delete(self, promo_id):
        global promos
        promos = [promo for promo in promos if promo["id"] != promo_id]
        return f'Promo with id {id} is deleted.', 200


class Main_participant(Resource):
    def post(self, promo_id):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        params = parser.parse_args()
        for promo in promos:
            if promo["id"] == promo_id:
                part_id = len(promo["participants"]) + 1
                for participant in promo["participants"]:
                    if participant["name"] == params["name"]:
                        return f'Participant with name {params["name"]} already exists', 400
                participant = {
                    "id": part_id,
                    "name": params["name"]
                }
                promo["participants"].append(participant)
                return part_id, 201


class Main_participant_id(Resource):
    def delete(self, promo_id, participant_id):
        for promo in promos:
            if promo["id"] == promo_id:
                promo["participants"] = [participant for participant in promo["participants"] 
                                         if participant["id"] != participant_id]
                return f'Participant with id {participant_id} is deleted.', 200


class Main_prize(Resource):
    def post(self, promo_id):
        parser = reqparse.RequestParser()
        parser.add_argument("description", type=str)
        params = parser.parse_args()
        for promo in promos:
            if promo["id"] == promo_id:
                prize_id = len(promo["prizes"]) + 1
                for prize in promo["prizes"]:
                    if prize["description"] == params["description"]:
                        return f'Prize with description {params["description"]} already exists', 400
                prize = {
                    "id": prize_id,
                    "description": params["description"]
                }
                promo["prizes"].append(prize)
                return prize_id, 201


class Main_prize_id(Resource):
    def delete(self, promo_id, prize_id):
        for promo in promos:
            if promo["id"] == promo_id:
                promo["prizes"] = [prize for prize in promo["prizes"] if prize["id"] != prize_id]
                return f'Prize with id {prize_id} is deleted.', 200


class Main_raffle(Resource):
    def post(self, promo_id):
        raffles = []
        for promo in promos:
            if promo["id"] == promo_id:
                prizes = promo["prizes"]
                if len(promo["participants"]) == len(promo["prizes"])\
                        and (len(promo["participants"]) != 0 and len(promo["prizes"]) != 0):
                    for participant in promo["participants"]:
                        prize_rand = random.choice(prizes)
                        prizes = [prize for prize in prizes if prize != prize_rand]
                        raffle = {
                            "winner": participant,
                            "prize": prize_rand
                        }
                        raffles.append(raffle)
                else:
                    return f'It is not possible to draw for the promotion id {promo_id}.', 409
        return raffles, 200


api.add_resource(Main, "/promo")
api.add_resource(Main_id, "/promo/<int:promo_id>")
api.add_resource(Main_participant, "/promo/<int:promo_id>/participant")
api.add_resource(Main_participant_id, "/promo/<int:promo_id>/participant/<int:participant_id>")
api.add_resource(Main_prize, "/promo/<int:promo_id>/prize")
api.add_resource(Main_prize_id, "/promo/<int:promo_id>/prize/<int:prize_id>")
api.add_resource(Main_raffle, "/promo/<int:promo_id>/raffle")
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host="127.0.0.1")

