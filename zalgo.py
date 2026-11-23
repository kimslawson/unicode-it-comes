import re,os;from random import*
z=lambda t:''.join(c+''.join(map(chr,choices(range(768,880),k=ord(c)%8)))for c in t)
for i in range(1,25):print(z(re.sub('<[^>]+>',' ',os.popen(f"curl -L http://unicode.org/versions/latest/core-spec/chapter-{i}").read())))
