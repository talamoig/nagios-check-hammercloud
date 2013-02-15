#!/usr/bin/python

import sys
import re
import datetime
import urllib
import urllib2
import getopt
from optparse import OptionParser

CRITICAL=0.8
WARNING=0.9

RET_OK=0
RET_WARN=1
RET_CRIT=2
RET_UNKN=3


def hammercloud(sitename,days):
    
    now=datetime.datetime.now()
    d=datetime.timedelta(days)
    yesterday=now-d
    time=yesterday.strftime("%m/%d/%Y %H:%M")
    url='http://hammercloud.cern.ch/hc/app/cms/joberrors/?&cloud=&test=&template=&start_date=%s&end_date='%urllib.quote(time,"")
    response = urllib2.urlopen(url)
    html=response.read().split("\n")
    html=map(lambda x:x.strip(),html)
    res=filter(lambda x:x.find("<td>%s"%sitename)==0,html)
    if len(res)!=1:
        print("Cannot find %s in %url"%(sitename,url))
        sys.exit(RET_UNKN)
    res=res[0]
    exp=".*<td>.*</td><td>([\.0-9]*)</td><td><a href=.*>([\.0-9]*) .*</td><td><a href=.*>([\.0-9]*) .*</td><td>(.*)</td></tr>"
    r=re.compile(exp)
    m=r.match(res)
    if m:
        total=int(m.group(1).replace(".",""))
        gridfailed=int(m.group(2).replace(".",""))
        appfailed=int(m.group(3).replace(".",""))
        totalfailed=gridfailed+appfailed
        efficiency=m.group(4)
        efficiency=float(efficiency)
        print "HammerCloud Efficiency: %s (%s/%s)"%(efficiency,total,totalfailed)
        if efficiency<CRITICAL and total>0:
            sys.exit(RET_CRIT)
        if efficiency<WARNING:
            sys.exit(RET_WARN)
        sys.exit(RET_OK)
    print("Cannot find match in %s"%res)
    sys.exit(RET_UNKN)
        

def main():
    usage = "usage: %prog [options] sitename"
    parser = OptionParser(usage)
    parser.add_option("-d", "--days", dest="days", default=1,
                      help="days to take into account for HammerCloud efficiency (default=1)")
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("Please specify a CMS site name")
    return hammercloud(args[0],options.days)
#    print args[0]
#    print options.days
    
if __name__ == "__main__":
    main()
                
