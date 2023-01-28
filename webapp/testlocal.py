import requests, time, json

null = None
false = False
true = True

json_data = {"hello":11}

for x in range(1):
    asda = requests.post('http://127.0.0.1:5000/post', json=json_data,
        headers={"Content-Type": "application/json", "Authorization":"mysecretkey"})
    print(x, asda.text)


time.sleep(3)
