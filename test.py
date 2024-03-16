
import requests, json, sys

def getGenotypeProbabilities(rs):
    server = "http://rest.ensembl.org"
    ext = "/variation/homo_sapiens"
    payload = {"population_genotypes" : 1}
    headers = {"Content-Type" : "application/json", "Accept" : "application/json"}
    data = {}
    data["ids"] = list(rs)
    r = requests.post(server+ext, headers=headers, params=payload, data=json.dumps(data))

    if not r.ok:
        r.raise_for_status()
        sys.exit()
    
    decoded = r.json()
    return decoded
 
def readDict(filename, sep):
    with open(filename, "r") as f:
        dict = {}
        for line in f:
            values = line.split(sep)
            dict[values[0].strip('"')] = str(values[1].strip(' ').strip('"').strip('\n').strip('"'))
        return(dict)
