import argparse, json
from config import CONSTANTS, FIELDS, getFieldValue
    
def writeResult(publications):
    with open('results/publications.txt', 'w') as f:
        for p in publications:
            f.write(json.dumps(p))
            f.write("\n")
    with open('results/publications.json', 'w') as j:
        j.write(json.dumps(publications, indent=1))
    
def generatePubs(number):
    publications = []
    for i in range(number):
        publication = {}
        publication["stationid"] = i+1
        for field in FIELDS:
             publication[field] = getFieldValue(field)
        publications.append(publication)
    writeResult(publications)
    return publications
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="publish.py creates publications")
    parser.add_argument('--number', '-n', default=100, type=int, help="Number of publications to be generated")
    args = parser.parse_args()
    generatePubs(args.number)