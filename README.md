# A proxy for logging MLFlow artifacts to the remote tracking server

Install dependencies:
```
pip install -r requirements.txt --no-cache-dir
```
Help:
```
usage: app.py [-h] [--name NAME] [--uri URI] [--host HOST] [--port PORT]

An artifact logger proxy for the MLFlow tracking server

optional arguments: <br>
  -h, --help   show this help message and exit <br>
  --name NAME  A name for proxy <br>
  --uri URI    Remote tracking server URI <br>
  --host HOST  Host to run a Flask application on <br>
  --port PORT  Port 
```
Run example:
```
python app/app.py
```
Command above will run a Flask server on http://0.0.0.0:5001 with the tracking URI http://localhost:5000 <br><br>
Logging example with Python 3 requests:
```
with open('artifacts/foo.txt', 'rb') as f1, open('artifacts/image.png', 'rb') as f2, open('artifacts/animation.gif', 'rb') as f3:
    client = MlflowClient(tracking_uri="http://localhost:5000")
    try:
        experiment_id = client.create_experiment("foo")
    except RestException as e:
        experiment = client.get_experiment_by_name("foo")
        experiment_id = experiment.experiment_id
    run = client.create_run(experiment_id)
    run_id = run.info.run_id
    print(experiment_id + ":" + run_id)

    files = {'file1': f1, 'file2': f2, 'file3': f3}
    data = {'run_id': run_id}
    r = requests.post('http://localhost:5001/log_artifact', files=files, data=data)
```