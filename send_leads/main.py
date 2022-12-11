

from flask import Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import requests as req
import json
from datetime import datetime
from data_base import get_session
import logging

from dotenv import dotenv_values
settings = dotenv_values('/home/aleksey/PyProject/test_flask/send_leads/.env')
logging.basicConfig(filename='/home/aleksey/PyProject/test_flask/send_leads/logs/send_leads_log',
                    format=f"%(levelname)s: %(message)s",
                    level=logging.INFO)

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = \
#     f'postgresql://{settings.get("PSQL_USER")}:{settings.get("PSQL_PASSWORD")}@{settings.get("HOST")}:5432/{settings.get("PSQL_DB_NAME")}'
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
from models import *


@app.post('/test')
def send_leads():

    lead = {
        'lead_id': request.form.get('leads[responsible][0][id]'),
        'crm_user_id': request.form.get('leads[responsible][0][responsible_user_id]'),
        'leads[responsible][0][status_id]': request.form.get('leads[responsible][0][status_id]'),
        'leads[responsible][0][pipeline_id]': request.form.get('leads[responsible][0][pipeline_id]'),
    }
    if lead.get('leads[responsible][0][status_id]') == '34017646' and \
            lead.get('leads[responsible][0][pipeline_id]') == '3414178':

        logging.info(f"[{datetime.utcnow()}] REQUEST:\"{request.__dict__}\"")
        print(datetime.utcnow(), lead)
        logging.info(f"[{datetime.utcnow()}] LEAD:\"{lead}\"")

        session = get_session()
        user = session.query(Users).filter_by(crm_id=int(lead.get('crm_user_id'))).first()
        if user:
            print('USER_IS_ADMIN8')

            data = {
                "chat_id": user.telegram_id,
                "text": f"<b>🔥Внимание! Новый лид!🔥</b>\n"
                        f"https://mirarealestate.amocrm.com/leads/detail/{lead.get('lead_id')}",
                "parse_mode": "HTML"
            }
            res = req.post(f"https://api.telegram.org/bot{settings.get('TOKEN')}/sendMessage", data=data)

            print(datetime.utcnow(), res.__dict__)
            logging.info(f"[{datetime.utcnow()}] RESPONSE_SEND_TG:\"{res.__dict__}\"")

            # После наполнения БД данными, удалить код ниже!
            msg_info = json.loads(res.__dict__.get('_content'))
            if msg_info.get('ok'):
                user.first_name = msg_info.get('result').get('chat').get('first_name')
                user.last_name = msg_info.get('result').get('chat').get('last_name')
                user.username = msg_info.get('result').get('chat').get('username')
                session.commit()

                print(datetime.utcnow(), user.__json__())
                logging.info(f"[{datetime.utcnow()}] SAVE_USER:\"{user.__json__()}\"")

    return {'CODE': 200, 'STATUS': 'OK'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, processes=1)
