import curses
import curses.panel

LEFT_CLICK = curses.BUTTON1_CLICKED
LEFT_DOUBLE = curses.BUTTON1_DOUBLE_CLICKED
RIGHT_CLICK = curses.BUTTON3_CLICKED
RIGHT_DOUBLE = curses.BUTTON3_DOUBLE_CLICKED
SCROLL_UP = 2097152
SCROLL_DOWN = 65536

""" 

To-Do's 

* Context Menu's

"""

class CursesApp():
	"""A CLI-App Class based on pycurses"""
	def __init__(self,debug=False,nodelay=False,logging=False,force_draw=False):

		if logging:
			self._flog = open('_curses.log','w')
		else:
			self._flog = None

		self.max_padline = 0

		self.debug = debug

		self.texts = []
		self.buttons = []
		self.drawables = []
		self.mouse = None

		self.message = None
		self._selection = None
		
		self._force_draw = force_draw

		self._scr = curses.initscr()
		self.scr_h, self.scr_w = self._scr.getmaxyx()

		if self.scr_w < 60:
			self.close()
			import mout
			mout.errorOut("Terminal is not wide enough!",fatal=True)
	
		self.scroll_line = 0

		if nodelay:
			self._scr.nodelay(1)

		self.pad_h = 4000
		self.pad_w = 150

		self._pad = curses.newpad(self.pad_h,self.pad_w)
		# self._pad = curses.newpad(4000,self.w)

		self.padclear()

		# self.contextwin = None
		self.context_items = []

		curses.noecho()
		curses.cbreak()
		self.scr.keypad(True)
		curses.curs_set(0)
		curses.mousemask(-1)

		self.define_colors()

	def log(self,text):
		self.message = text
		if self._flog:
			self._flog.write(text)
			self._flog.write('\n')

	def context_menu(self,line,col,items):
		self.log('Creating context window')
		self.context_items = items

	def hide_context_menu(self):
		self.message = 'Closing context menu'
		self.context_items = []

	def define_colors(self):
		curses.start_color()
		self.NORMAL = 0

		# NORMAL
		curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK) 
		curses.init_pair(3,curses.COLOR_GREEN,curses.COLOR_BLACK) 
		curses.init_pair(4,curses.COLOR_YELLOW,curses.COLOR_BLACK) 
		curses.init_pair(5,curses.COLOR_BLUE,curses.COLOR_BLACK) 
		curses.init_pair(6,curses.COLOR_MAGENTA,curses.COLOR_BLACK) 
		curses.init_pair(7,curses.COLOR_CYAN,curses.COLOR_BLACK) 
		curses.init_pair(8,curses.COLOR_WHITE,curses.COLOR_BLACK) 
		self.RED = curses.color_pair(2)
		self.GREEN = curses.color_pair(3)
		self.YELLOW = curses.color_pair(4)
		self.BLUE = curses.color_pair(5)
		self.MAGENTA = curses.color_pair(6)
		self.CYAN = curses.color_pair(7)
		self.WHITE = curses.color_pair(8)

		# INVERSE
		curses.init_pair(12,curses.COLOR_BLACK,curses.COLOR_RED) 
		curses.init_pair(13,curses.COLOR_BLACK,curses.COLOR_GREEN) 
		curses.init_pair(14,curses.COLOR_BLACK,curses.COLOR_YELLOW) 
		curses.init_pair(15,curses.COLOR_BLACK,curses.COLOR_BLUE) 
		curses.init_pair(16,curses.COLOR_BLACK,curses.COLOR_MAGENTA) 
		curses.init_pair(17,curses.COLOR_BLACK,curses.COLOR_CYAN) 
		curses.init_pair(18,curses.COLOR_BLACK,curses.COLOR_WHITE) 
		self.BLACK_INV = curses.color_pair(11)
		self.RED_INV = curses.color_pair(12)
		self.GREEN_INV = curses.color_pair(13)
		self.YELLOW_INV = curses.color_pair(14)
		self.BLUE_INV = curses.color_pair(15)
		self.MAGENTA_INV = curses.color_pair(16)
		self.CYAN_INV = curses.color_pair(17)
		self.WHITE_INV = curses.color_pair(18)

		# INVISIBLE
		curses.init_pair(99,curses.COLOR_WHITE,curses.COLOR_WHITE)
		self.WHITE_WHITE = curses.color_pair(99)

	def add_button(self,button):
		self.buttons.append(button)
		self.drawables.append(button)

	def add_text(self,text):
		self.texts.append(text)
		self.drawables.append(text)

	def deselect_buttons(self):
		for button in self.buttons:
			button.selected = False
	
	def clear_drawables(self):
		self.buttons = []
		self.texts = []
		self.drawables = []

	def draw_objects(self):

		for obj in self.drawables:
			obj.draw(self)

		if self.context_items:
			for obj in self.context_items:
				obj.draw(self)

	def get_dims(self):
		self.h, self.w = self.pad.getmaxyx()

	def draw(self):
		redraw = self.process_keypress()	
		if self._force_draw:
			redraw = True	
		self.drawcore()
		return redraw

	def firstdraw(self):
		self.get_dims()
		self.drawcore()

	def drawcore(self):
		self.padclear()
		self.scr.clear()
		self.max_padline = 0
		self.draw_objects()
		self.draw_scrollbar()
		if self._selection:
			self.highlight_selection()
		self.message = self._selection
		self.scr.refresh()
		if self.debug: 
			self.draw_debug()
			self.pad.refresh(self.scroll_line,0,0,0,self.scr_h-4,self.scr_w-3)
		else:
			self.pad.refresh(self.scroll_line,0,0,0,self.scr_h-1,self.scr_w-3)
		
	def draw_scrollbar(self):

		if self.max_padline > self.scr_h:

			screen_height = self.scr_h
			bar_length = max(5,(screen_height*screen_height)//(self.max_padline+5))
			scrollable_distance = 5+self.max_padline-screen_height			
			bar_position = ((screen_height-bar_length)*self.scroll_line)//(scrollable_distance)

			self.message = f'bar_length={bar_length}, bar_position={bar_position}'

			for i in range(self.scr_h-1):
				if i >= bar_position and i <= bar_position + bar_length:
					self.scr.attron(curses.color_pair(99))
					self.scr.addch(i,self.scr_w-1,'|')
					self.scr.attroff(curses.color_pair(99))

	def draw_debug(self):
		self.scr.addstr(self.scr_h-3,0,f'PAD: scroll_line={self.scroll_line}, max_padline={self.max_padline}')
		self.scr.clrtoeol()
		self.scr.addstr(self.scr_h-2,0,f'LOG: {self.message}')
		self.scr.clrtoeol()
		self.scr.addstr(self.scr_h-1,0,f'MOUSE: {self.mouse}')
		self.scr.clrtoeol()

	def process_keypress(self):
		self.key = self.scr.getch()

		if self.key == curses.KEY_MOUSE:
			return self.process_mouse()
		elif self.key == curses.KEY_DOWN and self.allow_scroll_decrease:
			self.scroll_line -= 1 
		elif self.key == curses.KEY_UP and self.allow_scroll_increase:
			self.scroll_line += 1 

		return False

	@property
	def clickables(self):
		clickables = []
		if self.context_items:
			clickables += [b for b in self.context_items if isinstance(b,Button)]
		clickables += self.buttons
		return clickables

	def process_mouse(self):
		self.mouse = curses.getmouse()
		x = self.mouse[1]
		y = self.mouse[2]
		state = self.mouse[4]

		if state & SCROLL_UP and self.allow_scroll_decrease:
			self.scroll_line -= 1 
		elif state & SCROLL_DOWN and self.allow_scroll_increase:
			self.scroll_line += 1 
		elif state & LEFT_CLICK:
			self._selection = None
			for button in self.clickables:
				if button.is_hit(x,y+self.scroll_line):
					prestate = button.active
					self._last_pressed = button
					button.toggle()
					self.log(f'Toggling button {button.name} {prestate} --> {button.active}')
					return True
		elif state & curses.BUTTON1_PRESSED:
			self.message = "Drag Started"
			self._mouse_drag_start = (x,y)
			self._selection = None
			return False
		elif state & curses.BUTTON1_RELEASED:
			self._mouse_drag_finish = (x,y)
			select = self.get_selection(self._mouse_drag_start,self._mouse_drag_finish)
			self.message = f"Drag Finished. {self._mouse_drag_start,self._mouse_drag_finish}"

			# add to clipboard (MacOS)
			import subprocess 
			subprocess.run("pbcopy", text=True, input=select)
			return False
		else:
			self._selection = None
			return False
		return False

	@property
	def allow_scroll_increase(self):
		if self.scr_h > self.max_padline:
			return False
		elif self.scroll_line + self.scr_h > self.max_padline + 5:
			return False
		return True
	
	@property
	def allow_scroll_decrease(self):
		return self.scroll_line > 0

	@property
	def scr(self):
		return self._scr

	@property
	def pad(self):
		return self._pad

	def get_selection(self,v1,v2):

		v1x = v1[0]
		v1y = v1[1]
		v2x = v2[0]
		v2y = v2[1]

		line_min = min(v1y, v2y)
		line_max = max(v1y, v2y)
		col_min = min(v1x, v2x)
		col_max = max(v1x, v2x)

		str_buffer = ""

		for y in range(line_min,line_max+1):
			for x in range(col_min,col_max+1):
				char = self.padget(y,x)
				str_buffer += char
			str_buffer += "\n"

		self._selection = [v1x,v1y,v2x,v2y]

		return str_buffer

	def padclear(self):
		self.pad.clear()
		self._pad_data = {}

	def padlog(self,line,col,char):
		if line not in self._pad_data.keys():
			self._pad_data[line] = {}
		self._pad_data[line][col] = char

	def padget(self,line,col):
		if line not in self._pad_data.keys():
			return ' '

		if col not in self._pad_data[line].keys():
			return ' '

		return self._pad_data[line][col]

	def highlight_selection(self):

		v1x,v1y,v2x,v2y = self._selection

		line_min = min(v1y, v2y)
		line_max = max(v1y, v2y)
		col_min = min(v1x, v2x)
		col_max = max(v1x, v2x)

		for y in range(line_min,line_max+1):
			for x in range(col_min,col_max+1):
				self.highlight(y, x)

	def highlight(self,line,col,char=None,color_pair=None):
		color_pair = color_pair or self.MAGENTA_INV
		color_pair = self.MAGENTA_INV
		char = char or self.padget(line, col)
		self.message = f'highlight {line} {col} {char}'
		self.pad.attron(color_pair)
		self.pad.addch(line, col, char)
		self.pad.attroff(color_pair)

	def padwrite(self,line,col,text,color_pair=None,bold=False,underline=False):

		for i,char in enumerate(text):
			self.padlog(line, col+i, char)

		attribute = None

		if bold:
			bold = curses.A_BOLD
		else:
			bold = 0

		if underline:
			underline = curses.A_UNDERLINE
		else:
			underline = 0

		# if bold:
		# 	attribute = curses.A_BOLD
		# 	# self.pad.attron(curses.A_BOLD)
		
		# if underline:
		# 	if attribute:
		# 		attribute = attribute | curses.A_UNDERLINE
		# 	else:
		# 		attribute = curses.A_UNDERLINE
		# 	# self.pad.attron(curses.A_UNDERLINE)

		# if color_pair:
		# 	if attribute:
		# 		attribute = attribute | color_pair
		# 	else:
		# 		attribute = color_pair
		# 	# self.pad.attron(color_pair)

		attribute = bold | underline | color_pair

		if bold and color_pair:
			self.log(f'BOLD COLOUR')

		if attribute:
			self.pad.attron(attribute)
			self.log(f'{bold} {underline} {color_pair} {bold | underline | color_pair}')
			self.log(f'{bold:b} {underline:b} {color_pair:b} {attribute:b}')

		self.pad.addstr(line,col,text)

		if attribute:
			self.pad.attroff(attribute)

		# if bold:
		# 	self.pad.attroff(curses.A_BOLD)

		# if underline:
		# 	self.pad.attroff(curses.A_UNDERLINE)

		# if color_pair:
		# 	self.pad.attroff(color_pair)

		if line > self.max_padline:
			self.max_padline = line

	def write(self,line,col,text):
		self.scr.addstr(line,col,str(text))
		return line, col+len(text)

	def close(self):
		self.scr.keypad(False)
		curses.echo()
		curses.nocbreak()
		curses.curs_set(1)
		curses.endwin()
		if self._flog:
			self._flog.close()

class Text():

	def __init__(self,name,line,col,color_pair=None,bold=False,underline=False):
		self.name = name
		self.line = line
		self.col = col
		self.activename = None
		self.color_pair = color_pair or curses.color_pair(0)
		self.bold = bold
		self.underline = underline

	@property
	def endcol(self):
		return self.col + self.length

	@property
	def length(self):
		if self.activename:
			if self.active:
				return len(self.activename)
			else:
				return len(self.name)
		else:
			return len(self.name)

	def draw(self,app):
		app.padwrite(self.line,self.col,self.name,self.color_pair,bold=self.bold,underline=self.underline)

class Button(Text):
	def __init__(self,app,name,line,col,active=False,enabler=None,disabler=None,target=None,padding=1,activename=None,color_inactive=None,color_active=None):
		super(Button, self).__init__(name,line,col)

		self.app = app
		self.active = active
		self.color_inactive = color_inactive or self.app.WHITE_INV
		self.color_active = color_active or self.app.YELLOW_INV

		self.activename = activename

		self.enabler = enabler
		self.disabler = disabler
		self.target = target

	@property
	def text(self):
		if self.activename:
			if self.active:
				return self.activename
			else:
				return self.name
		else:
			return self.name
	
	def draw(self,app):
		if self.active:
			app.padwrite(self.line,self.col,self.text,self.color_active,bold=False)
		else:
			app.padwrite(self.line,self.col,self.text,self.color_inactive,bold=False)

	def is_hit(self,x,y):
		if y != self.line: return False
		if x >= self.col and x < self.col + self.length:
			return True
		return False

	def toggle(self):
		if self.active:
			self.app.log(f"Disabling {self.name}")
			self.disable()
		else:
			self.app.log(f"Enabling {self.name}")
			self.enable()

	def enable(self):
		if self.enabler:
			self.app.log(f"Running Button({self.name}).enabler({self.target})")
			self.enabler(self.target)
		else:
			self.active = True

	def disable(self):
		if self.disabler:
			self.app.log(f"Running Button({self.name}).disabler({self.target})")
			self.disabler(self.target)
		else:
			self.active = False
