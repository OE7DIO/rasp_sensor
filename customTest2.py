import random   #for testing purposes


def init_sensor():
    #initialize your sensor here
    global senfo 
    senfo = {
        "name" : "Sensorname",
        "value" : 0,            #initial value may be useful
        "unit" : "Einheit"        
        }
    print("Finished initialising ")

def sense(): 
    #put your sensor here
    global senfo
    senfo["value"] = not senfo["value"]
    

def get_data():

    return [senfo["name"], senfo["value"], senfo["unit"]]