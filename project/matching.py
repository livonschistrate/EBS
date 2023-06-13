import argparse, json, random

PUB_WINDOW = 5


def writeResult(matching,file_name):
    with open('results/matching/'+file_name+'.txt', 'w') as f:
        for m in matching:
            f.write(json.dumps(m))
            f.write("\n")
    with open('results/matching/'+file_name+'.json', 'w') as j:
        j.write(json.dumps(matching, indent=1))

def generateMatchingOneSubscription(subscription,publications):
    sub_keys = []
    for key in subscription.keys():
        if key != 'stationid' and key != 'operators':
            sub_keys.append(key)

    op_values = []
    for value in subscription['operators'].values():
        op_values.append(value)

    op_keys = []
    for key in subscription['operators'].keys():
        op_keys.append(key)
        
    matching = []
    matching.append(subscription)
    conditions_remplies = True
    for publication in publications:
        for key in sub_keys:
            operator = op_values[op_keys.index(key)]
            if operator == '==':
                conditions_remplies = subscription[key]==publication[key]
            elif operator == '=':
                conditions_remplies = subscription[key]==publication[key]
            elif operator == '!=':
                conditions_remplies = subscription[key]!=publication[key]
            elif operator == '>':
                conditions_remplies = subscription[key]<publication[key]
            elif operator == '>=':
                conditions_remplies = subscription[key]<=publication[key]
            elif operator == '<':
                conditions_remplies = subscription[key]>publication[key]
            elif operator == '<=':
                conditions_remplies = subscription[key]>=publication[key]
            if not(conditions_remplies):
                break
        if conditions_remplies:
            matching.append(publication)
    return matching

def generateMatchingOneComplexSubscription(subscription,publications):
    sub_keys = []
    for key in subscription.keys():
        if key != 'stationid' and key != 'operators':
            sub_keys.append(key)

    op_values = []
    for value in subscription['operators'].values():
        op_values.append(value)

    op_keys = []
    for key in subscription['operators'].keys():
        op_keys.append(key)
        
    matching = []
    matching.append(subscription)
    conditions_remplies = True
    
    selected_city_pubs = []
    if subscription['operator']['city'] == '==':
        for pub in publications:
            if pub['city'] == subscription['city']:
                selected_city_pubs.append(pub)
    else:
        for pub in publications:
            if pub['city'] != subscription['city']:
                selected_city_pubs.append(pub)
                
    found = False
    while found == False:
        selected_pubs = random.sample(selected_city_pubs, PUB_WINDOW)
        averages = {}
        
        for key in sub_keys:
            if key in ["avg_temperature", "avg_rain_procentage", "avg_wind_speed"]:
                averages[key] = 0
                for pub in selected_pubs:
                    averages[key] += pub[key]
                averages[key] /= PUB_WINDOW
        
        for key in sub_keys:
            operator = op_values[op_keys.index(key)]
            if operator == '>':
                conditions_remplies = subscription[key]<averages[key]
            elif operator == '>=':
                conditions_remplies = subscription[key]<=averages[key]
            elif operator == '<':
                conditions_remplies = subscription[key]>averages[key]
            elif operator == '<=':
                conditions_remplies = subscription[key]>=averages[key]
            if not(conditions_remplies):
                break
        if conditions_remplies:
            matching.append(selected_pubs)
            found = True            
            
    return matching

def generateMatching(subscriptions,publications):
    path = 'results/matching.json'
    matching = []
    for subscription in subscriptions:
        matching.append(generateMatchingOneSubscription(subscription,publications))
    with open(path, 'w') as m:
        m.write(json.dumps(matching, indent=2))


if __name__ == '__main__':
    with open('results/publications.json') as p:
        publications = json.load(p)
    with open('results/subscriptions.json') as s:
        subscriptions = json.load(s)

    parser = argparse.ArgumentParser(description="matching.py match one subscription with the publications")
    parser.add_argument('--number', '-n', default=100, type=int, help="Id of the subscription you want to match")
    args = parser.parse_args()
    generateMatching(subscriptions,publications)

