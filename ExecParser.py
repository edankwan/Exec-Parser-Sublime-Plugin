import sublime
import sublime_plugin
import json
import re

settings = ''
panelList = []
commandList = []
execCommand = ''

def updateList():
    global settings
    global panelList
    global commandList
    global execCommand

    settings = sublime.load_settings('ExecParser.sublime-settings')
    panelList = []
    commandList = []

    commands = settings.get('commands')
    currentCommand = settings.get('current_command')
    for command in commands:
        panelList.append([command.get('name'), command.get('description')])

        execList = command.get('exec_lines')
        execText = '\n'.join(execList)
        commandList.append(execText)
        if currentCommand == command.get('id'):
            execCommand = execText



class ExecParserSetCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.window().show_quick_panel(panelList, self.onUpdate)

    def onUpdate(self, index):
        updateList()
        execCommand = commandList[index]
        settings.set('current_command', settings.get('commands')[index].get('id'))
        sublime.save_settings('ExecParser.sublime-settings')

        

class ExecParserPasteCommand(sublime_plugin.TextCommand):

    def parse(self, edit, region, text):
        self.view.erase(edit, region)
        exec(execCommand)
        self.view.insert(edit, region.begin(), text)

    def run(self, edit):
        clipText = sublime.get_clipboard()
        regions = self.view.sel()

        if len(regions) > 1:
            clipLines = clipText.split('\n')
            if len(regions) == len(clipLines):
                i = 0
                for region in regions:
                    self.parse(edit, region, clipLines[i])
                    i = i + 1
            else:
                for region in regions:
                    self.parse(edit, region, clipText)
        else:
            self.parse(edit, regions[0], clipText)




class ExecParserDuplicateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print 'TODO add exec parse for duplicate lines'



updateList()
