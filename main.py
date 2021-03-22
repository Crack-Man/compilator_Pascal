from lexer.queue_token import QueueToken
from lexer.directive import Directive
from lexer.space import Space

queue = QueueToken()
d = Directive()
d.set_coordinates(1)
queue.append_token(d)
s = Space()
queue.append_token(s)
list = queue.get_queue()
print(list[1].get_coordinates())