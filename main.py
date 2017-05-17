import sys
import math

class Player:
    instance = None
    def __init__(self):
        self.health=0
        self.storage = {'A':0,'B':0,'C':0,'D':0,'E':0}
        self.expertise = {'A':0,'B':0,'C':0,'D':0,'E':0}
        self.target=''
        self.samples=[]

    def addSample(self,_sample):
        localStorage=self.storage.copy()
        for s in self.samples:
            for c in s.cost:
                localStorage[c]-=s.cost[c]

        goOn=True
        for c in _sample.cost:
            if localStorage[c] < _sample.cost[c]:
                goOn=False
                break
        if goOn:
            _sample.status ="COMPLETED"
        self.samples.append(_sample)

    @staticmethod
    def getInstance():
        if Player.instance is None:
            Player.instance = Player()
        return Player.instance

    def getExpertiseVal(self):
        val = 0
        for _expertise in self.expertise:
            val+=self.expertise[_expertise]
        return val

class SampleData:
    listOfInstance=[]
    def __init__(self):
        self.id = 0
        self.carriedBy=0
        self.health = 0
        self.status = "INPROGRESS"
        self.cost={'A':0,'B':0,'C':0,'D':0,'E':0}

    @staticmethod
    def getBestSample(listOfSample):
        #print("listOfSample" + str(listOfSample),file=sys.stderr)
        if len(listOfSample)>=3:
            return None
        nbMolRemaining=10
        for sm in listOfSample:
            for c in sm.cost:
                nbMolRemaining-=sm.cost[c]
        #print("nbMolRemaining" + str(nbMolRemaining),file=sys.stderr)
        foundSample=None
        for sample in SampleData.listOfInstance:
            if sample not in listOfSample and sample.carriedBy==-1:
                if foundSample is None  or foundSample.health < sample.health :
                    total = 0
                    for c in sample.cost:
                        total+=sample.cost[c]
                    if total < nbMolRemaining:
                        foundSample = sample
        return foundSample


# Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!

project_count = int(input())
for i in range(project_count):
    a, b, c, d, e = [int(j) for j in input().split()]
plInstance = Player.getInstance()
# game loop
while True:
    SampleData.listOfInstance=[]
    plInstance.samples=[]
    for i in range(2):
        target, eta, score, storage_a, storage_b, storage_c, storage_d, storage_e, expertise_a, expertise_b, expertise_c, expertise_d, expertise_e = input().split()
        eta = int(eta)
        score = int(score)
        storage_a = int(storage_a)
        storage_b = int(storage_b)
        storage_c = int(storage_c)
        storage_d = int(storage_d)
        storage_e = int(storage_e)
        expertise_a = int(expertise_a)
        expertise_b = int(expertise_b)
        expertise_c = int(expertise_c)
        expertise_d = int(expertise_d)
        expertise_e = int(expertise_e)
        if i==0:
            plInstance.health = score
            plInstance.storage['A']=storage_a
            plInstance.storage['B']=storage_b
            plInstance.storage['C']=storage_c
            plInstance.storage['D']=storage_d
            plInstance.storage['E']=storage_e
            plInstance.expertise['A']=expertise_a
            plInstance.expertise['B']=expertise_b
            plInstance.expertise['C']=expertise_c
            plInstance.expertise['D']=expertise_d
            plInstance.expertise['E']=expertise_e
            plInstance.target = target

    available_a, available_b, available_c, available_d, available_e = [int(i) for i in input().split()]
    molAvailable={'A':available_a,'B':available_b,'C':available_c,'D':available_d,'E':available_e}
    sample_count = int(input())
    for i in range(sample_count):
        tempSampleData = SampleData()
        #test= input()
        #print(test,file=sys.stderr)
        sample_id, carried_by, rank, expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e = input().split()
        #sample_id, carried_by, rank, expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e = test.split()
        sample_id = int(sample_id)
        carried_by = int(carried_by)
        rank = int(rank)
        health = int(health)
        cost_a = int(cost_a)
        cost_b = int(cost_b)
        cost_c = int(cost_c)
        cost_d = int(cost_d)
        cost_e = int(cost_e)
        tempSampleData.cost['A']=cost_a
        tempSampleData.cost['B']=cost_b
        tempSampleData.cost['C']=cost_c
        tempSampleData.cost['D']=cost_d
        tempSampleData.cost['E']=cost_e
        tempSampleData.health=health
        tempSampleData.id=sample_id
        tempSampleData.carriedBy = carried_by
        SampleData.listOfInstance.append(tempSampleData)
        if carried_by == 0:
            #plInstance.samples.append(tempSampleData)
            plInstance.addSample(tempSampleData)
            print("////" + str(tempSampleData.cost),file=sys.stderr)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    print(plInstance.target,file=sys.stderr)
    if plInstance.target == 'DIAGNOSIS':
        action=False
        for sample in plInstance.samples:
            if sample.cost['A'] == -1:
                print("CONNECT " + str(sample.id))
                action=True
                break
        if action == False and len(plInstance.samples)<2:
            sample = SampleData.getBestSample(plInstance.samples)
            if sample != None:
                print("CONNECT " + str(sample.id))
            else:
                print("GOTO MOLECULES")

    elif plInstance.target == 'MOLECULES':
        allZero = True
        listOfMoleculesToGrab = {'A':0,'B':0,'C':0,'D':0,'E':0}
        for _sample in plInstance.samples:
            for c in _sample.cost:
                listOfMoleculesToGrab[c]+=_sample.cost[c]
        for mol in plInstance.storage:
            listOfMoleculesToGrab[mol]-=plInstance.storage[mol]
        for mol in plInstance.expertise:
            listOfMoleculesToGrab[mol] -= plInstance.expertise[mol]
            if listOfMoleculesToGrab[mol]>0:
                allZero = False
        grabMolecule = False
        for mol in listOfMoleculesToGrab:
            if listOfMoleculesToGrab[mol]>0:
                if molAvailable[mol]>0:
                    print ("CONNECT " + mol)
                    grabMolecule = True
                    break

        if allZero:
            print("GOTO LABORATORY")
        elif not grabMolecule :
            finishedOne = False
            for _sample in plInstance.samples:
                if _sample.status == "COMPLETED":
                    finishedOne = True
                    break
            if finishedOne:
                print("GOTO LABORATORY")
            else:
                print("WAIT")


    elif plInstance.target == 'LABORATORY':
        if len(plInstance.samples)>0:
            print("CONNECT " + str(plInstance.samples[0].id))
        else:
            print("GOTO SAMPLES")
    elif plInstance.target == "SAMPLES":
        if len(plInstance.samples)>0:
            print ("GOTO DIAGNOSIS")
        else:
            print ("CONNECT 1")
    elif plInstance.target == 'START_POS':
        print("GOTO SAMPLES ")



        
