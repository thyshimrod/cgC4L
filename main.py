import sys
import math

class Player:
    instance = None
    def __init__(self):
        self.health=0
        self.storage = {'A':0,'B':0,'C':0,'D':0,'E':0}
        self.expertise = {'A':0,'B':0,'C':0,'D':0,'E':0}
        self.target=''
        self.nbSampleAnalyzed = 0
        self.samples=[]
        self.eta = 0

    def getNbMoleculeInStorage(self):
        val = 0
        for s in self.storage:
            val += self.storage[s]

        return val

    def checkSampleStatus(self,_sample):
        localStorage = self.storage.copy()
        for s in self.samples:
            if s.status=="COMPLETED":
                for c in s.cost:
                    if s.cost[c]>0:
                        localStorage[c] -= s.cost[c]+self.expertise[c]

        goOn = True
        for c in _sample.cost:
            if localStorage[c] < (_sample.cost[c]-self.expertise[c]):
                goOn = False
                break

        return "COMPLETED" if goOn else "INPROGRESS"

    def addSample(self,_sample):
        _sample.status = self.checkSampleStatus(_sample)
        print("bbb " + str(_sample.id) + "//" + str(_sample.status) + "//" + str(_sample.diagState) + "//"+str(_sample.cost),file=sys.stderr)
        self.samples.append(_sample)
        if _sample.status == "COMPLETED" and _sample.diagState!="NEW":
            self.expertise[_sample.gain]+=1

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
    listOfInstance={}
    def __init__(self):
        self.id = 0
        self.carriedBy=0
        self.health = 0
        self.gain=0
        self.status = "INPROGRESS"
        self.diagState = "NEW"
        self.cost={'A':0,'B':0,'C':0,'D':0,'E':0}

    @staticmethod
    def getNbFreeSample():
        val = 0
        for _sample in SampleData.listOfInstance:
            if SampleData.listOfInstance[_sample].carriedBy == -1:
                val+=1

        return val

    @staticmethod
    def getBestSample(listOfSample):
        #print("listOfSample" + str(listOfSample),file=sys.stderr)
        if len(listOfSample)>=3:
            return None
        nbMolRemaining=10
        for sm in listOfSample:
            for c in sm.cost:
                if sm.cost[c] > 0:
                    nbMolRemaining-=sm.cost[c] + Player.getInstance().expertise[c]
        #print("nbMolRemaining" + str(nbMolRemaining),file=sys.stderr)
        foundSample=None
        for sampleID in SampleData.listOfInstance:

            sample = SampleData.listOfInstance[sampleID]
            print("BEST " + str(sampleID) + "//" + str(sample.carriedBy) + "//", file=sys.stderr)
            if sample not in listOfSample and sample.carriedBy==-1:
                if foundSample is None  or foundSample.health < sample.health :
                    total = 0
                    for c in sample.cost:
                        if sample.cost[c] > 0:
                            total+=sample.cost[c]-Player.getInstance().expertise[c]
                    if total < nbMolRemaining:
                        foundSample = sample
        print("BEST2 " + str(foundSample), file = sys.stderr)
        return foundSample


# Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!

project_count = int(input())
for i in range(project_count):
    a, b, c, d, e = [int(j) for j in input().split()]
plInstance = Player.getInstance()
# game loop
while True:
    #SampleData.listOfInstance=[]
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
            plInstance.eta = eta
            print("STORAGE " + str(plInstance.storage),file=sys.stderr)

    available_a, available_b, available_c, available_d, available_e = [int(i) for i in input().split()]
    molAvailable={'A':available_a,'B':available_b,'C':available_c,'D':available_d,'E':available_e}
    sample_count = int(input())
    for i in range(sample_count):

        #test= input()
        #print(test,file=sys.stderr)
        sample_id, carried_by, rank, expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e = input().split()
        #sample_id, carried_by, rank, expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e = test.split()
        sample_id = int(sample_id)
        carried_by = int(carried_by)
        tempSampleData = None
        if sample_id not in SampleData.listOfInstance:
            tempSampleData = SampleData()
            SampleData.listOfInstance[sample_id] = tempSampleData
        else:
            tempSampleData = SampleData.listOfInstance[sample_id]
        tempSampleData.gain = expertise_gain
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
        #SampleData.listOfInstance.append(tempSampleData)

        if carried_by == 0:
            #print("CARRIED " + str(sample_id) + "/" + str(plInstance.samples),file=sys.stderr)
            #plInstance.samples.append(tempSampleData)
            plInstance.addSample(SampleData.listOfInstance[sample_id])
            #print("////" + str(tempSampleData.cost) + str("//") + str(sample_id),file=sys.stderr)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    print(plInstance.target,file=sys.stderr)
    if plInstance.target == 'DIAGNOSIS':
        if plInstance.eta == 0:
            action=False
            for _sample in plInstance.samples:
                if _sample.diagState in ("NEW","DIAGNOSED"):
                    print("CONNECT " + str(_sample.id))
                    _sample.diagState = "DIAGNOSED" if _sample.diagState == "NEW" else "INCLOUD"
                    action = True
                    break

            if not action:
                sample = SampleData.getBestSample(plInstance.samples)
                if sample is not None:
                    print("CONNECT " + str(sample.id))
                    sample.diagState = "INCLOUD"
                else:
                    print("GOTO MOLECULES")
                    # for sample in plInstance.samples:
            #     if sample.cost['A'] == -1:
            #         print("CONNECT " + str(sample.id))
            #         action=True
            #         break
            # if action == False :#and len(plInstance.samples)<2:
            #     sample = SampleData.getBestSample(plInstance.samples)
            #     if sample != None:
            #         print("CONNECT " + str(sample.id))
            #     else:
            #         print("GOTO MOLECULES")
        else:
            print("WAIT")
    elif plInstance.target == 'MOLECULES':
        if plInstance.getNbMoleculeInStorage()<10:
            allZero = True
            grabMolecule = False
            listOfMoleculesToGrab = plInstance.storage.copy()
            for _sample in plInstance.samples:
                if _sample.status == "COMPLETED":
                    for c in _sample.cost:
                        listOfMoleculesToGrab[c]-=_sample.cost[c]

            for _sample in plInstance.samples:
                print("MOL " + str(_sample.cost) + str("//") + str(_sample.id),file=sys.stderr)
                if _sample.status != "COMPLETED":
                    for c in _sample.cost:
                        if listOfMoleculesToGrab[c]<(_sample.cost[c]-plInstance.expertise[c]) and molAvailable[c]>0:
                            print("CONNECT " + c)
                            grabMolecule = True
                            break
                if grabMolecule:
                    break
            if not grabMolecule:
                finishedOne = False
                for _sample in plInstance.samples:
                    if _sample.status == "COMPLETED":
                        finishedOne = True
                        break
                if finishedOne:
                    print("GOTO LABORATORY")
                else:
                    print("WAIT")
        else:
            print("GOTO LABORATORY")
    elif plInstance.target == 'LABORATORY':
        goOut=True
        for _sample in plInstance.samples:
            print("$$$$ " + str(_sample.id) + "//" + str(_sample.status),file=sys.stderr)
            if _sample.status == "COMPLETED":
            #if plInstance.checkSampleStatus(_sample) == "COMPLETED":
                print("CONNECT " + str(_sample.id))
                plInstance.nbSampleAnalyzed+=1
                goOut=False
                break
        if goOut:
            if SampleData.getNbFreeSample()>2:
                print("GOTO DIAGNOSIS")
            else:
                print("GOTO SAMPLES")
    elif plInstance.target == "SAMPLES":
        if len(plInstance.samples)>2 or SampleData.getNbFreeSample()>2:
            print ("GOTO DIAGNOSIS")
        elif plInstance.nbSampleAnalyzed>5 and len(plInstance.samples)<1:
            print("CONNECT 3")
        elif plInstance.nbSampleAnalyzed > 5 and len(plInstance.samples) > 1 :
            print("CONNECT 2")
        elif plInstance.nbSampleAnalyzed>3 and len(plInstance.samples)<2:
            print("CONNECT 2")
        elif plInstance.nbSampleAnalyzed<4 and len(plInstance.samples)<21:
            print("CONNECT 2")
        #elif plInstance.nbSampleAnalyzed > 3 and len(plInstance.samples) > 1:
        else:
            print("CONNECT 1")

    elif plInstance.target == 'START_POS':
        print("GOTO SAMPLES ")




