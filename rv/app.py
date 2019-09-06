# -*- coding utf-8 -*- #

from flask import Flask, render_template, request, make_response
from flask import jsonify

import time
import threading
from rv import lr_predict
from rv import xgboost_predict, logging_config

logger = logging_config.Logger()


def heartbeat():
    logger.info(time.strftime('%Y-%m-%d %H:%M:%S - heartbeat', time.localtime(time.time())))
    timer = threading.Timer(60, heartbeat)
    timer.start()


timer = threading.Timer(60, heartbeat)
timer.start()

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import re

zhPattern = re.compile(u'[\u4e00-\u9fa5]+')

app = Flask(__name__, static_url_path="/static")


@app.route('/message', methods=['POST'])
def reply():
    register_time = request.form['register_time']
    city = request.form['city']
    mileage = request.form['mileage']
    make = request.form['make']
    family = request.form['family']
    engine = request.form['engine']
    gear0 = request.form['gear0']
    vehicle_type_code = request.form['vehicle_type_code']
    publish_date = request.form['publish_date']
    new_price = request.form['new_price']
    # print(register_time, city, mileage, make, family, engine)
    # price = lr_predict.predict(register_time=register_time, city=city, mileage=mileage, make=make, family=family,
    #                            engine=engine, publish_date=publish_date, new_price=new_price, gear0=gear0,
    #                            vehicle_type_code=vehicle_type_code)
    # print('lr_predict:', price)
    price = xgboost_predict.predict(register_time=register_time, city=city, mileage=mileage, make=make, family=family,
                                    engine=engine, publish_date=publish_date, new_price=new_price, gear0=gear0,
                                    vehicle_type_code=vehicle_type_code)
    price = round(price, 1)
    data = [register_time, city, mileage, make, family, engine, gear0, vehicle_type_code, publish_date, new_price,
            price]
    return render_template("message.html", data=data)


@app.route("/")
def index():
    return render_template("index.html")


# 启动APP
if (__name__ == "__main__"):
    app.run(host='0.0.0.0', port=8808)
