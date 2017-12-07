from itertools import chain
from math import pi, sin, cos, atan2
from browser import document

class Node(object):
	NO_HIGHLIGHT = 0
	SELECTED = 1
	ACTIVE = 2

	radius = 20
	selection_ring_extra_radius = 4
	selection_ring_color = '#4444DDA0'
	selection_ring_thickness = 4
	active_ring_extra_radius = 4
	active_ring_color = '#DD4444A0'
	active_ring_thickness = 4

	font_name = 'Arial'
	font_size = 16

	def __init__(
		self,
		x, y, text, *,
		border_thickness=1,
		fill_color='white', border_color='black'):

		self.x = x
		self.y = y
		self.text = text
		self.border_thickness = border_thickness
		self.fill_color = fill_color
		self.border_color = border_color
		self.highlight = Node.NO_HIGHLIGHT
		self._outgoing_connections = []
		self._incoming_connections = []

	def move_to(self, x, y):
		self.x = x
		self.y = y

		for con in chain(
			self._outgoing_connections,
			self._incoming_connections):

			con.update()

	def set_highlight(self, highlight):
		self.highlight = highlight

	def connect(self, other, args):
		c = Connection(self, other, args)
		self._outgoing_connections.append(c)
		other._incoming_connections.append(c)

	def draw(self, context):
		context.save()
		r = Node.radius

		context.beginPath()
		context.fillStyle = self.fill_color
		context.arc(self.x, self.y, r, 0, 2*pi)
		context.fill()
		r += self.border_thickness / 2

		if self.highlight & Node.SELECTED:
			r += Node.selection_ring_extra_radius
			context.beginPath()
			context.lineWidth = Node.selection_ring_thickness
			context.strokeStyle = Node.selection_ring_color
			context.arc(self.x, self.y, r, 0, 2*pi)
			context.stroke()
			r += Node.selection_ring_thickness / 2
		if self.highlight & Node.ACTIVE:
			r += Node.active_ring_extra_radius
			context.beginPath()
			context.lineWidth = Node.active_ring_thickness
			context.strokeStyle = Node.active_ring_color
			context.arc(self.x, self.y, r, 0, 2*pi)
			context.stroke()
			r += Node.active_ring_thickness / 2

		context.beginPath()
		context.strokeStyle = '#000000'
		context.lineWidth = self.border_thickness
		context.arc(
			self.x, self.y,
			Node.radius,
			0, 2*pi)
		context.stroke()

		context.textAlign = 'center'
		context.font = '{}pt {}'.format(Node.font_size, Node.font_name)
		context.fillStyle = '#000000'
		context.fillText(self.text, self.x, self.y + Node.font_size / 2)
		context.restore()

	def draw_outgoing_connections(self, context):
		for con in self._outgoing_connections:
			con.draw(context)

class Connection(object):
	head_width = 10
	head_length = 15
	head_angle = atan2(head_width/2, head_length)
	line_thickness = 2

	def __init__(self, start_node, end_node, info):
		self.start_node = start_node
		self.end_node = end_node
		if info is None:
			self.info = None
		else:
			self.info = tuple(info)
		self.update()

	def update(self):
		self.start_point = [self.start_node.x, self.start_node.y]
		self.end_point = [self.end_node.x, self.end_node.y]

		dy = self.end_point[1] - self.start_point[1]
		dx = self.end_point[0] - self.start_point[0]
		shaft_angle = atan2(dy, dx)
		self.start_point[0] += self.start_node.radius * cos(shaft_angle)
		self.start_point[1] += self.start_node.radius * sin(shaft_angle)
		self.end_point[0] -= self.end_node.radius * cos(shaft_angle)
		self.end_point[1] -= self.end_node.radius * sin(shaft_angle)

		self.head_points = [
			[self.end_point[0], self.end_point[1]],
			[self.end_point[0], self.end_point[1]]]

		self.head_points[0][0] += Connection.head_length * cos(
			pi + shaft_angle - Connection.head_angle)
		self.head_points[0][1] += Connection.head_length * sin(
			pi + shaft_angle - Connection.head_angle)

		self.head_points[1][0] += Connection.head_length * cos(
			pi + shaft_angle + Connection.head_angle)
		self.head_points[1][1] += Connection.head_length * sin(
			pi + shaft_angle + Connection.head_angle)

	def draw_info(self):
		pass

	def draw(self, context):
		context.save()
		# TODO allow curved arrows
		context.beginPath()
		context.strokeStyle = '#000000'
		context.lineWidth = Connection.line_thickness
		context.moveTo(*self.start_point)
		context.lineTo(*self.end_point)
		context.moveTo(*self.head_points[0])
		context.lineTo(*self.end_point)
		context.moveTo(*self.head_points[1])
		context.lineTo(*self.end_point)
		context.stroke()
		context.restore()

