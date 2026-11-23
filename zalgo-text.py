import os,re
for c in re.sub(r'\n\s*','\n',re.sub('(?s)<!D.*?(?=<hg)|<[^>]*>','',re.sub('</[dfhlpt]','\n<',os.popen('curl -L unicode.org/versions/latest/core-spec/chapter-[1-24]').read()))):print(end=c+''.join(chr(768+b%112)for b in os.urandom(ord(c)%8)))
