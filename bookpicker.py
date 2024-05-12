import re
import json

class DeweyClass():
    def __init__(self, classification, description):
        self.classification = classification.strip()
        self.description = description.strip()
        self.codes = []
        self.codeDict = {}
    
    def addCode(self, code):
        idx = code[:3]
        code = code[4:].strip()
        self.codes.append((idx, code))
    
    def codesToDict(self):
        self.codeDict = {
            "Classification": self.classification,
            "Description": self.description,
            "Codes": [ {c[0]: c[1]} for c in self.codes ]
        }




def deweysToDict(infile="dewey_decimal.txt"):
    tmp = {}
    Deweys = []
    with open(infile, 'r') as f:
        deweys = f.readlines()
    
    for line in deweys:
        if re.match(r'^Class', line):
            classification = line[6:9]
            description = line[12:]
            try:
                base = int(classification[0])
            except ValueError:
                base = classification[0]
            tmp[base] = DeweyClass(classification, description)
        else:
            try:
                base = int(line[0])
            except ValueError:
                base = 'F'
            tmp[base].addCode(line)
    
    for d in tmp.values():
        d.codesToDict()
        Deweys.append(d.codeDict)

    return Deweys

def deweysToJson(DeweyDict):
    with open('deweyDecimal.json', 'w') as outfile:
        json.dump(DeweyDict, outfile)

if __name__ == "__main__":
    DeweyDict = deweysToDict()
    deweysToJson(DeweyDict)