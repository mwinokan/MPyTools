import curses

LEFT_CLICK = curses.BUTTON1_CLICKED
LEFT_DOUBLE = curses.BUTTON1_DOUBLE_CLICKED
RIGHT_CLICK = curses.BUTTON3_CLICKED
RIGHT_DOUBLE = curses.BUTTON3_DOUBLE_CLICKED
SCROLL_UP = 2097152
SCROLL_DOWN = 2097152

class CursesApp():
	"""A CLI-App Class based on pycurses"""
	def __init__(self,padding=2):

		# self.line_buffer = []

		self.texts = []
		self.buttons = []
		self.drawables = []
		self.mouse = None

		self.message = None

		self._scr = curses.initscr()

		curses.noecho()
		curses.cbreak()
		self.scr.keypad(True)
		curses.curs_set(0)
		curses.start_color()
		curses.mousemask(-1)

		self.define_pairs()

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
			obj.draw(self.scr)

	def get_dims(self):
		self.h, self.w = self.scr.getmaxyx()

	def draw(self):
		redraw = self.process_keypress()
		self.drawcore()
		return redraw

	def firstdraw(self):
		self.get_dims()
		self.drawcore()

	def drawcore(self):
		self.scr.clear()
		self.draw_objects()
		# self.draw_debug()
		self.scr.refresh()

	def draw_debug(self):
		self.scr.addstr(self.h-2,0,f'{self.message}')
		self.scr.addstr(self.h-1,0,f'{self.mouse}')

	def process_keypress(self):
		self.key = self.scr.getch()

		if self.key == curses.KEY_MOUSE:
			return self.process_mouse()

		return False

	def process_mouse(self):
		self.mouse = curses.getmouse()
		x = self.mouse[1]
		y = self.mouse[2]
		state = self.mouse[4]

		for button in self.buttons:
			if button.is_hit(x,y):
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
	def scr(self):
		return self._scr

	def define_pairs(self):
		curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_WHITE)
		curses.init_pair(2,curses.COLOR_BLACK,curses.COLOR_YELLOW)

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

	def __init__(self,name,line,col,color_pair=None):
		self.name = name
		self.line = line
		self.length = len(self.name)
		self.col = col
		self.endcol = self.col + self.length
		self.color_normal = curses.color_pair(0)
		self.color_pair = color_pair or curses.color_pair(0)

	def draw(self,scr):
		scr.attron(self.color_pair)
		scr.addstr(self.line,self.col,self.name)
		scr.attroff(self.color_pair)
		scr.clrtoeol()

class Button(Text):
	def __init__(self,app,name,line,col,active=False,enabler=None,disabler=None,target=None):
		super(Button, self).__init__(name,line,col)

		self.app = app
		self.active = active
		self.color_inactive = curses.color_pair(1)
		self.color_active = curses.color_pair(2)

		self.enabler = enabler
		self.disabler = disabler
		self.target = target
	
	def draw(self,scr):
		if self.active:
			scr.attron(self.color_active)
			scr.addstr(self.line,self.col,self.name)
			scr.attroff(self.color_active)
		else:
			scr.attron(self.color_inactive)
			scr.addstr(self.line,self.col,self.name)
			scr.attroff(self.color_inactive)
		scr.clrtoeol()

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
