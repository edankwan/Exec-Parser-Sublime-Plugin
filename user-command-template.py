#
# Rememeber to update your commands.json and reinitialize the plugin after you made the changes
#
# Variables:
#  - output(string): The text you are going to parse and alter. This value is single line based.
#  - parserType(string): 'paste' or 'duplicate', depends on the parser commands
#  - selectionText(string): The selected text
#  - clipboardText(string): The text in the user's clipboard
#
# Example 1 - Add dollar sign before the number:
# output = re.sub(r'(?<![\$\d])(\d+)', r'$\1', output)
#
# << I have 999
# >> I have $999
#
# Example 2 - Upper and lower case for each character using function call
#
# def upperAndLower(char, isUpper):
#     if isUpper:
#         return char.upper()
#     else:
#         return char.lower()
# arr = list(output)
# for i in range(0, len(arr)):
#     arr[i] = upperAndLower(arr[i], i & 1)
# output = ''.join(arr)
#
# << My name is Edan.
# >> mY NaMe iS EdAn.
#