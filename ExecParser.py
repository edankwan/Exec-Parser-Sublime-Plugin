import sublime
import sublime_plugin
import json
import os
import re

SETTING_FILENAME = 'ExecParser.sublime-settings'
COMMAND_PATH_PREFIX = {
    'user' : os.path.join(sublime.packages_path(), 'User', 'Exec Parser', 'commands'),
    'default' : os.path.join(sublime.packages_path(), 'Exec Parser', 'commands')
}
COMMAND_LIST = {
    'user' : os.path.join(sublime.packages_path(), 'User', 'Exec Parser', 'commands.json'),
    'default' : os.path.join(sublime.packages_path(), 'Exec Parser', 'commands.json')
}
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

    def readCommandJSON(cls, directory):
        try:
            f = open(COMMAND_LIST[directory], 'r')
        except(IOError), e:
            return {}
        else:
            try:
                commands = json.loads(f.read())
            except(ValueError), e:
                sublime.error_message('"' + directory + '" commands is not a valid json file.')
                return {}
            else:
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
        tmpList.sort(lambda x, y: cmp(x[0].lower(),y[0].lower()))
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
        except(KeyError), e:
            sublime.error_message('Command "' + commandId + '" no longer exist')
            return ''
        else:
            filename = os.path.join(COMMAND_PATH_PREFIX[command['directory']], command['filename'] + '.py')
            try:
                f = open(filename, 'r')
            except(IOError), e:
                sublime.error_message('Exer Parser plugin error: File "' + filename + '" not found.')
                return ''
            else:
                return f.read()

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

    init = classmethod(init)
    readCommandJSON = classmethod(readCommandJSON)
    createListItem = classmethod(createListItem)
    updateViewPanelList = classmethod(updateViewPanelList)
    setRecentCommand = classmethod(setRecentCommand)
    updateCommandList = classmethod(updateCommandList)
    getCommandData = classmethod(getCommandData)
    updatePasteCommand = classmethod(updatePasteCommand)
    updateDuplicateCommand = classmethod(updateDuplicateCommand)
    saveSetting = classmethod(saveSetting)

ExecParserCore.init()

class ExecParserSetCommand(sublime_plugin.TextCommand):

    commandId = ''
    applyToPanelList = [
        ['All', 'Apply the selected command to all parsers'],
        ['Paste only', 'Only apply the selected command to paste parser'],
        ['Duplicate only', 'Only apply the selected command to duplicate parser']
    ]

    def run(self, edit):
        self.view.window().show_quick_panel(ExecParserCore.viewPanelList, self.onCommandUpdate)

    def onCommandUpdate(self, index):
        self.commandId = ExecParserCore.viewPanelListIndexes[index]
        self.view.window().show_quick_panel(self.applyToPanelList, self.onApplyToUpdate)

    def onApplyToUpdate(self, index):
        if (index == 0) or (index == 1):
            ExecParserCore.updatePasteCommand(self.commandId)
        if (index == 0) or (index == 2):
            ExecParserCore.updateDuplicateCommand(self.commandId)

class ExecParserPasteCommand(sublime_plugin.TextCommand):

    def parseText(self, selectionText, clipboardText):
        parserType = 'paste'
        output = clipboardText
        exec(ExecParserCore.pasteCommandCache)
        return output

    def run(self, edit):
        clipboardText = sublime.get_clipboard()
        lines = clipboardText.splitlines()
        regions = self.view.sel()

        if (len(regions) > 1) and (len(regions) == len(lines)):
            i = 0
            for region in regions:
                selectionText = self.view.substr(region)
                self.view.erase(edit, region)
                self.view.insert(edit, region.begin(), self.parseText(selectionText, lines[i]))
                i = i + 1
        else:
            region = regions[0]
            selectionText = self.view.substr(region)
            parsedTextArr = []
            for i in range(0, len(lines)):
                parsedTextArr.append(self.parseText(selectionText, lines[i]))
            self.view.erase(edit, region)
            self.view.insert(edit, region.begin(), '\n'.join(parsedTextArr))

class ExecParserDuplicateCommand(sublime_plugin.TextCommand):

    def parseText(self, selectionText, clipboardText):
        parserType = 'duplicate'
        output = selectionText
        exec(ExecParserCore.duplicateCommandCache)
        return output

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
                    self.view.insert(edit, line.end(), '\n' + lineStr[0:matchObj.start()] + self.parseText(lineStr[matchObj.start():], clipboardText))
                else:
                    self.view.insert(edit, line.end(), '\n' + lineStr)
            else:
                text = self.view.substr(region)
                lines = text.splitlines()
                parsedText = ''
                for j in range(0, len(lines)):
                    parsedText += '\n' + self.parseText(lines[j], clipboardText)
                self.view.insert(edit, region.end(), parsedText)
                newRegion = sublime.Region(region.end(), region.end() + len(parsedText))
                regions.subtract(region)
                regions.add(newRegion)
            i = i - 1