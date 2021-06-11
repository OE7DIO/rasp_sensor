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
    senfo["value"] = random.randint(5, 19)
    

def get_data():
    sense()
    return [senfo["name"], senfo["value"], senfo["unit"]]