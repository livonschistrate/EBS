import random, argparse, json
from config import CONSTANTS, FIELDS, FREQUENCIES, EQ_FREQUENCIES, \
                   getFieldValue, getFieldOperator, getEqFieldOperator, getNonEqFieldOperator

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
    field_count, subs_that_contain_field, subs_that_contain_equal = dict(), {}, {}
    for field in FIELDS:
        field_count[field] = getFieldFrequency(field, number)
        subs_that_contain_field[field] = []
        subs_that_contain_equal[field] = []
    equal_field_count = dict()
    for field in FIELDS:
        equal_field_count[field] = getFieldEqualFrequency(field, field_count[field])
    
    subscriptions = []
    for i in range(number):
        if field_count != {}: 
            subscription = {}
            subscription['stationid'] = i+1
            fields = random.sample(list(field_count.keys()), random.randrange(1, len(field_count.keys()) + 1))
            for field in fields:
                subscription[field] = getFieldValue(field)
                field_count[field] -= 1
                subs_that_contain_field[field].append(i)
            subscriptions.append(subscription)

    for field in field_count:
        while field_count[field] < 0:
            sub_nr = random.choice(subs_that_contain_field[field])
            subscriptions[sub_nr].pop(field)
            field_count[field] += 1
            subs_that_contain_field[field].remove(sub_nr)
        while field_count[field] > 0:
            sub_nr = random.randrange(0, number)
            while sub_nr in subs_that_contain_field[field]:
                sub_nr = random.randrange(0, number)
            subscriptions[sub_nr][field] = getFieldValue(field)
            field_count[field] -= 1
            subs_that_contain_field[field].append(sub_nr)
             
    if any(len(sub.keys()) == 1 for sub in subscriptions):
        for sub in subscriptions:
            if len(sub.keys()) == 1:
                change_sub = random.choice([s for s in subscriptions if len(s.keys()) > 2])
                change_field = random.choice([f for f in change_sub.keys() if f in FIELDS])
                sub[change_field] = change_sub[change_field]
                change_sub.pop(change_field)                       
    
    for sub in subscriptions:
        sub['operators'] = {}
        for field in sub:
            sub['operators'][field] = getFieldOperator(field)
            if field not in ['operators', 'stationid'] and field in equal_field_count:
                if sub['operators'][field] in ['=', '=='] and equal_field_count[field] != 0:
                    subs_that_contain_equal[field].append(sub['stationid']-1)
                    equal_field_count[field] -= 1
                elif sub['operators'][field] in ['=', '=='] and equal_field_count[field] == 0:
                    sub['operators'][field] = getNonEqFieldOperator(field)
            elif field in ['operators', 'stationid']:
                sub['operators'].pop(field)

    for field in equal_field_count:
        while equal_field_count[field] < 0:
            sub_nr = random.choice(subs_that_contain_equal[field])
            if field in subscriptions[sub_nr]:
                subscriptions[sub_nr]['operators'][field] = getNonEqFieldOperator(field)
                equal_field_count[field] += 1
        while equal_field_count[field] > 0:
            sub_nr = random.randrange(0, number)
            while sub_nr in subs_that_contain_equal[field]:
                sub_nr = random.randrange(0, number)
            if field in subscriptions[sub_nr]:
                subscriptions[sub_nr]['operators'][field] = getEqFieldOperator(field)
                equal_field_count[field] -= 1
                    
    writeResult(subscriptions)
    return subscriptions

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="subscribe.py creates subscriptions")
    parser.add_argument('--number', '-n', default=100000, type=int, help="Number of publications to be generated")
    args = parser.parse_args()
    generateSubs(args.number)