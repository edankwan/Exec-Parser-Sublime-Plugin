output = re.sub(r'(\s*)(\S+)(\s*=\s*)([^;\s]+)(.*$)', r'\1\4\3\2\5', output)