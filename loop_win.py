#!/usr/bin/env python3

import sys
import mout
import subprocess
import time
import curses
from mwin.curses import CursesApp, Button, Text

def print_output(string):
	for line in string.split('\n'):
		print(line)

def run_process(command):

	try:
		process = subprocess.run(command, capture_output=True,text=True)
	except FileNotFoundError:
		mout.errorOut(f"Command/file '{command[0]}' could not be found",fatal=True)

	if process.returncode != 0:
		mout.errorOut(f"Command returned exit code {process.returncode}",fatal=False)

	if len(process.stderr) > 0:
		mout.warningOut(f"Non-zero STDERR output:")
		print_output(process.stderr)

	if len(process.stdout) > 0:
		print_output(process.stdout)

class LoopWindow(CursesApp):

	def __init__(self,command,sleep=5.0):
		super(LoopWindow, self).__init__(debug=False,nodelay=True)

		self.command = command

		try:

			start_time = time.time()
			self.draw_buffer()
			self.firstdraw()

			while True:

				redraw = self.draw()

				delta_time = time.time() - start_time
				if delta_time > sleep:
					start_time = time.time()
					self.clear_drawables()
					self.draw_buffer()
					redraw = True

				if redraw:
					self.drawcore()

		except KeyboardInterrupt:
			pass

		self.close()

	def split_by_escapes(self,line,string):

		array = []

		col = 0

		for substring in string.split("\u001b"):
		# for substring in string.split("m"):

			fmt_str = ''

			last = 0
			for i,char in enumerate(substring):
				if char == 'm':
					last = i+1
					break
				elif char == '[':
					continue
				fmt_str += char

			content = substring[last:]

			if not fmt_str:
				# array.append(f'#{content}')
				text = Text(content,line,col)
				self.add_text(text)
			else:
				fmt_codes = fmt_str.split(';')
				# array.append(f'@{fmt_codes}#{content}')
				
				bold=False
				underline=False

				if fmt_codes[0] == 0 or len(fmt_codes) == 1 and fmt_codes[0] == '0':
					text = Text(content,line,col)
					self.add_text(text)
					# continue

				else:

					if '1' in fmt_codes:
						bold = True
						fmt_codes = [f for f in fmt_codes if not '1']

					if '4' in fmt_codes:
						underline = True
						fmt_codes = [f for f in fmt_codes if not '4']

					color_pair = None
					
					if fmt_codes and fmt_codes[0] == '38' and fmt_codes[1] == '5':
						
						color_id256=fmt_codes[2]

						if color_id256 == '27':
							color_pair = self.GREEN
						elif color_id256 == '11':
							color_pair = self.YELLOW
						elif color_id256 == '154':
							color_pair = self.GREEN
						else:
							content = f'{"~".join(fmt_codes)}{content}'
						
						fmt_codes = []

					if fmt_codes:

						if '31' in fmt_codes:
							color_pair=self.RED
						elif '32' in fmt_codes:
							color_pair=self.GREEN
						elif '33' in fmt_codes:
							color_pair=self.YELLOW
						elif '34' in fmt_codes:
							color_pair=self.BLUE
						elif '35' in fmt_codes:
							color_pair=self.MAGENTA
						elif '36' in fmt_codes:
							color_pair=self.CYAN
						elif '37' in fmt_codes:
							color_pair=self.WHITE
						elif '95' in fmt_codes:
							color_pair=self.MAGENTA
						else:
							content = f'{"~".join(fmt_codes)}{content}'

					text = Text(content,line,col,color_pair=color_pair,bold=bold,underline=underline)
					self.add_text(text)
			
			col = text.endcol

		# return ''.join(array)

	def draw_buffer(self):

		# header
		text = Text(f'{" ".join(self.command)} @ {time.strftime("%H:%M:%S")}',0,0,color_pair=curses.A_STANDOUT)
		self.add_text(text)

		self.get_command_buffer()

		line = 2

		for string in self.line_buffer:
			string = self.split_by_escapes(line,string)
			# text = Text(string,line,0)
			# self.add_text(text)
			line += 1

	def get_command_buffer(self):

		try:
			process = subprocess.run(self.command, capture_output=True,text=True)
		except FileNotFoundError:
			mout.errorOut(f"Command/file '{self.command[0]}' could not be found",fatal=True)

		if len(process.stderr) > 0:
			mout.warningOut(f"Non-zero STDERR output:")
			print_output(process.stderr)

		self.line_buffer = process.stdout.split('\n')

def main():

	if len(sys.argv) < 2:
		mout.errorOut("Pass a command",fatal=True)

	command = sys.argv[1:]

	app = LoopWindow(command)

if __name__ == '__main__':
	main()
