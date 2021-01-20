# this is an example for cortex release 0.23 and may not deploy correctly on other releases of cortex

import boto3
from botocore import UNSIGNED
from botocore.client import Config
import mlflow.sklearn
import numpy as np
import re
import os
import joblib


class PythonPredictor:
    def __init__(self, config):
        os.environ["AWS_ACCESS_KEY_ID"] = "AKIA3KH6IPR6WOSYNHVU"
        os.environ["AWS_SECRET_ACCESS_KEY"] =  "IdJRXjhjSmY3b5tX35cKaGRivGTuAifS/Vq0JYi4"
        if os.environ.get("AWS_ACCESS_KEY_ID"):
            s3 = boto3.client("s3")  # client will use your credentials if available
        else:
            s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))  # anonymous client

        s3.download_file("cortex-6a2d11117c", "tmp/model.pickle", "/tmp/model.pickle")
        self.model = joblib.load(open("/tmp/model.pickle", "rb"))

    def predict(self, payload):
        inputs = [
                payload["input1"],
                payload["input2"],
                payload["input3"],
                payload["input5"],
                payload["input6"],
                payload["input7"],
                payload["input8"],
                payload["input9"],
                payload["input10"],
                payload["input11"],
                payload["input12"],
                payload["input13"],
                payload["input14"],
                payload["input15"],
                payload["input16"],
                payload["input17"]
        ]

        trip_duration = self.model.predict([inputs])[0]
        return trip_duration
