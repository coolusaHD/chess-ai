import datetime
from time import sleep

time = datetime.datetime.now()

sleep(1)

time2 = datetime.datetime.now()

diff = time2 - time

print(diff.seconds+diff.microseconds/1000000)