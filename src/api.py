#!/usr/bin/env -S PATH="${PATH}:/usr/local/bin" python3

from notion_api import appendToCurrentDayNotes, tasksDatabase, photoDatabase
from config import importedTagURL

from notion.block import DividerBlock, TextBlock

from flask import Flask, request
from flask_apscheduler import APScheduler
app = Flask(__name__)


class Config(object):
    JOBS = [
        {
            'id': 'ping',
            'func': 'keep_awake:ping',
            'args': (),
            'trigger': 'interval',
            'seconds': 600
        }
    ]

    SCHEDULER_API_ENABLED = True


@app.route('/add_note')
def add_note():
    try:
        note = request.args.get('title')

        appendToCurrentDayNotes(note)

        return 'Succeceed in adding note', 200
    except Exception:
        return 'Failed in adding note', 500


@app.route('/add_task')
def add_task():
    try:
        task = request.args.get('title')
        url = request.args.get('url')

        collection = tasksDatabase().collection
        row = collection.add_row()
        row.name = task
        row.status = 'Inbox'
        row.url = url
        
        row.add_new(TextBlock, title="asdasdasdjkhasdkha sdkhas djkhas dkjahs dkasjhd")


        return 'Succeceed in adding task', 200
    except Exception:
        return 'Failed in adding task', 500


@app.route('/add_photo')
def add_photo():
    try:
        task = request.args.get('title')
        url = request.args.get('url')

        collection = tasksDatabase().collection
        row = collection.add_row()
        row.name = task
        row.status = 'Inbox'
        row.photo = url

        return 'Succeceed in adding photo', 200
    except Exception:
        return 'Failed in adding photo', 500


@app.route('/add_photojournal')
def add_photojournal():
    try:
        task = request.args.get('title')
        url = request.args.get('url')

        collection = photoDatabase().collection
        row = collection.add_row()
        row.name = task
        row.photo = url

        return 'Succeceed in adding photo', 200
    except Exception:
        return 'Failed in adding photo', 500

if __name__ == '__main__':
    app.run()

app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()