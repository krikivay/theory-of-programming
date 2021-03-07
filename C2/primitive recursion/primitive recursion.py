argumentsSize = 3
programs = {}
comandSize = {}
# read comands of program f
file = open("f.urm")
programs["f"] = file.read().split("\n")
comandSize["f"] = len(programs["f"])
file.close()
    
# read comands of program g
file = open("g.urm")
programs["g"] = file.read().split("\n")
comandSize["g"] = len(programs["g"])
file.close()
    
        
# find all used registers for all comands of program f
registers = []
comands = programs["f"]
for comand in comands:
    comand = comand.replace(" ", "")
    if comand[0] in "ZS":
        registers += [int(comand[2:-1])]
    if comand[0] == "T":
        cmnd = comand[2:-1].split(",")
        registers += [int(cmnd[1])]
        
# find max for used register and number of argument
maxRegister = max(registers+[argumentsSize])
   
    
# start register for f is number arguments of f plus 1
# start register for g is start register for f plus max used register for f plus 1
startRegisters = {"f": argumentsSize+2, "g": argumentsSize+2+maxRegister+1}

finalCommands = []
# star part comand
finalCommands += ["J(0,0,4)"]
# end part comands
finalCommands += [f"T({startRegisters['g']},0)"]
finalCommands += ["J(0,0,0)"]
currentComandsSize = 3
    
    
moveCommands = {"f": [], "g": []}
# add comand T to move data for f on coorect start register
for i in range(0, argumentsSize+1):
        moveCommands["f"] += ["T("+ str(i) + "," + str(startRegisters["f"]+i) + ")"]
    
finalCommands += moveCommands["f"]
currentComandsSize += argumentsSize + 1
    
    
comands = programs["f"]
for i, comand in enumerate(comands):
    comand = comand.replace(" ", "")
        
    if comand[0] in "ZS":
        # move register in interval accroding f start register
        register = int(comand[2:-1])
        newRegister = regis + startRegisters["f"]
        comands[i] = comand[:2] + str(new_regis) + comand[-1]
                
    if comand[0] == "T":
        cmnd = comand[2:-1].split(",")
        # move register in interval accroding f start register
        register1 = int(cmnd[0])
        newRegister1 = regis1 + startRegisters["f"]
        register2 = int(cmnd[1])
        newRegister2 = regis2 + startRegisters["f"]
        comands[i] = comand[:2] + str(new_regis1) + "," + str(new_regis2) + comand[-1]
                
    if comand[0] == "J":
        cmnd = comand[2:-1].split(",")
        # move register in interval accroding f start register
        register1 = int(cmnd[0])
        newRegister1 = regis1 + startRegisters["f"]
        register2 = int(cmnd[1])
        newRegister2 = regis2 + startRegisters["f"]
                
        cmd = int(cmnd[2])
        # if number of comand is zero or over f's comand number
        # change it on number of next comand
        if (cmd == 0) or (cmd > comandSize["f"]):
            cmd = currentComandsSize + comandSize["f"] + 1
        # else change comand number according to current comands count 
        else:
            cmd = currentComandsSize + cmd
                
        comands[i] = comand[:2] + str(new_regis1) + "," + str(new_regis2) + \
                                                                                     "," + str(cmd) + comand[-1]
            
finalCommands += comands
currentComandsSize += comandSize["f"]


# check recursion for continue
finalCommands += [f"T({startRegisters['f']},{startRegisters['g']})"]
finalCommands += [f"J({argumentsSize+1},{startRegisters['g']+argumentsSize+1},2)"]
currentComandsSize += 2
check_comand = currentComandsSize
    
# add comand T to move data for g on coorect start register
for i in range(1, argumentsSize+1):
    moveCommands["g"] += ["T("+ str(i) + "," + str(startRegisters["g"]+i) + ")"]
moveCommands["g"] += [f"T({startRegisters['g']},{startRegisters['g']+argumentsSize+2})"]
moveCommands["g"] += [f"T(0,{startRegisters['g']})"]
    
    
finalCommands += moveCommands["g"]
currentComandsSize += argumentsSize + 2
    
    
comands = programs["g"]
for i, comand in enumerate(comands):
    comand = comand.replace(" ", "")
        
    if comand[0] in "ZS":
        # move register in interval accroding g start register
        register = int(comand[2:-1])
        newRegister = regis + startRegisters["g"]
        comands[i] = comand[:2] + str(new_regis) + comand[-1]
                
    if comand[0] == "T":
        cmnd = comand[2:-1].split(",")
        # move register in interval accroding g start register
        register1 = int(cmnd[0])
        newRegister1 = regis1 + startRegisters["g"]
        register2 = int(cmnd[1])
        newRegister2 = regis2 + startRegisters["g"]
        comands[i] = comand[:2] + str(newRegister1) + "," + str(newRegister2) + comand[-1]
                
    if comand[0] == "J":
        cmnd = comand[2:-1].split(",")
        # move register in interval accroding g start register
        register1 = int(cmnd[0])
        newRegister1 = regis1 + startRegisters["g"]
        register2 = int(cmnd[1])
        newRegister2 = regis2 + startRegisters["g"]
                
        cmd = int(cmnd[2])
        # if number of comand is zero or over g's comand number
        # change it on number of next comand
        if (cmd == 0) or (cmd > comandSize["g"]):
            cmd = currentComandsSize + comandSize["g"] + 1
        # else change comand number according to current comands count 
        else:
            cmd = currentComandsSize + cmd
                
        comands[i] = comand[:2] + str(newRegister1) + "," + str(newRegister2) + "," + str(cmd) + comand[-1]
finalCommands += comands
currentComandsSize += comandSize["g"]
    
finalCommands += [f"S({startRegisters['g']+argumentsSize+1})"]
finalCommands += [f"J(0,0,{check comand})"]
currentComandsSize += 2
    
    
# write primitive recursion program
superposFile = open("primitive recursion.urm", "w")
for comand in finalCommands:
    superposFile.write(comand + "\n")
superposFile.close()
print("primitive recursion program was created")
