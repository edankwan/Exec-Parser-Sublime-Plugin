# Sublime Text Plugin - Exec Parser #

Exec Parser is a sublime plugin that allow users to add custom python parser for paste command and duplicate line command.

## Installation ##
- **Manually**: Clone the repo into your packages folder (in Sublime: Preferences > Browse Packages...) and then rename the folder into "Exec Parser".

- **Package Control**: Coming soon.

## Usage ##

### Plugin Command ###

- **Exec Parser: Parse & Paste** *(Ctrl+Shift+v)* - To parse the string in the clipboard and paste it to the selected regions.

- **Exec Parser: Parse & Duplicate** *(Ctrl+Shift+c)* - To parse the string in the selected regions and duplicate it right behind it.

- **Exec Parser: Set Parser** *(Ctrl+Shift+x)* - To call the selection box to choose the command you want to apply. After you choose the command, you will be able to apply this command to the parser commands you want. You can apply it to:
	- All - to apply the selected command to **"Parse & Paste Command"** and **"Parse & Duplicate Command"**
	- Paste only - to apply the selected command to **"Parse & Paste Command"**
	- Duplicate only - to apply the selected command to **"Parse & Duplicate Command"**

- **Exec Parser: User Command Options** *(Ctrl+Shift+z)* - To call the option panel for user custom command:
	- **Reinitialize commands** - After you added/edited any user commands or edited the commmands.json file, you will need to run this command to reinitialize the plugin. Otherwise, the command list in the **Set Parser** panel won't be updated.
	- **Edit commands.json** - It is a json file which stores all of the user commands, it is physically located at [Packages]/User/Exec Parser.
	- **Add new command** - Add a new user command. You will be asked to enter the filename first. Be aware that you don't need to put any extension after the filename. After you entered the filename and if the file doesn't not exist, it will open the commands.json and the command file. You are good to go adding your codes in it. But don't forget to run the **Reinitialize commands** after you updated it. :-)
	- **Edit command** - It will show the list of all user commands and you can choose the one you want to edit. But don't forget to run the **Reinitialize commands** after you updated it. :-)
	- **Delete commands** - It will show the list of all user commands and you can choose the one you want to delete.

### Use the commands ###
First of all, you need to choose the command you want to use for your parser commands(paste/duplicate). Let's say you want to use the command to convert words in your clipboard into **camelCase**, you can hit *(Ctrl+Shift+x)* to open the **Exec Parser: Set Parser** panel to choose **camelCase**, then apply choose **Paste only**. Then Every time you hit *(Ctrl+Shift+v)* to trigger the **Exec Parser: Parse & Paste** parser command, the output will be in camelCased. Same thing for **Exec Parser: Parse & Duplicate**.

The command you chose will be stored until you change it again or restarting Sublime Text. There is a way to save the command you choose even after you restart the Sublime Text. You can do it by simply adding this to the **User Setting**:

	"update_default_command_on_change" : false

By default, the commands for **Exec Parser: Parse & Paste** and **Exec Parser: Parse & Duplicate** are both **"none"**. Which means it does nothing. I reason I did it this way is that, you can change the hotkey of this plugin to replace the native **paste** and **duplicate line** functions in sublime. 

### Create your own commands ###
Let's say you want to create a command to add a dollar sign before the numbers. Hit *(Ctrl+Shift+z)* to open the **Exec Parser: User Command Options** panel, choose **"Add new command"**. Type the command filename(without any extension) like "dollarize", then hit enter. Then it will open 2 files:

- **commands.json** - A json file which stores all of the user's commands descriptions. You can change the name and description in this file if you want to.
- **[filename].py***(In this case, dollarize.py)* - Where you put your script.

Type the following python script in the **dollarize.py**

	output = re.sub(r'(?<![\$\d])(\d+)', r'$\1', output)

Save it and hit *(Ctrl+Shift+z)* again to open the **Exec Parser: User Command Options** panel. select the **Reinitialize commands** to let the plugin to update the scripts. Now you are good to go to test it out.

The script file you are editing is simply executed by a **exec()** command in python. Which means you can get advantage of it and make your if/else statements, loops and functions. Here is another example:

    def upperAndLower(char, isUpper):
        if isUpper:
            return char.upper()
        else:
            return char.lower()
    arr = list(output)
    for i in range(0, len(arr)):
        arr[i] = upperAndLower(arr[i], i & 1)
    output = ''.join(arr)

	<< My name is Edan.
	>> mY NaMe iS EdAn.

***Easy enough!***

### Exposed variables####
We expose the following variables for you to build your commands:

- **output***(string)* the text in the **single line** that the parser commands are applying to. If the user select multiply lines, we splitted the lines before passing to the output variable. So in any case, you are only dealing with one line. I know it can be a deal breaker if you want to do multiline parsing. The reason I did this is to try to behave what the native function does. We may expose more content in the later build but right now it is how it works.
- **parserType***(string)* - It shows what parser command the user is using. It can be either **"paste"** or **"duplicate"**.
- **selectionText***(string)* - The current selected text. If the user is using multi-selection, every selection is using its own instance. This variable can be multiline.
- **clipboardText***(string)* - The clipboard content. This variable can be multiline.
- **lineIndex** - The index of the lines you are editing.
- **numOfLines** - The number of lines in the region.

### Exposed modules ###
- **shutil**
- **math**
- **datetime**
- **json**
- **os**
- **re**



## SETTING ##
	/* The default parser commands */
	"paste_command_id" : "none",
	"duplicate_command_id" : "none",
	
	/* To save the command you set as default */
	"update_default_command_on_change" : false,

## TODO ##
- Add more default exec commands
- Add package control
- Reduce the times of user's **Reinitialize commands** calls during command testing

## GOAL ##
The goal of this plugin is completely replace the native paste command and duplicate line command. I coded the way that if you are not using any parser command, it behaves just like the native command.

## CONTRIBUTION ##
It is my first time to try Python and I am not a good coder in general. So if you noticed there are something wrong with it, please make a pull request. If you have a cool command that you want to share, make a pull request. This plugin will get more and more powerful with your contribution :)

## ABOUT ME ##
My name is Edan Kwan and I am a front-end web developer. I know nothing about Python and I am bad at programming. I started building it because I always find it annoying to copy the dash-cased html attributes to camelCased javascript as variables name. I am pretty sure you guys can write it better than me. So, make pull requests to help it grow! :)



