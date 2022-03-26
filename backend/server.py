from flask import Flask
from flask_restful import Resource, Api
from db import create_table, insert_values, get_filter_results

app = Flask(__name__)
api = Api(app)

class filter_professions(Resource):
    def get(self, stress_anxiete, sommeil, attention, alimentation, social):
        values = {
            'Stress/Anxiete': stress_anxiete,
            'Sommeil': sommeil,
            'Attention': attention,
            'Alimentation': alimentation,
            'Social (conflit)': social
        }

        return get_filter_results(values)[0]

class filter_practitioners(Resource):
    def get(self, stress_anxiete, sommeil, attention, alimentation, social):
        values = {
            'Stress/Anxiete': stress_anxiete,
            'Sommeil': sommeil,
            'Attention': attention,
            'Alimentation': alimentation,
            'Social (conflit)': social
        }

        return get_filter_results(values)[1]

api.add_resource(filter_professions, '/professions/<string:stress_anxiete>/<string:sommeil>/<string:attention>/<string:alimentation>/<string:social>')
api.add_resource(filter_practitioners, '/professions/<string:stress_anxiete>/<string:sommeil>/<string:attention>/<string:alimentation>/<string:social>')

if __name__ == "__main__":
    create_table()
    insert_values()
    app.run(debug=True)