import sys
import math
from random import randint

class MarvinQuotes:
    listOfQuotes=[
        'I think you ought to know I’m feeling very depressed.',
        'I am at a rough estimate thirty billion times more intelligent than you.',
        'You can blame the Sirius Cybernetics Corporation for making androids with GPP…',
        'I have a million ideas. They all point to certain death.',
        'I could calculate your chance of survival, but you won’t like it.',
        'how just when you think life can’t possibly get any worse it suddenly does.',
        'I’d give you advice, but you wouldn’t listen. No one ever does',
        'And then of course I’ve got this terrible pain in all the diodes down my left side.',
        'Don’t pretend you want to talk to me, I know you hate me.'
    ]
    @staticmethod
    def getQuote():
        val = randint(0, 1)
        if val == 1:
            val = randint(0, len(MarvinQuotes.listOfQuotes) - 1)
            return MarvinQuotes.listOfQuotes[val]
        else:
            return ""

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
        status = "COMPLETED" if goOn else "INPROGRESS"
        return status

    def checkAllSampleStatus(self):
        for _sample in self.samples:
            _sample.status="INPROGRESS"
        for i in (3,2,1):
            for _sample in self.samples:
                if _sample.rank == i:
                    _sample.status = self.checkSampleStatus(_sample)

    def addSample(self,_sample):
        #_sample.status = self.checkSampleStatus(_sample)

        self.samples.append(_sample)
        self.checkAllSampleStatus()
        print("bbb " + str(_sample.id) + "//" + str(_sample.status) + "//" + str(_sample.diagState) + "//" + str(
            _sample.cost), file=sys.stderr)

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
        self.rank=0
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
            totalMol=-1
            print("BEST " + str(sampleID) + "//" + str(sample.carriedBy) + "//", file=sys.stderr)
            if sample not in listOfSample and sample.carriedBy==-1:
                total = 0
                for c in sample.cost:
                    if sample.cost[c] > 0:
                        total += sample.cost[c] - Player.getInstance().expertise[c]
                if foundSample is None  or foundSample.health < sample.health :
                    foundSample = sample
                    totalMol = total
                elif foundSample.health == sample.health:
                    if total<totalMol or totalMol==-1:
                        foundSample = sample
                        totalMol = total
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
            print("EXPERTISE " + str(plInstance.expertise), file=sys.stderr)

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
        tempSampleData.rank = rank
        tempSampleData.cost['A']=cost_a
        tempSampleData.cost['B']=cost_b
        tempSampleData.cost['C']=cost_c
        tempSampleData.cost['D']=cost_d
        tempSampleData.cost['E']=cost_e
        tempSampleData.health=health
        tempSampleData.id=sample_id
        tempSampleData.carriedBy = carried_by

        if carried_by == 0:
            plInstance.addSample(SampleData.listOfInstance[sample_id])

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    quote = MarvinQuotes.getQuote()
    print(plInstance.target,file=sys.stderr)
    if plInstance.target == 'DIAGNOSIS':
        if plInstance.eta == 0:
            action=False
            for _sample in plInstance.samples:
                if _sample.diagState in ("NEW"):#,"DIAGNOSED"):
                    print("CONNECT " + str(_sample.id) + " " + quote)
                    _sample.diagState = "DIAGNOSED" if _sample.diagState == "NEW" else "INCLOUD"
                    action = True
                    break

            if not action:
                storageSize=0
                for s in plInstance.storage:
                    storageSize+=plInstance.storage[s]
                if len(plInstance.samples)<3:
                    sample = SampleData.getBestSample(plInstance.samples)
                    if sample is not None:
                        print("CONNECT " + str(sample.id))
                        sample.diagState = "INCLOUD"
                    else:
                        print("GOTO MOLECULES " + quote)
                elif storageSize==10:
                    maxSize=-1
                    sample = None
                    for s in plInstance.samples:
                        total=0
                        for c in s.cost:
                            if s.cost[c] > 0:
                                total+=s.cost[c] - plInstance.expertise[c]
                        if total > maxSize:
                            maxSize=total
                            sample=s
                    print("CONNECT " + str(sample.id))

                else:
                    print("GOTO MOLECULES " + quote)
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

            nbToFind=-1
            sampleToFind = None
            for _sample in plInstance.samples:
                if _sample.status != "COMPLETED":
                    ttotal=0
                    for c in _sample.cost:
                        if _sample.cost[c] > 0:
                            ttotal+=_sample.cost[c] - plInstance.expertise[c]
                    if nbToFind == -1 or ttotal < nbToFind:
                        nbToFind = ttotal
                        sampleToFind = _sample

            if sampleToFind is not None:
                for c in sampleToFind.cost:
                    if listOfMoleculesToGrab[c] < (sampleToFind.cost[c] - plInstance.expertise[c]) and molAvailable[c] > 0:
                        print("CONNECT " + c + " " + quote)
                        grabMolecule = True
                        break
            if not grabMolecule:
                for _sample in plInstance.samples:
                   print("MOL " + str(_sample.cost) + str("//") + str(_sample.id),file=sys.stderr)
                   if _sample.status != "COMPLETED":
                       for c in _sample.cost:
                           if listOfMoleculesToGrab[c]<(_sample.cost[c]-plInstance.expertise[c]) and molAvailable[c]>0:
                               print("CONNECT " + c + " " + quote)
                               grabMolecule = True
                               break
                   if grabMolecule:
                       break
            if not grabMolecule:
                finishedOne = False
                finishedAll = True
                for _sample in plInstance.samples:
                    if _sample.status == "COMPLETED":
                        finishedOne = True
                    else:
                        finishedAll = False
                if finishedAll:
                    print("GOTO LABORATORY " + quote)
                if finishedOne:
                    if target == "LABORATORY":
                        print("WAIT TTTT" +quote)
                    else:
                        print("GOTO LABORATORY " + quote)
                else:
                    print("WAIT " + quote)
        else:
            print("GOTO LABORATORY " + quote)
    elif plInstance.target == 'LABORATORY':
        goOut=True
        print("@@@@@@@@@@@@@@@@@",file=sys.stderr)
        plInstance.checkAllSampleStatus()
        #for _sample in plInstance.samples:
        #    print("BBBB " + str(_sample.id) + "//" + str(_sample.status), file=sys.stderr)
        for _sample in plInstance.samples:
            print("$$$$ " + str(_sample.id) + "//" + str(_sample.status),file=sys.stderr)
            if _sample.status == "COMPLETED":
            #if plInstance.checkSampleStatus(_sample) == "COMPLETED":
                print("CONNECT " + str(_sample.id) + " CHECK")
                plInstance.nbSampleAnalyzed+=1
                goOut=False
                break
        if goOut:
            if len(plInstance.samples) == 3 :
                print("GOTO DIAGNOSIS " + quote)
            if len(plInstance.samples)>1:
                print("GOTO MOLECULES " + quote)
            elif SampleData.getNbFreeSample()>=2:
                print("GOTO DIAGNOSIS " + quote)
            else:
                print("GOTO SAMPLES " + quote)
    elif plInstance.target == "SAMPLES":
        expertiseSize = 0
        for e in plInstance.expertise:
            expertiseSize+=plInstance.expertise[e]

        if len(plInstance.samples) == 2:
            print("CONNECT 1")
        elif len(plInstance.samples) == 3:
            print ("GOTO DIAGNOSIS")
        elif expertiseSize<5:
            print("CONNECT 1")
        elif expertiseSize>8:
            print("CONNECT 3")
        else:
            print("CONNECT 2")




        # if len(plInstance.samples)>2 or SampleData.getNbFreeSample()>2:
        #     print ("GOTO DIAGNOSIS")
        # elif plInstance.nbSampleAnalyzed>8 and len(plInstance.samples)<1:
        #     print("CONNECT 3 " + quote)
        # #elif plInstance.nbSampleAnalyzed > 8 and len(plInstance.samples) > 1 :
        # #    print("CONNECT 2")
        # elif plInstance.nbSampleAnalyzed>5 and len(plInstance.samples)<2:
        #     print("CONNECT 2")
        # elif plInstance.nbSampleAnalyzed<5 and len(plInstance.samples)<1:
        #     print("CONNECT 2")
        # #elif plInstance.nbSampleAnalyzed > 3 and len(plInstance.samples) > 1:
        # else:
        #     print("CONNECT 1 " + quote)

    elif plInstance.target == 'START_POS':
        print("GOTO SAMPLES ")




