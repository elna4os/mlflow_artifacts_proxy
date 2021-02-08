import unittest
import requests
from mlflow.tracking import MlflowClient
from mlflow.exceptions import RestException


class TestMLFlowArtifactsProxy(unittest.TestCase):
    def testLogArtifact(self):
        with open('artifacts/foo.txt', 'rb') as f:
            client = MlflowClient(tracking_uri="http://localhost:5000")
            try:
                experiment_id = client.create_experiment("foo")
            except RestException as e:
                experiment = client.get_experiment_by_name("foo")
                experiment_id = experiment.experiment_id
            run = client.create_run(experiment_id)
            run_id = run.info.run_id
            print(experiment_id + ":" + run_id)

            files = {'file': f}
            data = {'experiment_id': experiment_id, 'run_id': run_id, }
            r = requests.post('http://localhost:5001/log_artifact', files=files, data=data)
            print(r.text)


if __name__ == '__main__':
    unittest.main()
