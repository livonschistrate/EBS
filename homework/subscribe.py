import random, argparse, json
from config import CONSTANTS, FIELDS, FREQUENCIES, EQ_FREQUENCIES, \
                   getFieldValue, getFieldOperator, changeFieldOperator

def getFieldFrequency(field, number):
    return FREQUENCIES[field] * number // 100

def getFieldEqualFrequency(field, number):
    return EQ_FREQUENCIES[field] * number // 100

def writeResult(subscriptions):
    with open('results/subscriptions.txt', 'w') as f:
        for s in subscriptions:
            f.write("{")
            for field in s:
                if field not in ['operators', 'stationid']:
                    f.write("({0}, {1}, {2})".format(field, s['operators'][field], s[field]))
            f.write("}\n")
    with open('results/subscriptions.json', 'w') as j:
        j.write(json.dumps(subscriptions, indent=1))

def generateSubs(number):
    field_count = dict()
    for field in FIELDS:
        field_count[field] = getFieldFrequency(field, number)
    equal_field_count = dict()
    for field in FIELDS:
        equal_field_count[field] = getFieldEqualFrequency(field, field_count[field])
    
    subscriptions = []
    fields_to_clear = []
    for i in range(number):
        subscription = {}
        subscription['stationid'] = i+1
        fields = random.sample(field_count.keys(), random.randrange(1, len(field_count.keys()) + 1))
        for field in fields:
            subscription[field] = getFieldValue(field)
            field_count[field] -= 1
        subscriptions.append(subscription)
        for field in field_count:
            if field_count[field] == 0:
                fields_to_clear.append(field)
        if fields_to_clear != []:
            for field in fields_to_clear:
                field_count.pop(field)
            fields_to_clear = []
                
    if field_count != []:
        for field in field_count:
            while field_count[field]:
                sub_nr = random.randrange(1, number)
                if field not in subscriptions[sub_nr]:
                    subscriptions[sub_nr][field] = getFieldValue(field)
                    field_count[field] -= 1
                    
    for i in range(number):        
        subscriptions[i]['operators'] = {}
    
    for sub in subscriptions:
        for field in sub:
            sub['operators'][field] = getFieldOperator(field)
            if field not in ['operators', 'stationid'] and field in equal_field_count:
                if sub['operators'][field] in ['=', '=='] and equal_field_count[field] != 0:
                    equal_field_count[field] -= 1
                if sub['operators'][field] in ['=', '=='] and equal_field_count[field] == 0:
                    while sub['operators'][field] in ['=', '==']:
                        sub['operators'][field] = getFieldOperator(field)
            if field in ['operators', 'stationid']:
                sub['operators'].pop(field)
        for field in equal_field_count:
            if equal_field_count[field] == 0:
                fields_to_clear.append(field)
        if fields_to_clear != []:
            for field in fields_to_clear:
                equal_field_count.pop(field)
            fields_to_clear = []
    
    if equal_field_count != []:
        for field in equal_field_count:
            while equal_field_count[field]:
                sub_nr = random.randrange(1, number)
                if field in subscriptions[sub_nr] and subscriptions[sub_nr]['operators'][field] not in ['=', '==']:
                    subscriptions[sub_nr]['operators'][field] = changeFieldOperator(field)
                    equal_field_count[field] -= 1
                    
    random.shuffle(subscriptions)
    writeResult(subscriptions)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="subscribe.py creates subscriptions")
    parser.add_argument('--number', '-n', default=100, type=int, help="Number of publications to be generated")
    args = parser.parse_args()
    generateSubs(args.number)