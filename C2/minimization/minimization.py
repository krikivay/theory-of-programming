# read comands of program f
program = []
file = open("f.urm")
argumentsSize = 2
program = file.read().split("\n")
comandsSize = len(program)
file.close()
    
    
startRegister = argumentsSize + 3
    
    
# add comand T to move data for f on coorect start Register
finalCommands = []
moveCommands = []
for i in range(0, argumentsSize+2):
        moveCommands += ["T("+ str(i) + "," + str(startRegister+i) + ")"]
  
finalCommands += moveCommands
    
    
for i, comand in enumerate(program):
    comand = comand.replace(" ", "")
        
    if comand[0] in "ZS":
        # move Register in interval accroding f start Register
        register = int(comand[2:-1])
        newRegister = register + startRegister
        program[i] = comand[:2] + str(newRegister) + comand[-1]
                
    if comand[0] == "T":
        cmnd = comand[2:-1].split(",")
        # move Register in interval accroding f start Register
        register1 = int(cmnd[0])
        newRegister1 = register1 + startRegister
        register2 = int(cmnd[1])
        newRegister2 = register2 + startRegister
        program[i] = comand[:2] + str(newRegister1) + "," + str(newRegister2) + comand[-1]
                
    if comand[0] == "J":
        cmnd = comand[2:-1].split(",")
        # move Register in interval accroding f start Register
        register1 = int(cmnd[0])
        newRegister1 = register1 + startRegister
        register2 = int(cmnd[1])
        newRegister2 = register2 + startRegister
               
        cmd = int(cmnd[2])
        # if number of comand is zero or over f's comand number
        # change it on number of next comand
        if (cmd == 0) or (cmd > comandsSize):
            cmd = len(moveCommands) + comandsSize + 1
        # else change comand number according to current comands count 
        else:
            cmd = len(moveCommands) + cmd
               
        program[i] = comand[:2] + str(newRegister1) + "," + str(newRegister2) + \
                                                                                     "," + str(cmd) + comand[-1]
            
finalCommands += program
    

# check if root is found
finalCommands += [f"J({argumentsSize+2},{startRegister}," + \
                                       f"{len(moveCommands) + comandsSize+4})"]
    
# end of program
finalCommands += [f"S({argumentsSize+1})"]
finalCommands += ["J(0,0,1)"]
finalCommands += [f"T({argumentsSize+1},0)"]
    
    
# write minimization program
superpos_file = open("minimization.urm", "w")
for comand in finalCommands:
    superpos_file.write(comand + "\n")
superpos_file.close()
print("minimization program was created")
