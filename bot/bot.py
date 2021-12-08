# -*- coding: utf-8 -*-
# todo-> remover os imports que não foram utilizados(traceback, timedelta, timezone)
import os, sys, traceback, logging, configparser
import xlsxwriter
from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.blocking import BlockingScheduler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler
#todo-> seguir as boas praticas de codigo da pep8 para desenvolvimento de codigo em python

def main(argv):
    greetings()

    print('Press Crtl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    app = Flask(__name__)
    handler = RotatingFileHandler('bot.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    #todo-> utilzar arquivo de configuração(config, settings, env...) para declarar as variaveis de ambiente
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123mudar@127.0.0.1:5432/bot_db'
    db = SQLAlchemy(app)
    config = configparser.ConfigParser()
    config.read('/tmp/bot/settings/config.ini')

    var1 = int(config.get('scheduler','IntervalInMinutes'))
    app.logger.warning('Intervalo entre as execucoes do processo: {}'.format(var1))
    scheduler = BlockingScheduler()

    #todo-> remover variavel que não esta sendo utilizada(task1_instance)
    task1_instance = scheduler.add_job(task1(db), 'interval', id='task1_job', minutes=var1)

    try:
        scheduler.start()
    except(KeyboardInterrupt, SystemExit):
        pass

def greetings():
    #todo-> Seguir o padrão de espaçamento descrito na pep8
    print('             ##########################')
    print('             # - ACME - Tasks Robot - #')
    print('             # - v 1.0 - 2020-07-28 - #')
    print('             ##########################')

def task1(db):

    file_name = 'data_export_{0}.xlsx'.format(datetime.now().strftime("%Y%m%d%H%M%S"))
    file_path = os.path.join(os.path.curdir, file_name)
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()

    #todo-> aproveitar que ja esta utilziando o SQLAlchemy
    # e utilizar ele como ORM, no lugar de fazer uma consulta na mão
    # Seria algo como "users.query.all()"
    orders = db.session.execute('SELECT * FROM users;')
    #todo-> fechar a conexão
    
    index = 1
    
    #todo-> pode ser refatorado criando uma lista de index
    # e utilizando um for para passar por cada letra usando 
    # o str(i+65) como parametro
    worksheet.write('A{0}'.format(index),'Id')
    worksheet.write('B{0}'.format(index),'Name')
    worksheet.write('C{0}'.format(index),'Email')
    worksheet.write('D{0}'.format(index),'Password')
    worksheet.write('E{0}'.format(index),'Role Id')
    worksheet.write('F{0}'.format(index),'Created At')
    worksheet.write('G{0}'.format(index),'Updated At')
    
    for order in orders:
        index = index + 1

        print('Id: {0}'.format(order[0]))
        worksheet.write('A{0}'.format(index),order[0])
        print('Name: {0}'.format(order[1]))
        worksheet.write('B{0}'.format(index),order[1])
        print('Email: {0}'.format(order[2]))
        worksheet.write('C{0}'.format(index),order[2])
        print('Password: {0}'.format(order[3]))
        worksheet.write('D{0}'.format(index),order[3])
        print('Role Id: {0}'.format(order[4]))
        worksheet.write('E{0}'.format(index),order[4])
        print('Created At: {0}'.format(order[5]))
        worksheet.write('F{0}'.format(index),order[5])
        print('Updated At: {0}'.format(order[6]))
        worksheet.write('G{0}'.format(index),order[6])
        
    workbook.close()
    #todo-> tratar excecoes
    print('job executed!')

if __name__ == '__main__':
    main(sys.argv)
