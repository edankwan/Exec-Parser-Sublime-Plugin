_tmp = re.sub(r'([a-z])([A-Z])', r'\1 \2', output)
_tmp = re.sub(r'[^\w\n\r]+', '_', _tmp.lower())
_tmp = re.sub(r'_+', '_', _tmp)
output = re.sub(r'^( *).*', r'\1', output) + re.sub(r'^[^_\w\n\r]*(_*).*', r'\1', output) + _tmp.strip('_').replace('_', '-')