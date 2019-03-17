import re, string, argparse

class State:
    def __init__(self, name):
        self.epsilonClosure = []
        self.transitions = {}
        self.name = name
        self.isEnd = False

class DfaState:
    def __init__(self, name):
        self.transitions = {}
        self.list = []
        self.name = name
        self.isEnd = False

class Dfa:
    def __init__(self, parsed):
        self.states = []
        self.visitedDfa = []
        self.secondIndex = 0
        self.letters = string.ascii_uppercase
        self.start = ""
        self.end = []
        self.dead = False
        self.dfaStart = ""
        self.dfaEnd = []
        self.alphabet = []
        self.handleParse(parsed)
        self.index = 0
        self.calculateDfa()
        self.geneticAlgorithm()
        self.markStates()
        self.markEndStates()
        self.printResult()

    def getCharName(self):
        letter = ""
        if self.index == 26:
            self.index = 0
            self.secondIndex +=1
        if self.secondIndex == 0:
            letter = self.letters[self.index]
        else:
            letter = self.letters[self.index] + str(self.secondIndex)
        self.index += 1
        return letter

    def markStates(self):
        for i in self.visitedDfa:
            print(i.name+":",end =" ")
            for j in i.list:
                print(j.name,end =" ")
            print("")

    def markEndStates(self):
        for i in self.visitedDfa:
            for j in i.list:
                if j.isEnd:
                    i.isEnd = True

    def createDfa(self):
        dfa1 = DfaState(self.getCharName())
        return dfa1

    def extendE(self, dfa):
        for i in dfa.list:
            for x in i.epsilonClosure:
                if x not in dfa.list:
                    dfa.list.append(x)
        return dfa

    def calculateDfa(self):
        startState = self.getStateByName(self.start.name)
        dfa1 = self.createDfa()
        dfa1.list.append(startState)
        self.dfaStart = dfa1.name
        dfa1 = self.extendE(dfa1)
        self.visitedDfa.append(dfa1)
        
    def geneticAlgorithm(self):
        for i in self.visitedDfa:
            for j in self.alphabet:
                check = False
                newdfa = self.createDfa()
                for k in i.list:
                    if j in k.transitions:
                        check = True
                        newdfa.list.append(k.transitions[j])
                newdfa = self.extendE(newdfa)
                visited, stateN = self.checkNotVisited(newdfa)
                if not check:
                    self.index -= 1
                    i.transitions[j] = "DEAD"
                    self.dead = True
                else:
                    if visited:
                        self.visitedDfa.append(newdfa)
                    else:
                        self.index -= 1
                        newdfa.name = stateN.name
                    i.transitions[j] = newdfa

                
    def checkNotVisited(self, dfa):
        checkList = []
        for k in dfa.list:
            checkList.append(k.name)
        for i in self.visitedDfa:
            namesList = []
            for x in i.list:
                namesList.append(x.name)
            if set(namesList) == set(checkList):
                return False, i
        return True, ""
            
    def printStates(self):
        newList = []
        for i in self.visitedDfa:
            newList.append(i.name)
        if self.dead:
            newList.append("DEAD")
        print(*newList, sep=', ')
        return self.print2(newList)

    def printAlphabet(self):
        print(*self.alphabet, sep=',')
        return self.print1(self.alphabet)

    def printStartState(self):
        print(self.dfaStart)
        return(self.dfaStart)
        
    def printFinalState(self):
        newList = []
        for i in self.visitedDfa:
            if i.isEnd:
                newList.append(i.name)
        print(*newList, sep=', ')
        return self.print2(newList)

    def printTransitions(self):
        newList = []
        for i in self.visitedDfa:
            for k in self.alphabet:
                if i.transitions[k] == "DEAD":
                    newList.append("("+i.name+", "+k+", DEAD)")
                else:    
                    newList.append("("+i.name+", "+k+", "+i.transitions[k].name+")")
        if self.dead:
            for t in self.alphabet:
                newList.append("(DEAD, "+t+", DEAD)")
        print(*newList, sep=', ')
        return self.print2(newList)

    def print1(self, x):
            return ','.join(map(str, x))

    def print2(self, x):
        return ', '.join(map(str, x))

    def printResult(self):
        output_file = open("task_2_2_result.txt", "w+", encoding="utf-8")
        output_file.write(self.printStates() + "\n")
        output_file.write(self.printAlphabet() + "\n")
        output_file.write(self.printStartState() + "\n")
        output_file.write(self.printFinalState() + "\n")
        output_file.write(self.printTransitions() + "\n")    

    def handleParse(self, parsed):
        alphabet = parsed[1]
        start = parsed[2]
        end = parsed[3]
        transitions = parsed[4]
        self.addAllStates(transitions)
        self.setFinalStates(end.split(","))
        self.setAlphabet(alphabet)
        self.setStartState(start)

    def setFinalStates(self, end):
        for i in end:
            self.getStateByName(i).isEnd = True

    def setStartState(self, start):
        for i in self.states:
            if i.name == start:
                self.start = i

    def setAlphabet(self, x):
        f = x.split(",")
        newList = []
        for i in f:
            if i != " ":
                newList.append(i)
        self.alphabet = newList

    def checkStateName(self, name):
        for i in self.states:
            if i.name == name:
                return False
        return True

    def getStateByName(self, name):
        for i in self.states:
            if i.name == name:
                return i

    def handleAddingStates(self, finalParse):
        s1 = finalParse[0]
        trans = finalParse[1]
        s2 = finalParse[2]
        if self.checkStateName(s1):
            s11 = State(s1)
            self.states.append(s11)
        if self.checkStateName(s2):
            s12 = State(s2)
            self.states.append(s12)
        if trans == "":
            self.getStateByName(s1).epsilonClosure.append(self.getStateByName(s2)) 
        else:
            self.getStateByName(s1).transitions[trans] = self.getStateByName(s2)
        

    def addAllStates(self, transitions):
        splitted = re.findall(r'\(\w+\, \w?\, \w+\)', transitions)
        parseTransition = []
        for i in splitted:
            new = i.replace("(", "")
            new = new.replace(")", "")
            parseTransition.append(new)
        finalParse = []
        for i in parseTransition:
            finalParse = i.split(", ")
            self.handleAddingStates(finalParse)
           
def parseInput(x):
    newList = []
    for i in x:
        new = i.replace("\n", "")
        newList.append(new)
    return newList

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",
                        metavar="file")

    args = parser.parse_args()

    print(args.file)
    lines = []
    with open(args.file, "r") as f:
        for line in f:
            lines.append(line)
    parsed = parseInput(lines)
    Dfa(parsed)
