import curses

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
	def __init__(self,debug=False):

		self.max_padline = 0

		self.debug = debug

		self.texts = []
		self.buttons = []
		self.drawables = []
		self.mouse = None

		self.message = None

		self._scr = curses.initscr()
		self.scr_h, self.scr_w = self._scr.getmaxyx()

		if self.scr_w < 60:
			self.close()
			import mout
			mout.errorOut("Terminal is not wide enough!",fatal=True)
	
		self.scroll_line = 0
		self._pad = curses.newpad(4000,150)
	# /	self._pad = curses.newpad(4000,self.w)

		curses.noecho()
		curses.cbreak()
		self.scr.keypad(True)
		curses.curs_set(0)
		curses.mousemask(-1)

		self.define_colors()

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
	
	# def clear_buttons(self):
	# 	self.buttons = []

	# def clear_texts(self):
	# 	self.texts = []

	def clear_drawables(self):
		self.buttons = []
		self.texts = []
		self.drawables = []

	def draw_objects(self):
		for obj in self.drawables:
			obj.draw(self)

	def get_dims(self):
		self.h, self.w = self.pad.getmaxyx()

	def draw(self):
		redraw = self.process_keypress()
		self.drawcore()
		return redraw

	def firstdraw(self):
		self.get_dims()
		self.drawcore()

	def drawcore(self):
		self.pad.clear()
		self.scr.clear()
		self.max_padline = 0
		self.draw_objects()
		self.draw_scrollbar()
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

	def process_mouse(self):
		self.mouse = curses.getmouse()
		x = self.mouse[1]
		y = self.mouse[2]
		state = self.mouse[4]

		if state & SCROLL_UP and self.allow_scroll_decrease:
			self.scroll_line -= 1 
		elif state & SCROLL_DOWN and self.allow_scroll_increase:
			self.scroll_line += 1 
		else:
			for button in self.buttons:
				if button.is_hit(x,y+self.scroll_line):
					if state & LEFT_CLICK:
						# self.deselect_buttons()
						button.toggle()
						return True
					# elif state & LEFT_DOUBLE:
					# 	button.action()
					# 	return True
					# elif state & RIGHT_CLICK:
					# 	button.action()
					# 	return True
		return False

	@property
	def allow_scroll_increase(self):
		# if self.scroll_line > 0:

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

	def padwrite(self,line,col,text,color_pair=None,bold=False):

		if bold:
			self.pad.attron(curses.A_BOLD)

		if color_pair:
			self.pad.attron(color_pair)

		self.pad.addstr(line,col,text)

		if bold:
			self.pad.attroff(curses.A_BOLD)

		if color_pair:
			self.pad.attroff(color_pair)

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

class Text():

	def __init__(self,name,line,col,color_pair=None,bold=False):
		self.name = name
		self.line = line
		self.col = col
		self.activename = None
		self.color_pair = color_pair or curses.color_pair(0)
		self.bold = bold

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
		app.padwrite(self.line,self.col,self.name,self.color_pair,bold=self.bold)

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
			self.app.message = f"Disabling {self.name}"
			self.disable()
		else:
			self.app.message = f"Enabling {self.name}"
			self.enable()

	def enable(self):
		if self.enabler:
			self.app.message = f"Running Button({self.name}).enabler({self.target})"
			self.enabler(self.target)
		self.active = True

	def disable(self):
		if self.disabler:
			self.app.message = f"Running Button({self.name}).disabler({self.target})"
			self.disabler(self.target)
		self.active = False
