from math import pi, sin, cos, atan2
from browser import document

class Node(object):
	radius = 20

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
		self._connections = []

	def move_to(self, x, y):
		self.x = x
		self.y = y

		for con in self._connections:
			con.update()

	def connect(self, other, *args):
		self._connections.append(Connection(self, other, args))

	def draw(self, context):
		context.beginPath()
		context.fillStyle = self.fill_color
		context.arc(
			self.x, self.y,
			Node.radius,
			0, 2*pi)
		context.fill()

		context.beginPath()
		context.lineWidth = self.border_thickness
		context.arc(
			self.x, self.y,
			self.radius,
			0, 2*pi)
		context.stroke()
		# TODO draw text

		for con in self._connections:
			con.draw(context)

class Connection(object):
	head_width = 10
	head_length = 15
	head_angle = atan2(head_width/2, head_length)
	line_thickness = 1

	def __init__(self, start_node, end_node, info):
		self.start_node = start_node
		self.end_node = end_node
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
		# TODO allow curved arrows
		context.beginPath()
		context.lineWidth = Connection.line_thickness
		context.moveTo(*self.start_point)
		context.lineTo(*self.end_point)
		context.moveTo(*self.head_points[0])
		context.lineTo(*self.end_point)
		context.moveTo(*self.head_points[1])
		context.lineTo(*self.end_point)
		context.stroke()

