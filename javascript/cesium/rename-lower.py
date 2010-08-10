#!/usr/bin/python
import os
for base, dirs, files in os.walk(os.getcwd()):
	for file_name in files:
		if file_name != file_name.lower():
			print(file_name)
			os.rename(os.path.join(base, file_name), os.path.join(base, file_name.lower()))
