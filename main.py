import sys
import math

class Player:
    instance = None
    def __init__(self):
        self.health=0
        self.storage = {'A':0,'B':0,'C':0,'D':0,'E':0}
        self.target=''
        self.samples=[]

    def getInstance():
        if Player.instance==None:
            Player.instance = Player()
        return Player.instance

class SampleData:
    listOfInstance=[]
    def __init__(self):
        self.id = 0
        self.carriedBy=0
        self.health = 0
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
                if foundSample == None  or foundSample.health < sample.health :
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
            plInstance.target = target

    available_a, available_b, available_c, available_d, available_e = [int(i) for i in input().split()]
    sample_count = int(input())
    for i in range(sample_count):
        tempSampleData = SampleData()
        sample_id, carried_by, rank, expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e = input().split()
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
            plInstance.samples.append(tempSampleData)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    print(plInstance.target,file=sys.stderr)
    if plInstance.target == 'DIAGNOSIS':

        sample = SampleData.getBestSample(plInstance.samples)
        if sample != None:
            print("CONNECT " + str(sample.id))
        else:
            print("GOTO MOLECULES")

    elif plInstance.target == 'MOLECULES':
        grabMolecules = False
        tab= {'A':0,'B':0,'C':0,'D':0,'E':0}
        for sample in plInstance.samples:
            for c in sample.cost:
                tab[c]+=sample.cost[c]
        for storage in plInstance.storage:
            tab[storage]-=plInstance.storage[storage]
        for t in tab:
            if tab[t] > 0:
                print("CONNECT " + t)
                grabMolecules = True
                break

        #print(tab,file=sys.stderr)
        if grabMolecules == False:
            print("GOTO LABORATORY")

    elif plInstance.target == 'LABORATORY':
        if len(plInstance.samples)>0:
            print("CONNECT " + str(plInstance.samples[0].id))
        else:
            print("GOTO DIAGNOSIS")
    elif plInstance.target == 'START_POS':
        print("GOTO DIAGNOSIS")



        
