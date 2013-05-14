def _capitalize(matchObj):
    return matchObj.expand(r'\1').upper()

def _lowerFirst(matchObj):
    return matchObj.expand(r'\1') + matchObj.expand(r'\2').lower() + matchObj.expand(r'\3')

_tmp = re.sub(r'[^\w\n\r]+', '_', output)
_tmp = re.sub(r'_+', '_', _tmp)
_tmp = re.sub(r'_([a-z])',  _capitalize, _tmp)
output = re.sub(r'^( *).*', r'\1', output) + re.sub(r'^[^_\w\n\r]*(_*).*', r'\1', output) + re.sub(r'^([^a-zA-Z]*)([a-zA-Z])(.*)',  _lowerFirst, _tmp.strip('_'))