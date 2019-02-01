import os
import sad

def runMkdirCommand(directory, *args):
    _executeCommand(sad._LINUX_MKDIR_COMMAND_, directory, args)

def runRmCommand(file, *args):
    _executeCommand(sad._LINUX_RM_COMMAND_, file, args)

def runRmDirCommand(directory, *args):
    _executeCommand(sad._LINUX_RM_COMMAND_DIR, directory, args)

def runLsCommand(directory, writeFile = None):
    _executeCommand(sad._LINUX_LS_COMMAND_, directory, [], writeFile=writeFile)

def runPythonCommand(pythonFile, *args):
    _executeCommand(sad._LINUX_PYTHON_COMMAND_, pythonFile, args)

def runHerokuCreateCommand(projectName):
    _executeCommand(sad._LINUX_HEROKU_COMMAND_, sad._LINUX_HEROKU_CREATE_OPTION_, [projectName])

def runHerokuInfoCommand(projectName, writeFile = None):
    _executeCommand(sad._LINUX_HEROKU_COMMAND_, sad._LINUX_HEORKU_INFO_OPTION_, [projectName], writeFile=writeFile)

def runHerokuDestroyCommand(projectName):
    _executeCommand(sad._LINUX_HEROKU_COMMAND_, sad._LINUX_HEROKU_DESTORY_OPTION_, [projectName, sad._LINUX_HEROKU_DESTROY_CONFIRM_, projectName])

def _executeCommand(command, fistrArg, args, writeFile = None):
    command = command + fistrArg
    for arg in args:
        command += " " + arg
    if(writeFile != None):
        command += sad._LINUX_WRITE_ERROR_COMMAND_ + writeFile 
        command += sad._LINUX_WRITE_COMMAND_ + writeFile
    os.system(command)
