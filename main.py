from decoder import Decoder
from time_manager import TimeManager
import cgi

form = cgi.FieldStorage()
searchterm = form.getvalue('searchbox')

decoder = Decoder()
timealloc = TimeManager()
instruction = decoder.decodeInstruction(searchterm)

if instruction == 1:
    timealloc.createEvent()

elif instruction == 2:
    timealloc.checkAvailability()

elif instruction == 3:
    x = 0

else:
    print()
