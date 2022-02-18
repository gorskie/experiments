from flask import Flask, jsonify, render_template
from flask_cors import CORS
from redis import Redis
from pymongo import MongoClient
from sum_mongo_counts import connect_mongo_db, get_done_counts
import docker


class Dashboard:
    def __init__(self, redis_server, docker_server, mongo_client):
        self.app = Flask(__name__)
        self.redis = redis_server
        self.docker = docker_server
        self.mongo = mongo_client
        CORS(self.app, resources={r'/data': {'origins': '*'}})


def get_jobs_stats(database):
    jobs_waiting = int(database.llen('jobs_waiting_queue'))
    jobs_in_progress = int(database.hlen('jobs_in_progress'))
    jobs_total = jobs_waiting + jobs_in_progress + jobs_done
    client_ids = database.get('total_num_client_ids')
    clients_total = int(client_ids) if client_ids is not None else 0
    return {
        'num_jobs_waiting': jobs_waiting,
        'num_jobs_in_progress': jobs_in_progress,
        'jobs_total': jobs_total,
        'clients_total': clients_total
    }


def get_container_stats(client):
    stats = {}
    for container in client.containers.list():
        long_name_lst = container.name.split('_')
        long_name_lst.pop(0)
        long_name_lst.pop(-1)
        name = '_'.join(long_name_lst)
        status = container.status
        stats[name] = status
    return stats


def create_server(database, docker_server, mongo_client):
    dashboard = Dashboard(database, docker_server, mongo_client)

    @dashboard.app.route('/', methods=['GET'])
    def _index():
        return render_template(
            'index.html'
        )

    @dashboard.app.route('/data', methods=['GET'])
    def _get_dashboard_data():
        data = get_jobs_stats(dashboard.redis)
        data.update({'num_jobs_done': get_done_counts(dashboard.mongo, 'mirrulations')})
        container_information = get_container_stats(dashboard.docker)
        data.update(container_information)
        return jsonify(data), 200

    return dashboard


if __name__ == '__main__':
    server = create_server(Redis('redis'), docker.from_env(), connect_mongo_db('mongo'))
    server.app.run(port=5000)
