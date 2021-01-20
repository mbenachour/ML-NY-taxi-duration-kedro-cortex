# ML-NY-taxi-duration-kedro-cortex

## Running training pipelines and nodes  

download the data from : https://public-datasets-mba.s3.amazonaws.com/train.csv

copy the file to the input location in Kedro :

```bash
cp train.csv ./data/01_raw 
```

```bash
cd my_cab_trip_duration_kedro_training 
```

the models pickle files will be created under 

```bash
./data/06_models/<version>/model.pickle
```


## Deploy with cortex

creating kubernetes deployment cluster :

```bash
cortex up basic-cluster.yaml 
```

once the cluster is up , we need to copy the model created  by Kedro to s3  :


```bash
aws s3 cp ./data/06_models/<version>/model.pickle s3://cortex-6a2d11117c/tmp/
```

Deploy the API

```bash
cd cortex-trip-estimator
cortex deploy trip_estimator.yaml
```

Testing the  API 

```bash
 python consume.py
Trip duration is :  5.252568735167378
```