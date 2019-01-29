import os
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters 
import logging
import Utils.sad as sad
import Utils.commandManager as commandManager
import Utils.utils as utils
import Utils.logManager as logManager
import configManager as configManager

def generateBot(testFlag = True):
    config = configManager.getConfig()
    TOKEN = config.get(sad._CONFIG_RAVEGEN_SECTION_, sad._CONFIG_TOKEN_OPTION_)
    if(testFlag == True):
        _generateBot(TOKEN)
    else:
        webhookURL = configManager.get(config, sad._CONFIG_RAVEGEN_SECTION_, sad._CONFIG_DEPLOY_URL_OPTION)
        port = configManager.get(config, sad._CONFIG_RAVEGEN_SECTION_, sad._CONFIG_DEPLOY_PORT_OPRION)
        webhookPath = configManager.get(config, sad._CONFIG_RAVEGEN_SECTION_, sad._CONFIG_WEBHOOK_PATH_OPTION)
        _generateBot(TOKEN, webhookURL, port, webhookPath)

def deployBot(withOptions = False, testFlag = True, generateFlag = True):
    if(withOptions == False):
        if utils.file_Or_Directory_Exists(sad._ACTUAL_PATH, sad._OUTPUT_BOT_DIR_):
            if utils.file_Or_Directory_Exists(sad._OUTPUT_BOT_DIR_, sad._OUTPUT_BOT_NAME_):
                generateFlag = False                
    if(generateFlag == True):
        generateBot(testFlag)
    if(testFlag == True):
        logManager.printVerbose("Running Test Bot")
        commandManager.runPythonCommand(sad.OUTPUT_BOT_PATH)
        commandManager.runRmCommand(sad._MODULES_DIR_ + sad._DF_ + sad._LINUX_ALL_TAG_ + sad._PYC_EXTENTION)        
    #TODO deploy bot in heroku


def changeState(testFlag):
    if(testFlag == True):
        deployBot(withOptions=True)
    else:
        logManager.printVerbose("Changing to deploy mode...")
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        logger = logging.getLogger(__name__)        
        config = configManager.getConfig()
        updater = Updater(config.get(sad._CONFIG_RAVEGEN_SECTION_, sad._CONFIG_TOKEN_OPTION_))
        webhookURL = configManager.get(config, sad._CONFIG_RAVEGEN_SECTION_, sad._CONFIG_DEPLOY_URL_OPTION)
        webhookPath = configManager.get(config, sad._CONFIG_RAVEGEN_SECTION_, sad._CONFIG_WEBHOOK_PATH_OPTION)
        if(webhookURL[-1] == '/'):
            webhookURL = webhookURL[:-1]
        if(webhookPath[-1] == '/'):
            webhookPath = webhookPath[:-1]
        webhookURL += sad._DF_ + webhookPath
        logManager.printVerbose("Changing webhook to: " + webhookURL)
        updater.bot.setWebhook(webhookURL)
        logManager.printVerbose("DONE")

def _generateBot(TOKEN, webhookURL = None, port = None, webhookPath = None):
    commandManager.runMkdirCommand(sad._OUTPUT_BOT_DIR_)
    commandManager.runLsCommand(sad._MODULES_DIR_, writeFile=sad._TEMP_LS_MODULES_FILE_NAME)
    modules = []
    tempLsFile = open(sad._TEMP_LS_MODULES_FILE_NAME, 'r')

    for line in tempLsFile:
        modules.append(line.rstrip('\n'))

    tempLsFile.close()

    modules = [module.split('.')[0] for module in modules if module.split('.')[1] == sad._MODULES_EXTENTION_]
    commandManager.runRmCommand(sad._TEMP_LS_MODULES_FILE_NAME)
    outputBotFile = open(sad.OUTPUT_BOT_PATH, 'w')
    outputBotFile.write("from telegram.ext import Updater, CommandHandler, MessageHandler, Filters \n")
    outputBotFile.write("import logging \n")
    outputBotFile.write("import os \n")
    outputBotFile.write("import sys \n")
    outputBotFile.write("sys.path.insert(0, '" + sad._MODULES_DIR_ + "')\n")
    for module in modules:
        outputBotFile.write("from " + module + " import *\n")
    outputBotFile.write('\n')
    outputBotFile.write("if __name__ == \"__main__\":\n")
    outputBotFile.write("\tTOKEN = \"" + TOKEN + "\"\n")
    if(webhookURL != None):
        if(port == None):
            outputBotFile.write("\tPORT = os.environ.get('PORT')\n")    
        else:
            outputBotFile.write("\tPORT = " + str(port) + "\n")

    
    outputBotFile.write("\tlogging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)\n")
    outputBotFile.write("\tlogger = logging.getLogger(__name__)\n")
    outputBotFile.write("\tupdater = Updater(TOKEN)\n")
    outputBotFile.write("\tdispatcher = updater.dispatcher\n")
    for module in modules:
        outputBotFile.write("\t" + module + "_handler = CommandHandler('" + module + "'," + module + ")\n")
        outputBotFile.write("\tdispatcher.add_handler(" + module + "_handler)\n")
    
    if(webhookURL != None):
        if(webhookPath == None):
            outputBotFile.write("\tupdater.start_webhook(listen=\"0.0.0.0\", port=int(PORT), url_path=TOKEN)\n")
            webhookURL += sad._DF_ + webhookPath
        else:
            outputBotFile.write("\tupdater.start_webhook(listen=\"0.0.0.0\", port=int(PORT), url_path=\"" + webhookPath + "\")\n")
        outputBotFile.write("\tupdater.bot.setWebhook(\"" + webhookURL + "\")\n")
    else:
        outputBotFile.write("\tupdater.bot.deleteWebhook()\n")
        outputBotFile.write("\tupdater.start_polling()\n")


    outputBotFile.write("\tupdater.idle()\n")
    outputBotFile.close()