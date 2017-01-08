# -*- coding: UTF-8 -*-


import configparser
import json
import flask
from service.CostGenerator import CostGenerator
import threading


PROP_FILE_NAME = 'appconfig.properties'


app = flask.Flask(__name__)


def set_properties(file_name):

    config = configparser.ConfigParser()

    try:
        config.read(file_name)
        tick_time_period = config['COST_PROP']['TickTimePeriod']
        tick_cost_rate = config['COST_PROP']['TickCostRate']
        cost_difference = config['COST_PROP']['CostDifference']

    except KeyError:
        print("Error: Invalid property file %s. Default properties are used.\n" % file_name)
        # Default service properties
        tick_time_period = 1  # in seconds
        tick_cost_rate = 60
        cost_difference = 200

    return tick_time_period, tick_cost_rate, cost_difference


def to_json(data):
    return json.dumps(data)


def response(code, data):
    return flask.Response(
        status=code,
        mimetype="application/json",
        response=data
    )


tmp = set_properties(PROP_FILE_NAME)
TICK_TIME_PERIOD = tmp[0]
TICK_COST_RATE = tmp[1]
COST_DIFFERENCE = tmp[2]

USD_RUR = CostGenerator(COST_DIFFERENCE, TICK_COST_RATE, TICK_TIME_PERIOD)
USD_EUR = CostGenerator(COST_DIFFERENCE, TICK_COST_RATE, TICK_TIME_PERIOD)
EUR_RUR = CostGenerator(COST_DIFFERENCE, TICK_COST_RATE, TICK_TIME_PERIOD)


@app.route('/', methods=['GET'])
def get_cost():

    response_data = {}

    for c in [('USD_RUR', USD_RUR), ('USD_EUR', USD_EUR), ('EUR_RUR', EUR_RUR)]:
        response_data[c[0]] = c[1]()

    print(response_data)
    return response(200, response_data)


@app.errorhandler(400)
def page_not_found(error):
    return response(400, {})


@app.errorhandler(404)
def page_not_found(error):
    return response(400, {})


@app.errorhandler(500)
def special_exception_handler(error):
    return response(500, {})


if __name__ == '__main__':
    app.run()
