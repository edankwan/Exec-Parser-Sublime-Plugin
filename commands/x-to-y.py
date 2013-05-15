SWITCH_PATTERNS = [
    ['add', 'remove'],
    ['remove', 'add'],
    ['x', 'y'],
    ['y', 'x'],
    ['width', 'height'],
    ['height', 'width'],
    ['left', 'right'],
    ['right', 'left'],
    ['top', 'bottom'],
    ['bottom', 'top']
]

def getFirstMatchIndex(text, pattern, fillChar):
    matchObj = re.search(r'[^A-Z](' + pattern.capitalize() + r')[^a-z]|[^A-Z](' + pattern.upper() + r')[^a-z]|[^a-z](' + pattern + r')[^a-z]', fillChar+text+' ')
    if matchObj:
        return matchObj.start(0)
    else:
        return -1

index = 0
foundLen = 0
patternIndex = -1
found = True
replaceList = []
fillChar = ' '
fullLen = len(output)
while found:
    found = False
    minIndex = fullLen
    tmp = output[index:]
    for i in range(0, len(SWITCH_PATTERNS)):
        foundIndex = getFirstMatchIndex(tmp, SWITCH_PATTERNS[i][0], fillChar)
        if(foundIndex > -1) and (foundIndex < minIndex):
            found = True
            patternIndex = i
            minIndex = foundIndex
    if not found:
        break
    print tmp
    foundLen = len(SWITCH_PATTERNS[patternIndex][0])
    replaceList.append([index + minIndex, patternIndex])
    index = index + minIndex + foundLen
    fillChar = output[index - 1: index]

tmp = ''
index = 0
for i in range(0, len(replaceList)):
    replaceItem = replaceList[i]
    replaceIndex = replaceItem[0]
    pattern = SWITCH_PATTERNS[replaceItem[1]]
    tmp = tmp + output[index: replaceIndex]
    if output[replaceIndex:replaceIndex+1].isupper():
        if (replaceIndex < fullLen-1) and (output[replaceIndex+1:replaceIndex+2].isupper()):
            tmp = tmp + pattern[1].upper()
        else:
            tmp = tmp + pattern[1].capitalize()
    else:
        tmp = tmp + pattern[1]
    index = replaceIndex + len(pattern[0])
output = tmp + output[index:]