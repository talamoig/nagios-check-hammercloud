#!/usr/bin/python

import sys
import re
import datetime
import urllib
import urllib2

CRITICAL=0.8
WARNING=0.9

RET_OK=0
RET_WARN=1
RET_CRIT=2
RET_UNKN=3

now=datetime.datetime.now()
d=datetime.timedelta(1)
yesterday=now-d
time=yesterday.strftime("%m/%d/%Y %H:%M")
url='http://hammercloud.cern.ch/hc/app/cms/joberrors/?&cloud=&test=&template=&start_date=%s&end_date='%urllib.quote(time,"")
response = urllib2.urlopen(url)
html=response.read().split("\n")
html=map(lambda x:x.strip(),html)
try:
    site=sys.argv[1]
except Exception:
    sys.stderr.write("Please specify a site name (eg. T2_IT_Rome)")
    os.exit(unknown)
res=filter(lambda x:x.find("<td>%s"%site)==0,html)
if len(res)!=1:
    sys.exit(RET_UNKN)
res=res[0]
exp=".*<td>(.*)</td></tr>"
r=re.compile(exp)
m=r.match(res)
if m:
    efficiency=m.group(1)
    efficiency=float(efficiency)
    print "Hammer Cloud Efficiency: %s"%efficiency
    if efficiency<CRITICAL:
        sys.exit(RET_CRIT)
    if efficiency<WARNING:
        sys.exit(RET_WARN)
    sys.exit(RET_OK)
sys.exit(RET_UNKN)
                                                    
# should never be here
