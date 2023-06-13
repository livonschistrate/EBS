import json, random
from config import CONSTANTS, FIELDS, AVG_CONSTANTS, AVG_FIELDS, getFieldValue
  
def writeResult(publications):
    with open('results/complexsubscriptions.txt', 'w') as f:
        for p in publications:
            f.write(json.dumps(p))
            f.write("\n")
    with open('results/complexsubscriptions.json', 'w') as j:
        j.write(json.dumps(publications, indent=1))

def generateComplexSubs(number):
    complex_subscriptions = []
    for i in range(number):
        subscription = {}
        subscription['operators'] = {}
        subscription["stationid"] = i+1
        subscription["city"] = getFieldValue('city')
        subscription['operators']['city'] = random.choice(['==', '!='])
        fields = random.sample(list(AVG_FIELDS), random.randrange(1, len(AVG_FIELDS) + 1))
        for field in fields:
             subscription[field] = getFieldValue(field)
        complex_subscriptions.append(subscription)
    writeResult(complex_subscriptions)