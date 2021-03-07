programs = ["f.urm", "g1.urm", "g2.urm", "g3.urm"]
argumentsSize = 2
programsSize = len(programs)

programsList = []
comandSize= []
maxRegisters = []
    
for i, program in enumerate(programs):
        
    # read comands of program
    file = open(program)
    comands = file.read().split("\n")
    programsList += [comands]
    comandSize += [len(comands)]
    file.close()
        
        
    # find all used registers for all comands of program
    registers = []
    for comand in comands:
        comand = comand.replace(" ", "")
        if comand[0] in "ZS":
            registers += [int(comand[2:-1])]
        if comand[0] == "T":
            cmnd = comand[2:-1].split(",")
            registers += [int(cmnd[1])]
        
    # add to registers count of arguments
    registers += [programsSize-1] if i == 0 else [argumentsSize]
        
    # find max for used register and number of argument
    maxRegisters += [max(registers)]
    
    
# start register for first program is 0
startRegisters = [0]
    
for i in range(1, programsSize):
    # start register for current program is sum of start register and
    # max used register for previous program increased by one
    startRegisters += [startRegisters[i-1] + maxRegisters[i-1] + 1]
        
    
# add comand T to move data on coorect start register
moveCommands = []
for i in range(1, programsSize):
    comands = programsList[i]
    for j in range(0, argumentsSize+1):
        moveCommands += ["T("+ str(j) + "," + str(startRegisters[i]+j) + ")"]
    
    
currentComandsSize = (argumentsSize+1) * (programsSize - 1)
    
    
# move command registers to correct intervals for all subprograms
for i in range(1, programsSize):
    comands = programsList[i]
        
    for j, comand in enumerate(comands):
        comand = comand.replace(" ", "")
        if comand[0] in "ZS":
            # move register in interval accroding start register
            register = int(comand[2:-1])
            newRegister = register + startRegisters[i]
            comands[j] = comand[:2] + str(newRegister) + comand[-1]
                
        if comand[0] == "T":
            cmnd = comand[2:-1].split(",")
            # move register in interval accroding start register
            register1 = int(cmnd[0])
            newRegister1 = register1 + startRegisters[i]
            register2 = int(cmnd[1])
            newRegister2 = register2 + startRegisters[i]
            comands[j] = comand[:2] + str(newRegister1) + "," + str(newRegister2) + comand[-1]
                
        if comand[0] == "J":
            cmnd = comand[2:-1].split(",")
            # move register in interval accroding start register
            register1 = int(cmnd[0])
            newRegister1 = register1 + startRegisters[i]
            register2 = int(cmnd[1])
            newRegister2 = register2 + startRegisters[i]
                
            cmd = int(cmnd[2])
            # if number of comand is zero or over program's comand number
            # change it on number of next comand
            if (cmd == 0) or (cmd > comandSize[i]):
                cmd = currentComandsSize + comandSize[i] + 1
            # else change comand number according to current comands count 
            else:
                cmd = currentComandsSize + cmd
                
            comands[j] = comand[:2] + str(newRegister1) + "," + str(newRegister2) + \
                                                                                     "," + str(cmd) + comand[-1]
    currentComandsSize += comandSize[i]


# add comand T to move result data on first registers
finalMoveCommands = []
for i in range(1, programsSize):
    finalMoveCommands += ["T("+ str(startRegisters[i]) + "," + str(i) + ")"]
        
        
currentComandsSize += programsSize - 1
    
    
# change comand number for f program because of last performing
comands = programsList[0]
for j, comand in enumerate(comands):
        comand = comand.replace(" ", "")

        if comand[0] == "J":
            cmd = int(comand[-2])
            # if number of comand is over program's comand number change it on zero
            if cmd > comandSize[0]:
                cmd = 0
            # else change comand number according to current comands count 
            elif cmd != 0:
                cmd = currentComandsSize + cmd
                
            comands[j] = comand[:6] + str(cmd) + comand[-1]
    
    
finalCommands = moveCommands
for i in range(1, programsSize):
    finalCommands += programsList[i]
finalCommands += finalMoveCommands
finalCommands += programsList[0]
    
# write superposition program
superposFile = open("superposition.urm", "w")
for comand in finalCommands:
    superposFile.write(comand + "\n")
superposFile.close()
print("superposition program was created")
