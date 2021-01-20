import requests

endpoint = "https://g06o0hssmj.execute-api.us-east-1.amazonaws.com/trip-estimator"
payload = {
    "input1":2.0,
    "input2":6.0,
    "input3":-73.96147155761719,
    "input5":40.774391174316406,
    "input6":-73.9537124633789,
    "input7":40.77536010742188,
    "input8":0.6621858468807331,
    "input9":0.007819358973817251,
    "input10":0.007788946222373263,
    "input11":6.0,
    "input12":23.0,
    "input13":33.0,
    "input14":0.0,
    "input15":3.0,
    "input16":0.0,
    "input17":0.0
}
prediction = requests.post(endpoint, payload)

trip_duration = str(prediction.content,'utf-8')

print("Trip duration is : ", trip_duration)