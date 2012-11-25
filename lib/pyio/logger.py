#!/usr/bin/env python
#
# Copyright (c) 2012, Luke Southam <luke@devthe.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# - Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# - Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
#
# - Neither the name of the DEVTHE.COM LIMITED nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
"""
Shell based logging
"""

from os import system, getpgrp
from sys import stdout, stderr, argv
from optparse import OptionParser

__author__ = "Luke Southam <luke@devthe.com>"
__copyright__ = "Copyright 2012, DEVTHE.COM LIMITED"
__license__ = "The BSD 3-Clause License"
__status__ = "Development"

# the message structure
MESSAGE = """{color}[{cmd};{pid}]: ({type_}) - '{msg}'{color_end}"""

# Color codes
purple = '\033[95m'
blue = '\033[94m'
green = '\033[92m'
orange = '\033[93m'
red = '\033[91m'



#Colored message; to add a bit of (consistent) style to messages.
colors = {
    'DEBUG': blue,
    'MESSAGE': green,
    'WARNING': orange,
    'ERROR': red,
    'UNKNOWN': purple,
}


class Log(object):
    """
    Instance return from getLog; it stores original settings and
    splits logging methods to make log() easier and less repetitive.
    """
    def __init__(self, debug=False, out=stdout, errors=True):
        if not errors:
            errors = out
        self.out = (errors, out)
        self.proc = argv[0]
        self.pid = getpgrp()
        return self

    def logger(self, type_, msg):
        log(slef.proc, self.pid, self.debug, type_, msg, self.out)
        return self

    def debug(self, msg):
        logger("DEBUG", msg)
        return self

    def message(self, msg):
        logger("MESSAGE", msg)
        return self

    def error(self, msg):
        logger("ERROR", msg)
        return self

    def warn(self, msg):
        logger("WARNING", msg)
        return self

def log(cmd, pid, debug, type_, msg, out=(True, stdout)):
    """
    prints out message in MESSAGE format and prints to out.
    """
    type_ = type_.upper()

    type_ = type_ if type_ in colors else "UNKNOWN"
    if type_ == "DEBUG" and not debug:
        return
    elif type_ == "ERROR" and out[0] is True:
        out = stderr
    elif type_ == "ERROR":
        out = out[1]
    elif out[0] is True:
        out = out[1]

    color = colors[type_]
    color_end = "\033[0m"

    print >> out, MESSAGE.format(**locals())


def getLog(debug, out=stdout, errors=True):
    """
    returns an instance of Log.
    """
    if not errors:
        errors = out
    out = (errors, out)
    return lambda type_, msg: log(debug, type_, msg, out)

def tobool(i):
    print i, i.lower().strip() in ['true', 't', 'y', 'yes']
    return i.lower().strip() in ['true', 't', 'y', 'yes']


def main():
    """
    allows logger in bash scripts

    logger="python logger.py" #set to logger.py file
    log="$logger --cmd $0 --pid $$ --debug"
    $log --type debug "Hello there"

    ##also##

    log(){ $log $@ --out /dev/null; }
    log --type error "Now you see me"
    log --type warning "Now you don't"
    """
    parser = OptionParser(usage="%prog [options] --cmd [cmd] --pid [pid] --type [type] [message]")
    parser.add_option("-d", "--debug",
                  action="store_true", dest="debug", default=False,
                  help="print debug messages to stdout")
    parser.add_option("-o", "--out", action="store", type="string", dest="out", default=None,
                  help="print messages to other file() not stdout")
    parser.add_option("--no-errors",
                  action="store_true", dest="no_errors", default=False,
                  help="redirect even errors to --out")
    parser.add_option("-t", "--type", type="string",
                  action="store", dest="type",
                  help="The type")
    parser.add_option("--pid", type="string",
                  action="store", dest="pid",
                  help="The pid")
    parser.add_option("--cmd", type="string",
                  action="store", dest="cmd",
                  help="The command")
    (options, args) = parser.parse_args()
    log_args = [options.cmd, options.pid, options.debug, options.type, " ".join(args)]
    if options.out:
        out = file(options.out, "w")
        errors = not options.no_errors
        outs = (errors, out)
        log_args.append(outs)
    log(*log_args)


if __name__ == '__main__':
    main()
