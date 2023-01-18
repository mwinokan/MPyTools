#!/usr/bin/env python3

import time
import mwin
# import os
import subprocess
import re

window = mwin.Window()

#re.sub(r'\[.*?m', "", sq_buff)

# print(sq_list)

window.activate_alternate()

try:
	while True:
		
		window.write_command("sq.sh")

		window.draw()
		time.sleep(0.2)
except KeyboardInterrupt:
	pass

window.deactivate_alternate()

# print(window._debug_strbuff)
