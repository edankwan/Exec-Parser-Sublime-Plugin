import sublime
import sublime_plugin
import shutil
import math
import datetime
import json
import os
import re

PROJECT_NAME = 'Exec Parser'
SETTING_FILENAME = 'ExecParser.sublime-settings'
COMMANDS_JSON_FILENAME = 'commands.json'
FOLDERS = {}
USER_PLUGIN_DIRECTORY = ''
USER_COMMANDS_DIRECTORY = ''
USER_COMMANDS_JSON_FILE_PATH = ''
USER_COMMAND_TEMPLATE_FILE_PATH = ''


class ExecParserCore:

    settings = None
    commands = None

    # A three dimensional list are used for the view panel
    viewPanelList = []
    viewPanelListIndexes = []

    pasteCommandId = ''
    duplicateCommandId = ''
    pasteCommandCache = None
    duplicateCommandCache = None

    updateDefaultCommandOnChange = False

    recentCommandList = []

    def init(cls):
        cls.settings = sublime.load_settings(SETTING_FILENAME)
        cls.install()
        cls.commands = cls.readCommandJSON('default')
        userCommands = cls.readCommandJSON('user')
        for commandId in userCommands:
            cls.commands[commandId] = userCommands[commandId]

        cls.updateDefaultCommandOnChange = cls.settings.get('update_default_command_on_change')
        cls.recentCommandList = cls.settings.get('recent_command_list')
        cls.updatePasteCommand(cls.settings.get('paste_command_id'), True)
        cls.updateDuplicateCommand(cls.settings.get('duplicate_command_id'), True)


        # check if all of the recentCommandList are available in the commands list
        # if the recent command doesn't exist anymore, remove it from the list
        recentCommandList = cls.recentCommandList
        commands = cls.commands
        hasChanged = False
        i = len(recentCommandList) - 1
        while i > -1:
            if commands.get(recentCommandList[i]) is None:
                recentCommandList.pop(i)
                hasChanged = True
            i = i - 1
        if hasChanged:
            cls.settings.set('recent_command_list', cls.recentCommandList)
            cls.saveSetting()

        cls.setRecentCommand(cls.pasteCommandId)

    def install(cls):
        defaultDirectory = FOLDERS['default']
        USER_PLUGIN_DIRECTORY = FOLDERS['user']
        if not os.path.exists(USER_PLUGIN_DIRECTORY):
            os.makedirs(USER_PLUGIN_DIRECTORY)
        if not os.path.exists(USER_COMMANDS_JSON_FILE_PATH):
            try:
                f = open(USER_COMMANDS_JSON_FILE_PATH,'w+')
            except(IOError) as e:
                sublime.error_message('"' + USER_COMMANDS_JSON_FILE_PATH + '" commands file is not writable')
            else:
                f.write('{}')
                f.close()
        try:
            os.makedirs(USER_COMMANDS_DIRECTORY)
        except(OSError) as e:
            pass

    def readCommandJSON(cls, directory):
        try:
            f = open(os.path.join(FOLDERS[directory], COMMANDS_JSON_FILENAME), 'r')
        except(IOError) as e:
            sublime.error_message('"' + directory + '" commands file is not readable')
            return {}
        else:
            try:
                commands = json.loads(f.read())
            except(ValueError) as e:
                f.close()
                sublime.error_message('"' + directory + '" commands is not a valid json file.')
                return {}
            else:
                f.close()
                return commands

    def createListItem(cls, commandId):
        command = cls.commands.get(commandId)
        return [
            command['name'],
            command['description']
        ]

    def updateViewPanelList(cls):
        viewPanelList = cls.viewPanelList = []
        viewPanelListIndexes = cls.viewPanelListIndexes = []
        recentCommandList = cls.recentCommandList

        # put all recent commands to the viewPanelList
        for i in range(0, len(recentCommandList)):
            commandId = recentCommandList[i]
            viewPanelList.append(cls.createListItem(commandId))
            viewPanelListIndexes.append(commandId)

        commands = cls.commands
        tmpList = []
        # put all commands in the list
        for commandId in commands:
            if commandId not in recentCommandList:
                listItem = cls.createListItem(commandId)
                listItem.append(commandId)
                tmpList.append(listItem)
        # use alphabetical order for the rest of the commands
        def keyFunc(item):
            return item[0]
        tmpList.sort(key=keyFunc)
        for i in range(0, len(tmpList)):
            viewPanelListIndexes.append(tmpList[i].pop())
        viewPanelList.extend(tmpList)

    def setRecentCommand(cls, commandId):
        recentCommandList = cls.recentCommandList
        i = len(recentCommandList) - 1
        while i > -1:
            if recentCommandList[i] == commandId:
                recentCommandList.pop(i)
                break
            i = i - 1
        cls.recentCommandList.insert(0, commandId)
        cls.settings.set('recent_command_list', cls.recentCommandList)
        cls.updateViewPanelList()

    def updateCommandList(cls):
        recentCommandList = cls.recentCommandList
        viewPanelList = cls.viewPanelList = recentCommandList

    def getCommandData(cls, commandId):
        try:
            command = cls.commands[commandId]
        except(KeyError) as e:
            sublime.error_message('Command "' + commandId + '" does not exist')
            return ''
        else:
            filename = os.path.join(FOLDERS[command['directory']], 'commands', command['filename'] + '.py')
            try:
                f = open(filename, 'r')
            except(IOError) as e:
                sublime.error_message('Exer Parser plugin error: File "' + filename + '" not found.')
                return ''
            else:
                data = f.read()
                f.close()
                return data

    def updatePasteCommand(cls, commandId, isInit = False, forceUpdate = False):
        if (cls.pasteCommandId != commandId) or (forceUpdate):
            cls.pasteCommandId = commandId
            cls.pasteCommandCache = cls.getCommandData(commandId)
            if not isInit:
                cls.setRecentCommand(commandId)
                if cls.updateDefaultCommandOnChange:
                    cls.settings.set('paste_command_id', commandId)
                cls.saveSetting()


    def updateDuplicateCommand(cls, commandId, isInit = False, forceUpdate = False):
        if (cls.duplicateCommandId != commandId) or (forceUpdate):
            cls.duplicateCommandId = commandId
            cls.duplicateCommandCache = cls.getCommandData(commandId)
            if not isInit:
                cls.setRecentCommand(commandId)
                if cls.updateDefaultCommandOnChange:
                    cls.settings.set('duplicate_command_id', commandId)
                cls.saveSetting()

    def saveSetting(cls):
        sublime.save_settings(SETTING_FILENAME)

    def getAvailableUserCommandFileName(cls):
        i = 1
        while True:
            filename = 'untitled-' + str(i)
            if os.path.exists(os.path.join(USER_COMMANDS_DIRECTORY, filename) +'.py'):
                i = i + 1
            else:
                return filename

    def getAvailableUserCommandSuffix(cls):
        jsonData = cls.readCommandJSON('user')
        i = 1
        while True:
            if 'untitled_' + str(i) in jsonData:
                i = i + 1
            else:
                return str(i)


    init = classmethod(init)
    install = classmethod(install)
    readCommandJSON = classmethod(readCommandJSON)
    createListItem = classmethod(createListItem)
    updateViewPanelList = classmethod(updateViewPanelList)
    setRecentCommand = classmethod(setRecentCommand)
    updateCommandList = classmethod(updateCommandList)
    getCommandData = classmethod(getCommandData)
    updatePasteCommand = classmethod(updatePasteCommand)
    updateDuplicateCommand = classmethod(updateDuplicateCommand)
    saveSetting = classmethod(saveSetting)

    getAvailableUserCommandFileName = classmethod(getAvailableUserCommandFileName)
    getAvailableUserCommandSuffix = classmethod(getAvailableUserCommandSuffix)

class ExecParserUserCommandOptionsCommand(sublime_plugin.TextCommand):

    mainMenu = [
        ['Reinitialize commands', 'Everytime you updated the user\'s command or ' + COMMANDS_JSON_FILENAME + ', you need to call this function to reinitialize the plugin.'],
        ['Edit '+ COMMANDS_JSON_FILENAME, 'Edit the json file that stores the list of all the user\'s commands.'],
        ['Add new command', 'Add a new user command.'],
        ['Edit command', 'Edit an user command.'],
        ['Remove command', 'Remove an user command.']
    ]

    userCommands = None
    userViewPanelList = []
    userViewPanelListIndexes = []

    def run(self, edit):
        sublime.set_timeout(lambda: self.view.window().show_quick_panel(self.mainMenu, self.onMainMenuUpdate), 1)
        # ExecParserCore.init()

    def onMainMenuUpdate(self, index):
        if index == 0:
            ExecParserCore.init()
        elif index == 1:
            sublime.set_timeout(lambda: self.view.window().open_file(USER_COMMANDS_JSON_FILE_PATH), 1)
        elif index == 2:
            self.showAddInput()
        elif (index == 3) or (index == 4):
            self.userCommands = ExecParserCore.readCommandJSON('user')
            self.userViewPanelList = []
            self.userViewPanelListIndexes = []
            for commandId in self.userCommands:
                self.userViewPanelList.append(ExecParserCore.createListItem(commandId))
                self.userViewPanelListIndexes.append(commandId)
            if len(self.userViewPanelList) == 0:
                sublime.error_message('Cannot find any user command.')
            elif index == 3:
                sublime.set_timeout(lambda: self.view.window().show_quick_panel(self.userViewPanelList, self.onEdit), 1)
            elif index == 4:
                sublime.set_timeout(lambda: self.view.window().show_quick_panel(self.userViewPanelList, self.onRemove), 1)

    def onEdit(self, index):
        if index < 0: return
        commandId = self.userViewPanelListIndexes[index]
        command = self.userCommands[commandId]
        filePath = os.path.join(USER_COMMANDS_DIRECTORY, command.get('filename') + '.py')
        if os.path.exists(filePath):
            sublime.set_timeout(lambda: self.view.window().open_file(filePath), 100)
        else:
            sublime.error_message('"' + filePath + '" does not exist.')

    def onRemove(self, index):
        if index < 0: return
        commandId = self.userViewPanelListIndexes[index]
        command = self.userCommands[commandId]
        filePath = os.path.join(USER_COMMANDS_DIRECTORY, command.get('filename') + '.py')
        if os.path.exists(filePath):
            try:
                f = open(USER_COMMANDS_JSON_FILE_PATH,'w+')
            except(IOError) as e:
                sublime.error_message('"' + directory + '" commands file is not writable')
            else:
                os.remove(filePath)
                del self.userCommands[commandId]
                f.write(json.dumps(self.userCommands, indent=4, sort_keys=False))
                f.close()
                ExecParserCore.init()
        else:
            sublime.error_message('"' + filePath + '" does not exist.')


    def showAddInput(self):
            sublime.set_timeout(lambda: self.view.window().show_input_panel('Filename: ', ExecParserCore.getAvailableUserCommandFileName(), self.onAdd, None, None), 1)

    def onAdd(self, filename):
        filePath = os.path.join(USER_COMMANDS_DIRECTORY, filename + '.py')
        if os.path.exists(filePath):
            sublime.error_message('File "' + filePath + '" already exists')
            self.showAddInput()
            return
        jsonData = ExecParserCore.readCommandJSON('user')
        suffix = ExecParserCore.getAvailableUserCommandSuffix()
        jsonData['untitled_' + suffix] = json.loads('{ "name" : "Untitled ' + suffix + '", "description" : "A user command", "directory" : "user", "filename" : "' + filename + '"}')

        try:
            f = open(USER_COMMANDS_JSON_FILE_PATH,'w+')
        except(IOError) as e:
            sublime.error_message('"' + directory + '" commands file is not writable')
        else:
            f.write(json.dumps(jsonData, indent=4, sort_keys=False))
            f.close()
        shutil.copyfile(USER_COMMAND_TEMPLATE_FILE_PATH, filePath)
        window = self.view.window()
        sublime.set_timeout(lambda: window.open_file(USER_COMMANDS_JSON_FILE_PATH), 100)
        sublime.set_timeout(lambda: window.open_file(filePath), 150)

class ExecParserSetCommand(sublime_plugin.TextCommand):

    commandId = ''
    menu = [
        ['All', 'Apply the selected command to all parsers'],
        ['Paste only', 'Only apply the selected command to paste parser'],
        ['Duplicate only', 'Only apply the selected command to duplicate parser']
    ]

    def run(self, edit):
        sublime.set_timeout(lambda: self.view.window().show_quick_panel(ExecParserCore.viewPanelList, self.onCommandUpdate), 1)

    def onCommandUpdate(self, index):
        if index < 0: return
        self.commandId = ExecParserCore.viewPanelListIndexes[index]
        sublime.set_timeout(lambda: self.view.window().show_quick_panel(self.menu, self.onApplyToUpdate), 1)

    def onApplyToUpdate(self, index):
        if index < 0: return
        if (index == 0) or (index == 1):
            ExecParserCore.updatePasteCommand(self.commandId)
        if (index == 0) or (index == 2):
            ExecParserCore.updateDuplicateCommand(self.commandId)

class ExecParserPasteCommand(sublime_plugin.TextCommand):

    def parseText(self, selectionText, clipboardText, lineIndex, numOfLines):
        parserType = 'paste'
        output = clipboardText
        localDict = locals()
        exec(ExecParserCore.pasteCommandCache, None, localDict)
        return localDict['output']

    def run(self, edit):
        clipboardText = sublime.get_clipboard()
        lines = clipboardText.splitlines()
        regions = self.view.sel()

        if (len(regions) > 1) and (len(regions) == len(lines)):
            i = 0
            for region in regions:
                selectionText = self.view.substr(region)
                self.view.erase(edit, region)
                self.view.insert(edit, region.begin(), self.parseText(selectionText, lines[i], i, len(lines)))
                i = i + 1
        else:
            region = regions[0]
            selectionText = self.view.substr(region)
            parsedTextArr = []
            for i in range(0, len(lines)):
                parsedTextArr.append(self.parseText(selectionText, lines[i], i, len(lines)))
            self.view.erase(edit, region)
            self.view.insert(edit, region.begin(), '\n'.join(parsedTextArr))

class ExecParserDuplicateCommand(sublime_plugin.TextCommand):

    def parseText(self, selectionText, clipboardText, lineIndex, numOfLines):
        parserType = 'duplicate'
        output = selectionText
        localDict = locals()
        exec(ExecParserCore.duplicateCommandCache, None, localDict)

        return localDict['output']

    def run(self, edit):
        clipboardText = sublime.get_clipboard()
        regions = self.view.sel()

        i = len(regions) - 1
        # using backward looping to ensure the infinite stack with regions.add()
        while i > -1:
            region = regions[i]
            if region.empty():
                line = self.view.line(region)
                lineStr = self.view.substr(line)
                matchObj = re.search('\S', lineStr)
                if matchObj:
                    self.view.insert(edit, line.end(), '\n' + lineStr[0:matchObj.start()] + self.parseText(lineStr[matchObj.start():], clipboardText, 0, 1))
                else:
                    self.view.insert(edit, line.end(), '\n' + lineStr)
            else:
                text = self.view.substr(region)
                lines = text.splitlines()
                parsedTextArr = []
                for j in range(0, len(lines)):
                    parsedTextArr.append(self.parseText(lines[j], clipboardText, j, len(lines)))
                parsedText = '\n'.join(parsedTextArr)
                self.view.insert(edit, region.end(), parsedText)
                newRegion = sublime.Region(region.end(), region.end() + len(parsedText))
                regions.subtract(region)
                regions.add(newRegion)
            i = i - 1


def plugin_init():

    global FOLDERS
    global USER_PLUGIN_DIRECTORY
    global USER_COMMANDS_DIRECTORY
    global USER_COMMANDS_JSON_FILE_PATH
    global USER_COMMAND_TEMPLATE_FILE_PATH

    FOLDERS['user'] = os.path.join(sublime.packages_path(), 'User', PROJECT_NAME)
    FOLDERS['default'] = os.path.join(sublime.packages_path(), PROJECT_NAME)
    USER_PLUGIN_DIRECTORY = FOLDERS['user']
    USER_COMMANDS_DIRECTORY = os.path.join(USER_PLUGIN_DIRECTORY, 'commands')
    USER_COMMANDS_JSON_FILE_PATH = os.path.join(USER_PLUGIN_DIRECTORY, COMMANDS_JSON_FILENAME)
    USER_COMMAND_TEMPLATE_FILE_PATH = os.path.join(FOLDERS['default'], 'user-command-template.py')
    ExecParserCore.init()

sublime.set_timeout(plugin_init, 500)
