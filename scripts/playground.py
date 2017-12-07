from browser import document, alert
from ui import Node, Connection, Button

def _rel_mouse_coords(ev):
	offsetX = 0
	offsetY = 0
	elm = ev.target
	while elm:
		offsetX += elm.offsetLeft - elm.scrollLeft
		offsetY += elm.offsetTop - elm.scrollTop
		elm = elm.offsetParent
	return ev.pageX - offsetX, ev.pageY - offsetY

class Playground(object):
	def __init__(self, canvas):
		self.canvas = canvas
		self.context = canvas.getContext('2d')
		self.translation = [0, 0]
		self.nodes = []
		self.connections = []
		self.buttons = []
		self.next_idx = 0

		self.selected_obj = None
		self.selection_type = None

		canvas.bind('mousedown', self.mouse_down)
		canvas.bind('mouseup', self.mouse_up)
		canvas.bind('mousemove', self.mouse_move)
		# canvas.bind('contextmenu', self.context_menu)
		canvas.bind('keypress', self.key_press)

	def find_obj(self, x, y):
		# TODO translation
		for b in self.buttons:
			if b.contains_point(x, y):
				return b
		for n in self.nodes:
			if n.contains_point(x, y):
				return n
		for c in self.connections:
			if c.contains_point(x, y):
				return c
		return None

	def mouse_down(self, ev):
		# TODO translation
		x, y = _rel_mouse_coords(ev)
		clicked_obj = self.find_obj(x, y)

		if self.selection_type is Node:
			self.selected_obj.set_highlight(Node.NO_HIGHLIGHT)
		elif self.selection_type is Connection:
			self.selected_obj.set_highlight(Connection.NO_HIGHLIGHT)

		if clicked_obj is None:
			if self.selection_type is None:
				self.nodes.append(Node(x, y, 'q{}'.format(self.next_idx)))
				self.next_idx += 1
				self.selected_obj = None
				self.selection_type = None
			else:
				self.selected_obj = None
				self.selection_type = None
		elif isinstance(clicked_obj, Button):
			self.selected_obj = clicked_obj
			self.selection_type = Button
		elif isinstance(clicked_obj, Node):
			if self.selection_type is Node:
				# TODO read transition info
				con = self.selected_obj.connect(clicked_obj, None)
				self.connections.append(con)
				self.selected_obj = None
				self.selection_type = None
			else:
				self.selected_obj = clicked_obj
				self.selection_type = Node
		elif isinstance(clicked_obj, Connection):
			self.selected_obj = clicked_obj
			self.selection_type = Connection

		if self.selection_type is Node:
			self.selected_obj.set_highlight(Node.SELECTED)
		elif self.selection_type is Connection:
			self.selected_obj.set_highlight(Connection.SELECTED)

		self.draw()

	def mouse_up(self, ev):
		pass

	def mouse_move(self, ev):
		# self.draw()
		pass

	def key_press(self, ev):
		pass

	def draw(self):
		self.context.fillStyle = '#FFFFFF'
		self.context.fillRect(0, 0, self.canvas.width, self.canvas.height)
		self.canvas.strokeStyle = '#000000'
		self.canvas.lineWidth = 4
		self.context.strokeRect(0, 0, self.canvas.width, self.canvas.height)
		# TODO translation
		for n in self.nodes:
			n.draw(self.context)
		for c in self.connections:
			c.draw(self.context)