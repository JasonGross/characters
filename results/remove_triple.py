#!/usr/bin/python
import os
import re
find = re.compile('(.*?_[0-9][0-9])[0-9](_[0-9-]+.+)')
for base, dirs, files in os.walk(os.getcwd()):
	print(base)
	for file_name in files:
		if find.match(file_name):
			if os.path.exists(os.path.join(base, ''.join(find.match(file_name).groups()))):
				print(file_name)
				os.remove(os.path.join(base, file_name))
		
