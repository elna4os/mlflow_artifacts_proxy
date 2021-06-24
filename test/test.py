import unittest

import requests
from mlflow.exceptions import RestException
from mlflow.tracking import MlflowClient


class TestMLFlowArtifactsProxy(unittest.TestCase):
    def testLogArtifact(self):
        with open('artifacts/foo.txt', 'rb') as f1, open('artifacts/image.png', 'rb') as f2, open(
                'artifacts/animation.gif', 'rb') as f3:
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
            print(r.text)


if __name__ == '__main__':
    unittest.main()
