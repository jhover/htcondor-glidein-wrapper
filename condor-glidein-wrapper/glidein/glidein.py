#!/bin/env python

import getopt
import logging
import os
import socket
import subprocess 
import sys

def setup_logging():
    print("setup_logging...")
    # Set up logging. 
    # Check python version 
    major, minor, release, st, num = sys.version_info
    
    # Set up logging, handle differences between Python versions... 
    # In Python 2.3, logging.basicConfig takes no args
    #
    FORMAT23="[ %(levelname)s ] %(asctime)s %(filename)s (Line %(lineno)d): %(message)s"
    FORMAT24=FORMAT23
    FORMAT25="[%(levelname)s] %(asctime)s %(module)s.%(funcName)s(): %(message)s"
    FORMAT26=FORMAT25
    
    if major == 2:
        if minor ==3:
            formatstr = FORMAT23
        elif minor == 4:
            formatstr = FORMAT24
        elif minor == 5:
            formatstr = FORMAT25
        elif minor == 6:
            formatstr = FORMAT26
    
    log = logging.getLogger()
    hdlr = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(FORMAT23)
    hdlr.setFormatter(formatter)
    log.addHandler(hdlr)

def gather_info():
    print("hostname is %s" % socket.gethostname())
    keys = os.environ.keys()
    keys.sort()
    for i in keys:
        print("%s = %s" % (i,os.environ[i]))
       

def main():
    usage = """
    usage: $0 [options]

Run glidein against given collector:port and auth for at least -x seconds. 

OPTIONS:
    -h --help           Print help.
    -d --debug          Debug logging.      
    -v --verbose        Verbose logging. 
    -c --collector      Collector name
    -p --port           Collector port
    -a --authtype       Auth [password|gsi]
    -t --authtoken      Auth token (password or comma-separated subject DNs for GSI)
    -x --lingertime     Glidein linger time seconds [300]
"""
    
    # Defaults
    debug = True
    verbose = False
    collector="gridtest05.racf.bnl.gov"
    port= 29618
    authtype="password"
    authtoken="changeme"
    lingertime=600   # 10 minutes
    
    # Handle command line options
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, 
                                   "hdvc:p:a:t:x:", 
                                   ["help",
                                    "debug",
                                    "verbose", 
                                    "collector=", 
                                    "port=", 
                                    "authtype=",
                                    "authtoken=",
                                    "lingertime",
                                    ])
    except getopt.GetoptError, error:
        print( str(error))
        print( usage )                          
        sys.exit(1)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(usage)                     
            sys.exit()            
        elif opt in ("-d", "--debug"):
            debug = True
            verbose = False
        elif opt in ("-v", "--verbose"):
            verbose = True
            debug = False
        elif opt in ("-c", "--collector"):
            collector_host = arg
        elif opt in ("-p", "--port"):
            collector_port = int(arg)
        elif opt in ("-a", "--authtype"):
            authtype = arg
        elif opt in ("-t", "--authtoken"):
            authtoken = arg
        elif opt in ("-x","--lingertime"):
            lingertime = int(arg)
              
    setup_logging()
    log=logging.getLogger()    

    log.setLevel(logging.WARNING)
    print("debug is %s" % debug)
    print('verbose is %s' % verbose)
    if debug: 
        log.setLevel(logging.DEBUG) # Override with command line switches
        log.debug('Logging set to debug')
    if verbose:
        log.setLevel(logging.INFO) # Override with command line switches
        log.info('Logging set to info')

    log.info('python scripts work!')
    #p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    
    gather_info()
        

if __name__ == '__main__':
    main()