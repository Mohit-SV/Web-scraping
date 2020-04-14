import datetime
from . import app
from flask import jsonify, url_for
from flask import render_template
from .config import client
from .tasks import scra_per, build_hourly_key_details
from .helpers.test_flatten import all_keys_count


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html',
                           title='Reuter\'s news check')


# calling task1
@app.route('/scraper', methods=['POST'])
def scraper():
    task = scra_per.apply_async()
    print('called scraper')
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}


# calling task2
@app.route('/schema', methods=['POST'])
def schema():
    task = build_hourly_key_details.apply_async()
    print("called schema")
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}

# defining task status
@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = scra_per.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        try:
            print(task.info)
            response = {
                'state': task.state,
                'current': task.info.get('current', 0),
                'total': task.info.get('total', 1),
                'status': task.info.get('status', '')
            }
            if 'result' in task.info:
                response['result'] = task.info['result']
        except:
            print(task.info)
            response = {
                'state': task.state,
                'current': task.info[0][0],
                'total': task.info[0][0],
                'status': task.info[0][0]
            }
            if 'result' in task.info:
                response['result'] = task.info[0][0]
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


@app.route('/table', methods=['GET', 'POST'])
def gen_table():
    db = client.reuters_news
    col = db.news_items_key_freq
    # hourly_key_details = col.find({}, { '_id': 0 }).sort("natural", -1).limit(1)
    hourly_key_details = col.find({}, { '_id': 0 })
    hourly_key_details1 = {}
    for i in hourly_key_details:
        hourly_key_details1.update(i)
    # print(hourly_key_details1)
    return render_template('table.html', hourly_key_details= hourly_key_details1)
