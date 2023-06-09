import json, random, datetime

CONSTANTS = json.load(open('data.json'))

FREQUENCIES = CONSTANTS['frequencies']

EQ_FREQUENCIES = CONSTANTS['eqfrequencies']

FIELDS = ["city", "temperature", "rain_procentage", "wind_speed", "wind_direction", "date"]

AVG_CONSTANTS = json.load(open('complexdata.json'))

AVG_FIELDS = ["avg_temperature", "avg_rain_procentage", "avg_wind_speed"]

def getFieldValue(field):
    if field in ["city", "wind_direction"]:
        return random.choice(CONSTANTS[field])
    elif field in ["temperature", "rain_procentage", "wind_speed"]:
        return random.uniform(CONSTANTS[field]["min_value"], CONSTANTS[field]["max_value"])
    elif field in ["avg_temperature", "avg_rain_procentage", "avg_wind_speed"]:
        return random.uniform(AVG_CONSTANTS[field]["min_value"], AVG_CONSTANTS[field]["max_value"])
    elif field == "date":
        month = random.randrange(1, 13)
        if month in [1, 3, 5, 7, 8, 10, 12]:
            day = random.randrange(1, 32)
        elif month in [4, 6, 9, 11]:
            day = random.randrange(1, 31)
        else:
            day = random.randrange(1, 29)
        return datetime.datetime(2022, month, day).strftime('%m/%d/%Y')
    
def getFieldOperator(field):
    if field in ["city", "wind_direction"]:
        return random.choice(CONSTANTS['string_operator'])
    elif field in ["temperature", "rain_procentage", "wind_speed", "date"]:
        return random.choice(CONSTANTS['numeric_operator'])
    elif field in ["avg_temperature", "avg_rain_procentage", "avg_wind_speed"]:
        return random.choice(AVG_CONSTANTS['numeric_operator'])
    
def getEqFieldOperator(field):
    if field in ["city", "wind_direction"]:
        return CONSTANTS['string_operator'][0]
    elif field in ["temperature", "rain_procentage", "wind_speed", "date"]:
        return CONSTANTS['numeric_operator'][0]
    
def getNonEqFieldOperator(field):
    if field in ["city", "wind_direction"]:
        return CONSTANTS['string_operator'][1]
    elif field in ["temperature", "rain_procentage", "wind_speed", "date"]:
        return random.choice([x for x in CONSTANTS['numeric_operator'] if x != CONSTANTS['numeric_operator'][0]])
    
    
    