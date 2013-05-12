# Exec Parser #

A sublime plugin that allow users to add custom python paste command on the text.

## Usage ##
The default parser command is "none", so it does nothing and if you use the "Parse & Paste" command(Ctrl+shift+V), it just behaves like normal paste command.

To set the parser command, use "Set Parser" command(Ctrl+shift+X), and choose the parser command you want. For example, "camelCase". Then you are able to paste something with the "Parse & Paste" command(Ctrl+shift+V) to convert what it has in your clipboard into camelCase.

I designed it the way that it won't change the context in your clipboard and everytime you run the command, it parses it all over again. It will have a slightly performance issue but I find it better if the user doesn't want to change the context in the clipboard.

## TODO ##
- Add more default exec commands
- Add duplicate lines parser commands
- Add package control

## ABOUT ME ##
My name is Edan Kwan and I am a front-end web developer. I know nothing about Python. I started building it because I  always find it annoying to copy the dash-cased html attributes to camelCased javascript as variables name. I am pretty sure you guys can write it better than me. Please contribute and help it grow! :)
