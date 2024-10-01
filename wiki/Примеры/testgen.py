import sys

print('Convert',sys.argv[1],'to', sys.argv[2])
with open(sys.argv[1],'r',encoding='utf8') as f:
	data=f.read()
script = ['#!/bin/bash','rm test.log.txt']
n=0
for cmd in data.split('\n'):
	cmd = cmd.strip()
	if not cmd or cmd.startswith('#'):
		continue
	script.append('')
	script.append('echo "==========================="')
	script.append('echo "'+cmd+'" | tee -a test.log.txt')
	script.append('echo "==========================="')
	script.append(cmd+' 2>&1 | tee -a test.log.txt')
	script.append('echo -e "\\n\\n\\n\\n"')
	n+=1
with open(sys.argv[2],'w',encoding='utf8',newline='\n') as f:
	f.write('\n'.join(script))
print('Saved',n,'commands to',sys.argv[2])

