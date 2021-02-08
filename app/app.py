from flask import Flask, request
from argparse import ArgumentParser
from mlflow.tracking import MlflowClient
from waitress import serve
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import shutil


class Application:
    def __init__(self, name, uri, host, port):
        self.name = name
        self.uri = uri
        self.host = host
        self.port = port
        self.app = Flask(name)
        self.client = MlflowClient(tracking_uri=uri)

        @self.app.route("/log_artifact", methods=['POST'])
        def log_artifact():
            if request.method == 'POST':
                if request.files:
                    if 'run_id' in request.form:
                        run_id = request.form['run_id']
                    else:
                        return {'status': 'fail', 'text': 'run_id is not found!'}

                    tmp_path = os.path.join(str(Path.home()), "mlflow_artifacts_proxy", run_id)
                    os.makedirs(tmp_path)
                    for f in request.files:
                        file = request.files[f]
                        filename = secure_filename(file.filename)
                        file_path = os.path.join(tmp_path, filename)
                        file.save(file_path)
                        self.client.log_artifact(run_id, local_path=file_path)
                    shutil.rmtree(os.path.join(str(Path.home()), "mlflow_artifacts_proxy"))

                    return {'status': 'success', 'text': "You're great!"}
                else:
                    return {'status': 'fail', 'text': 'No files!'}

    def run(self):
        serve(self.app, host=self.host, port=self.port)


if __name__ == '__main__':
    parser = ArgumentParser(description="An artifact logger proxy for the MLFlow tracking server")
    parser.add_argument("--name", type=str, default="MLFlow artifacts logger proxy", help="A name for proxy")
    parser.add_argument("--uri", type=str, default="http://localhost:5000", help="Remote tracking server URI")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to run a Flask application on")
    parser.add_argument("--port", type=int, default=5001, help="Port")

    args = parser.parse_args()
    app = Application(args.name, args.uri, args.host, args.port)
    app.run()
