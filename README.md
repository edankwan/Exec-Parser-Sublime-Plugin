# Sublime Text Plugin - Exec Parser #

Exec Parser is a sublime plugin that allow users to add custom python parser for paste command and duplicate line command.

## Usage ##

### Plugin Command ###

- **Exec Parser: Parse & Paste** *(Ctrl+Shift+v)* - To parse the string in the clipboard and paste it to the selected regions.

- **Exec Parser: Parse & Duplicate** *(Ctrl+Shift+v)* - To parse the string in the selected regions and duplicate it right behind it.

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

## ABOUT ME ##
My name is Edan Kwan and I am a front-end web developer. I know nothing about Python. I started building it because I always find it annoying to copy the dash-cased html attributes to camelCased javascript as variables name. I am pretty sure you guys can write it better than me. So, make pull requests to update the plugin or to share your cool commands to help it grow! :)
****