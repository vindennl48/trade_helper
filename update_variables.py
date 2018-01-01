import json

def update_variables():
    while True:
        try:
            with open('.data.dat', 'r') as f:
                PV = json.loads(f.read())
            break
        except:
            print("Error accessing data file")
    return PV

