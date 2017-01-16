#!/usr/bin/python

import cgi
from ConfigParser import ConfigParser
import os
import subprocess
import sys
import os.path
import time

def print_error(s):
    print "<html><body><p>"
    print "Eroare: %s" % s
    print "</p></body></html>"


def gen_logrotate_conf(logpath):
    logname = os.path.basename(logpath)
    confpath = "/etc/logrotate.d/xmaslog_" + logname

    if not os.path.isfile(confpath):
        st = os.statvfs(logpath)
        free_size = (st.f_bavail * st.f_frsize) / (1024 * 1024)
        with open(confpath, "w") as f:
            f.write('%s {\n' % os.path.abspath(logpath))
            f.write('\trotate 0\n')
            f.write('\tdaily\n')
            f.write('\tmissingok\n')
            f.write('\tsize %dM\n' % free_size)
            f.write('}\n')
            f.close()

form = cgi.FieldStorage()

userip = os.environ["REMOTE_ADDR"]

configpath = "/home/root/xmas.cfg"

config = ConfigParser()
config.read(configpath)
if not config.has_section('all'):
    config.add_section('all')

if 'stopped' in form:
    os.system("killall lights_control.py")

    with open(config.get("all", "log_path"), "a") as logfile:
        if config.has_option("all", "running"):
            config.remove_option("all", "running")
            logfile.write("Userul cu IPul %s a oprit luminile\n" % userip)

    config.set("all", "stopped", "Opreste")
    with open(configpath, 'w') as f:
        config.write(f)

    print "HTTP/1.0 302 OK"
    print "Location: /index.py"
    print ""

    sys.exit()

##Nu am oprit, deci pornim sau schimbam setarile

##Sanity checks
if ( not os.path.isfile(form['drv_path'].value)\
        or not os.access(form['drv_path'].value, os.W_OK)):
    print_error('Device node-ul "%s" nu exista/nu este accesibil. Back si reincercati' % form['drv_path'].value)
    sys.exit()

if ( not os.path.isfile(form['pattern_path'].value)\
        or not os.access(form['pattern_path'].value, os.R_OK)):
    print_error('Fisierul pattern "%s" nu exista/nu este accesibil. Back si reincercati' % form['pattern_path'].value)
    sys.exit()

logpath = form['log_path'].value
try:
    f = open(logpath, "a")
    f.close()
except IOError:
    print_error('Fisierul pentru log "%s" nu poate fi deschis. Back si reincercati' % logpath)
    sys.exit()


### Salvam ceilalti parametrii
gen_logrotate_conf(logpath)
with open(logpath, "a") as logfile:
    if config.has_option('all', 'stopped'):
        #A fost oprit, acum il pornim
        config.remove_option('all', 'stopped')
        logfile.write("Userul cu IPul %s a pornit luminile\n" % userip)

    verb_name = {
            'drv_path': 'calea pentru device node',
            'pattern_path': 'calea fisierului pattern',
            'log_path': 'calea fisierului log',
            'startd' : 'data de inceput',
            'endd': 'data de sfarsit',
            'startt': 'timpul de inceput',
            'endt': 'timpul de sfarsit',
            'speed': 'viteza de aprindere',
            }

    for ckey in form:
        if config.has_option('all', ckey):
            old_val = config.get('all', ckey)
            if (old_val != form[ckey].value):
                #adaugam intrare in log
                logfile.write('Userul cu IPul %s a modificat %s din %s in %s\n' % \
                        (userip, verb_name[ckey], old_val, form[ckey].value))
        config.set('all', ckey, form[ckey].value)

#start led script here

os.system("killall lights_control.py")

args = ['lights_control.py', form['drv_path'].value, form['startd'].value,\
form['startt'].value, form['endd'].value, form['endt'].value, form['speed'].value,\
form['pattern_path'].value]

p = subprocess.Popen(args, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

with open(configpath, 'w') as f:
    config.write(f)

print "HTTP/1.0 302 OK"
print "Location: /index.py"
print ""
