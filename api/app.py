from typing import Dict

import celery.states as states
from flask import Flask, Response, jsonify, url_for

from worker import celery

dev_mode = True
app = Flask(__name__)


@app.route('/')
def health_check() -> Response:
    return jsonify("The service is running properly")


@app.route('/calculate_fare')
def calculate_fare() -> str:
    task = celery.send_task('tasks.calculate_fare', args=[], kwargs={})
    response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
    return response


@app.route('/check/<string:task_id>')
def check_task(task_id: str) -> Dict:
    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return res.state
    else:
        return jsonify(res.result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
