#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 22:20:31 2012

@author: root
"""

from optparse import OptionParser,OptionGroup
import subprocess
import re
import sys

def free(opt,args):
    # Get process info
    ps = subprocess.Popen(['ps', '-caxm', '-orss,comm'], stdout=subprocess.PIPE).communicate()[0]
    vm = subprocess.Popen(['vm_stat'], stdout=subprocess.PIPE).communicate()[0]

    # Iterate processes
    processLines = ps.split('\n')
    sep = re.compile('[\s]+')
    rssTotal = 0 # kB
    for row in range(1,len(processLines)):
        rowText = processLines[row].strip()
        rowElements = sep.split(rowText)
        try:
            rss = float(rowElements[0]) * 1024
        except:
            rss = 0 # ignore...
        rssTotal += rss

    # Process vm_stat
    vmLines = vm.split('\n')
    sep = re.compile(':[\s]+')
    vmStats = {}
    for row in range(1,len(vmLines)-2):
        rowText = vmLines[row].strip()
        rowElements = sep.split(rowText)
        vmStats[(rowElements[0])] = int(rowElements[1].strip('\.')) * 4096
    if opt.vm_stat:
        print 'Wired Memory:\t\t%d MB' % ( vmStats["Pages wired down"]/1024/1024 )
        print 'Active Memory:\t\t%d MB' % ( vmStats["Pages active"]/1024/1024 )
        print 'Inactive Memory:\t\t%d MB' % ( vmStats["Pages inactive"]/1024/1024 )
        print 'Free Memory:\t\t%d MB' % ( vmStats["Pages free"]/1024/1024 )
        print 'Real Mem Total (ps):\t%.3f MB' % ( rssTotal/1024/1024 )
    else:
        total=(vmStats["Pages wired down"]+vmStats["Pages active"]+ \
              vmStats["Pages inactive"]+vmStats["Pages free"])/1024
        free=(vmStats["Pages inactive"]+vmStats["Pages free"])/1024
        used=total-free
        shared=0
        print    '\t\t total  \t used  \t free  \t shared  \t buffers \t cached'
        print 'Mem: \t\t%d  \t %d \t%d \t %d '%(total,used,free,shared)
        print "-/+ buffers/cache:"
        print "Swap:"



if __name__ =="__main__":

    parser = OptionParser(usage="usage: free [-b|-k|-m|-g] [-l] [-o] [-t] [-s delay] [-c count] [-V]",
                          epilog="free tool on Mac OS"
                         )


    group=OptionGroup(parser,"show output in bytes, KB, MB, or GB",
                      description=None)
    group.add_option("-b", action="store_true", help="show output in bytes.")
    group.add_option("-k", action="store_true", help="show output in KB.")
    group.add_option("-m", action="store_true", help="show output in MB.")
    group.add_option("-g", action="store_true", help="show output in GB.")
    parser.add_option_group(group)


    parser.add_option("-l",action="store_true",help= "show detailed low and high memory statistics")
    parser.add_option("-o",

                      action="store_true",
                      help="use old format (no -/+buffers/cache line)")
    parser.add_option("-t",action="store_true",help= "display total for RAM + swap")
    parser.add_option("-s",action="store",dest="delay",type='int',
                      help= "update every [delay] seconds")
    parser.add_option("-c",action="store",dest="count",type='int',
                      help= "update [count] times")
    parser.add_option("-V",action="store_true",default="Version 1.0",
                      help= "display version information and exit",
                      )
    parser.add_option("-v","--vm_stat",action="store_true",dest="vm_stat",
                      help= "display format like vm_stat",
                      )

    (options, args) = parser.parse_args()
    free(options,args)

