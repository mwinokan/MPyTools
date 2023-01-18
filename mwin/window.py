
import numpy as np
import os
import mout
import re
import mcol

class Window(object):
	
	"""Curses Style Terminal Window"""

	def __init__(self,border=True,show_exit_help=True):
		mout.debugOut("mwin.Window.__init__()")

		super(Window, self).__init__()
		self._width = os.get_terminal_size()[0]
		self._height = os.get_terminal_size()[1]
		self._buffer = np.empty((self._height,self._width),dtype=object)
		self._current_line = 0
		self._border = border
		self._fo = open('temp.log','wt')

		self.clear_buffer()

		if border:
			self._tpad = 1
			self._bpad = 1
			self._rpad = 1
			self._lpad = 2
			self.make_border()
		else:
			self._tpad = 0
			self._bpad = 0
			self._rpad = 0
			self._lpad = 0

		if show_exit_help:
			for i,char in enumerate('Press Ctrl+C to exit...'):
				if i == self._width-self._rpad:
					break
				self._buffer[self._height-self._bpad-1][i+self._lpad] = char
			self._bpad = 3

		mout.debugOut(f"#cols={self._width}")
		mout.debugOut(f"#rows={self._height}")

	def activate_alternate(self):
		os.system('tput smcup')

	def deactivate_alternate(self):
		os.system('tput rmcup')

	def clear(self):
		self.clear_buffer()
		if self._border:
			self.make_border()
		self._current_line = 0

	def clear_buffer(self):
		for i in range(self._width):
			for j in range(self._height):
				self._buffer[j][i] = " "

	def make_border(self):

		self._buffer[0][0] = '┏'
		self._buffer[0][-1] = '┓'
		self._buffer[-1][0] = '┗'
		self._buffer[-1][-1] = '┛'

		self._buffer[0][1:-1] = '━'
		self._buffer[-1][1:-1] = '━'

		for r in range(self._height):
			if r == 0:
				continue
			if r == self._height-1:
				continue
			self._buffer[r][0] = '┃'
			self._buffer[r][-1] = '┃'

	def draw(self):
		for i,row in enumerate(self._buffer):

			for char in row:

				if char.startswith('™'):
					char = char.replace('™033','\033')
					print(char,end='',flush=True)
				else:
					print(char,end='',flush=True)
				self._fo.write(char)

			# print(''.join(row),end='',flush=True)
			if i < self._height-1:
				print('')

	def sanitise_text(self,text,remove_escapes=False):

		buff = str(text)
		buff = buff.split(r'\n')

		sq_list = []
		for string in buff:
			this_str = string
			if remove_escapes:
				this_str = re.sub(r'\\.*?m', "", this_str)
				this_str = re.sub(r'\\', "", this_str)
			sq_list.append(this_str)

		sq_list[0] = sq_list[0].lstrip('b"')

		return sq_list

	def write_command(self,command):
		import subprocess

		buff = subprocess.check_output(command)

		buff_list = self.sanitise_text(buff,remove_escapes=False)

		self.clear()

		for line in buff_list[:-1]:
			self.write_line(line)

	def fancy_split(self,line):

		str_list = []

		escaped = False
		recently_ended = False

		for i,char in enumerate(line):

			if not escaped:

				if char == '\\':

					escaped = True
					str_list.append('™')

				elif recently_ended:
					str_list[-1] += char
					recently_ended = False

				else:
					str_list.append(char)

			else:

				if char == 'm':
					escaped = False
					recently_ended = True
				str_list[-1] += char

		str_list = [line.replace('x1b','033') for line in str_list]

		self._fo.write(str(str_list))

		return str_list

	def write_line(self,strbuff,force=False):
		
		if self._current_line >= self._height - self._bpad - 1:
			for i,char in enumerate('...'):
				if i == self._width-self._rpad:
					break
				self._buffer[self._height-self._bpad][i+self._lpad] = char

			return

		strbuff = self.fancy_split(strbuff)

		for i,char in enumerate(strbuff):
			if i+self._lpad == self._width-self._rpad-1:
				self._buffer[self._current_line+self._tpad][i+self._lpad] = "—"
				break
			self._buffer[self._current_line+self._tpad][i+self._lpad] = str(char)
		self._current_line += 1
