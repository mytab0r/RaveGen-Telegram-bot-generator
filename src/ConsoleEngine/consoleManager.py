import os
import readline
import Utils.sad as sad
import Utils.errorHandler as errorHandler

consoleErrorHandler = errorHandler.ErrorHandler("Console Manager")

#TODO ver como hacer esto en la instalacion
_CONSOLE_ENGINE_COMMANDS_FILE_PATH = "/home/xnpiochv/Documentos/Rave_Gen/src/ConsoleEngine/commands"

def verifyArgs(argv):
    if(len(argv) < 2):
        consoleErrorHandler.addError("Args needed", sad._CRITICAL_ERROR_)
        printHelp()
    commands, commandsInfo = getConsoleCommands()
    ansFatherCommand = None
    for i in range(1, len(argv)):
        command = argv[i]
        if(ansFatherCommand == None):
            if _is_Father(command) == False:
                consoleErrorHandler.addError("Command " + command + " dosen't exists", sad._CRITICAL_ERROR_)
            else:
                if command in commands:
                    ansFatherCommand = command
                else:
                    consoleErrorHandler.addError("Command " + command + " dosen't exists", sad._CRITICAL_ERROR_)
        else:
            if _is_Father(command) == True:
                consoleErrorHandler.addError("Command " + ansFatherCommand + " and command " + command + " can't be together", sad._CRITICAL_ERROR_)
            else:
                options = _splitOptions(command)
                for option in options:
                    if not option in commandsInfo[ansFatherCommand][sad._CONSOLE_ENGINE_OPTION_TAG_]:
                        consoleErrorHandler.addError("Command " + ansFatherCommand + " dosen't have option " + option, sad._CRITICAL_ERROR_)
                    
    consoleErrorHandler.handle()

def printHelp():
    _, commandsInfo = getConsoleCommands()
    print("Rave Gen - By ChrisChV")
    print("Program for generate basic telegram bots with python-telegram-bot")
    print("COMMANDS\n")
    for command, info in commandsInfo.iteritems():
        print("\t" + command + ": " + info[sad._CONSOLE_ENGINE_INFO_OPTION_])
        if(len(info[sad._CONSOLE_ENGINE_OPTION_TAG_]) > 0):
            print("\tOPTIONS")
            for option, optionInfo in info[sad._CONSOLE_ENGINE_OPTION_TAG_].iteritems():
                print("\t\t-" + option + ": " + optionInfo)
        

def getConsoleCommands():
    commandsFile = open(_CONSOLE_ENGINE_COMMANDS_FILE_PATH, 'r')
    commandsInfo = {}
    commands = []
    for line in commandsFile:
        tokens = line.split(" ")
        infoString = ""
        for i in range(2, len(tokens)):
            infoString += tokens[i] + " "
        infoString = infoString[:-1]
        infoString = infoString.rstrip('\n')
        if tokens[1] == 'None':
            tempDic = {sad._CONSOLE_ENGINE_OPTION_TAG_: {}, sad._CONSOLE_ENGINE_INFO_OPTION_: infoString}
            commandsInfo[tokens[0]] = tempDic
            commands.append(tokens[0])
        else:
            commandsInfo[tokens[1]][sad._CONSOLE_ENGINE_OPTION_TAG_][tokens[0]] = infoString
    commandsFile.close()
    return commands, commandsInfo

def getOptions(argv):
    options = []
    for i in range(2,len(argv)):
        option = argv[i]
        options += _splitOptions(option)
    return options


    

def _setAutocompleter():
    readline.parse_and_bind("tab: complete")
    readline.set_completer(_completer)

def _completer(text, state):
    commands, _ = getConsoleCommands()
    options = [i for i in commands if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

def _is_Father(command):
    if(command[0] == '-'):
        return False
    else:
        return True
    

def _splitOptions(command):
    options = []
    for i in range(1,len(command)):
        options.append(command[i])
    return options


