from browser import document, alert, window

_canvas_div = document['maindiv']
_canvas = document['maincanvas']

def on_resize(ev):
	_canvas.height = _canvas_div.height
	_canvas.width = _canvas_div.width

on_resize(None)
window.bind('resize', on_resize)