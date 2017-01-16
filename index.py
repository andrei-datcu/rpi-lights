#!/usr/bin/python
from ConfigParser import ConfigParser
import time
import subprocess

def is_running():
    try:
        s = subprocess.check_output(["pgrep", "lights_control"])
        return True
    except subprocess.CalledProcessError:
        return False
    return False

config = ConfigParser()
config.read("/home/root/xmas.cfg")

dic = config._sections.get('all', {})


print "<!DOCTYPE HTML>"
print "<html>"
print "<head>"
print "<title>XMAS Lights Controller</title>"
print '<meta charset="utf-8">'
print '<meta name="viewport" content="width=device-width, initial-scale=1">'
print '<link rel="stylesheet" href="/bootstrap.min.css">'
print '<link rel="stylesheet" href="/bootstrap-select.min.css">'
print '<link rel="stylesheet" href="/bootstrap-timepicker.min.css">'
print '<link rel="stylesheet" href="/datepicker.css">'
print '<script src="/jquery.min.js"></script>'
print '<script src="/bootstrap.min.js"></script>'
print '<script src="/bootstrap-select.min.js"></script>'
print '<script src="/bootstrap-timepicker.min.js"></script>'
print '<script src="/bootstrap-datepicker.js"></script>'
print '<script type="text/javascript"> $(document).ready(function(e) {'
print "$(\'.selectpicker\').selectpicker();$(\'#dp\').datepicker({format: \"yyyy-mm-dd\"});$(\'#dp2\').datepicker({format: \"yyyy-mm-dd\"});"
print "$(\'#tp1\').timepicker({showMeridian: false});;"
print "$(\'#tp2\').timepicker({showMeridian: false});});"
print "</script>"

print '<STYLE type="text/css">'
print '.form-horizontal .control-label { text-align:left !important;}'
print '    </STYLE>'

print '</head>'
print "<body>"

print '<div class="container">'

print '<h2 style=""> Christmas Lights controller</h2>'
print '<form class="form-horizontal" method="post" action="/process_args.py" role="form">'

print '<div class="form-group"><label class="control-label col-sm-3" for="drv_path">Calea catre driverul ledurilor</label>'
print '<div class="col-sm-5"><input type="text" class="form-control" id="drv_path" name="drv_path" value="%s"></div>' % \
        dic.get('drv_path', '/dev/xmas')
print '</div>'
print '<div class="form-group"><label class="control-label col-sm-3" for="pattern_path">Calea catre fisierul pattern</label>'
print '<div class="col-sm-5"><input type="text" class="form-control" id="pattern_path" name="pattern_path" value="%s"></div>' % \
        dic.get("pattern_path","/home/root/pattern")
print '</div>'
print '<div class="form-group"><label class="control-label col-sm-3" for="log_path">Calea catre fisierul log</label>'
print '<div class="col-sm-5"><input type="text" class="form-control" id="log_path" name="log_path" value="%s"></div>' % \
        dic.get("log_path", "/home/root/log")
print '</div>'

print '<div class="form-group"><label class="control-label col-sm-3">'
print '<span style="font-weight: bold;"> Data acum: </span> </label>'
print '<div class="col-sm-5"><p>%s</p></div></div>' % time.strftime("%c")

print '<div class ="form-group"> <label class="control-label col-sm-3">Perioada functionarii </label>'
print '<div class = "col-sm-5"><div class="controls form-inline">'
print '<input type="text" class="form-control" name="startd" id="dp" value="%s"> - ' % dic.get("startd", "2016-12-19")
print '<input type="text" class="form-control" id="dp2" name="endd" value="%s">' % dic.get("endd", "2017-01-26")
print '</div></div></div>'


print '<div class ="form-group"> <label class="control-label col-sm-3">Perioada functionarii </label>'
print '<div class = "col-sm-5"><div class="controls form-inline">'
print '<input class="form-control" type="text" id="tp1" name="startt" value="%s"> -' % dic.get("startt", "19:00")
print ' <input class="form-control" type="texte" id="tp2" name="endt" value="%s">' \
        % dic.get("endt", "02:05")
print '</div></div></div>'

print '<div class = "form-group"><label class="control-label col-sm-3">Viteza</label>'
print '<div class = "col-sm-5"><select class="selectpicker" name="speed">'
options = {'lent':0, 'normal':1, 'rapid':2}
keys = options.keys()
keys.sort()
speed = int(dic.get("speed", 0))
for i in keys:
    if (options[i] == speed):
        print '<option selected value="%d">%s</option>' % (options[i], i)
    else:
        print '<option value="%d">%s</option>' % (options[i], i)
print '</select></div></div>'


print '<div class ="form-group"> <label class="control-label col-sm-3">Starea curenta</label>'
print '<div class = "col-sm-5">'
if is_running():
    print '<span style="color:green; font-weight: bold;"> pornit </span>'
else:
    print '<span style="color:red; font-weight: bold;"> oprit </span>'
print '</div></div>'

print '<div class ="form-group">'
print '<div style="text-align:center;" class="controls form-inline col-sm-8">'
print '<input type="submit" class="btn btn-default" name ="running" value="Porneste" >'
print '<input type="submit" class="btn btn-default" name="stopped" value="Opreste">'
print'</div></div>'

print '</form></div>'
print '</body></html>'
