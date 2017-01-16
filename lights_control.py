#!/usr/bin/python

from datetime import datetime, date, time, timedelta
from time import sleep
import sys
import signal

##functie care aprinde becurile si asteapta o perioada, dupa care le stinge
def flash_the_lights(driver_file, seconds, pm):

    with open (driver_file, 'w') as f:
        f.write(pm.next_pattern())
        f.flush()

    sleep(seconds)


def datetime_from_d_t(d, t):
    return datetime(d.year, d.month, d.day, t.hour, t.minute, 0)

##intoarce sub forma de datetime cand se va incepe urmatorul interval in care
##trebuiesc aprinse luminile. None inseamna ca acum trebuiesc aprinse luminile
def get_next_interval(startd, endd, startt, endt):
    nowdt = datetime.now()
    nowd = nowdt.date()
    nowt = nowdt.time()

    if (startd <= nowd) and (nowd <= endd):
        #suntem in intervalul potrivit
        if (startt < endt):
            #interval de timp normal ex 20- 22
            if (startt <= nowt) and (nowt <= endt):
                return None
            else:
                if nowt < startt:
                    return datetime_from_d_t(nowd, startt)
                else:
                    return datetime_from_d_t(nowd + timedelta(days=1), startt)
        else:
            #interval de timp care trece peste zi: ex 22:00 - 06:00
            if (startt <= nowt) or (nowt <= endt):
                return None
            else:
                return datetime_from_d_t(nowd, startt)
    elif endd < nowd:
        close_signal(None, None)
    else:
        if (nowd < startd):
            return datetime_from_d_t(startd, startt)
        else:
            return datetime_from_d_t(startd + timedelta(days=365), startt)


class PatternManager:
    onchar = '*'
    offchar = '-'
    numled = 12

    def __init__(self, filepath):
        self.current = 0
        with open(filepath, "r") as f:
            lines = f.readlines()
            self.size = len(lines)
            self.patterns = [x.replace(PatternManager.onchar, '1').replace( \
                    PatternManager.offchar, '0').ljust(PatternManager.numled, \
                    '0')[:PatternManager.numled] for x in lines]

        if (self.size == 0):
            self.patterns = ['0' * PatternManager.numled]

    def next_pattern(self):
        result = self.patterns[self.current]
        self.current = (self.current + 1) % self.size
        return result

    def reset(self):
        self.current = 0

if len(sys.argv) != 8:
    print "Wrong arguments"
    sys.exit(1)

def parse_date(dstr):
    sp = dstr.split('-')
    return date(int(sp[0]), int(sp[1]), int(sp[2]))

def parse_time(tstr):
    sp = tstr.split(':')
    return time(int(sp[0]), int(sp[1]), 0)

drv_path = sys.argv[1]


def close_the_lights():
    with open(drv_path, "w") as f:
        f.write('0' * 12)
        f.flush()
        f.close()

def close_signal(signal, frame):
    close_the_lights()
    sys.exit(0)

signal.signal(signal.SIGTERM, close_signal)

start_date = parse_date(sys.argv[2])
start_time = parse_time(sys.argv[3])
end_date = parse_date(sys.argv[4])
end_time = parse_time(sys.argv[5])
speed = sys.argv[6]
pm = PatternManager(sys.argv[7])

if (speed == 0):
    sec = 3
elif speed == 1:
    sec = 1.5
else:
    sec = 0.75

while True:
    next_int = get_next_interval(start_date, end_date, start_time, end_time)
    if next_int == None:
        flash_the_lights(drv_path, sec, pm)
    else:
        close_the_lights()
        diff = next_int - datetime.now()
        pm.reset()
        sleep(diff.total_seconds())
