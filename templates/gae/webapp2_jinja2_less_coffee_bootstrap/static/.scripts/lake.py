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
Hello; I'm lake.
A simple python script made for the purpose of
creating a stress-free process to compile your
less files to css.
"""
from optparse import OptionParser
from os import system as shell, listdir as ls
from os.path import isfile
import json
import sys
import tty
import termios
import signal

__author__ = "Luke Southam <luke@devthe.com>"
__copyright__ = "Copyright 2012, DEVTHE.COM LIMITED"
__license__ = "The BSD 3-Clause License"
__status__ = "Development"


def main(paths, paths_l, nw_path, lesses, files, Lakefile, config,
         ignore, quite, force, *args, **kwargs):
    if not quite:
        shell('clear')
        print bcolors.HEADER + __doc__.split('\n')[1] + bcolors.ENDC
        print "\n".join(__doc__.split('\n')[2:])

        print "I'm presuming the files are at %s " % "".join(
            [(path + "/*.less") for path in paths_l])

        print "and files at sub directory e.g. %s" % paths_l[0] + "/imports/*.less"
        print "are to be ignored."

        if Lakefile:
            print bcolors.OKBLUE + "Ha!Ha! that's a Lakefile I see " +\
                "well those files shell be ignored!" + bcolors.ENDC

        print
        print
        print

    if not force:
        print bcolors.OKGREEN + "final list to compile is:" + bcolors.ENDC
        for old_file, nw_file in files:
            print "    - \033[94m%s\033[0m -> \033[92m%s\033[0m" % (old_file,
                                                                    nw_file)
        confirm()

    s = signal.signal(signal.SIGINT, signal.SIG_IGN)

    if not quite:
        print
        print
        print

    i = 0
    c = 0
    compiled = []
    ignored = []
    total_ops = float(len(files) + 1)
    n = 0

    for f in files:
        if f not in ignore:
            n += 1
            if not quite: center("compiling %r \n" % f[1] + get_loader(n / total_ops))
            less(*f)
            compiled.append(f)
            c += 1
        else:
            n += 1
            if not quite: center("ignoring %s \n" % f[0] + get_loader(n / total_ops))
            ignored.append(f)
            i += 1

    p = ["'" + path + "'" for path in paths_l]
    msg = "\n"

    msg += "    \033[92m compiled %r files\033[0m from %s" % (
        c, "".join(p) + (":" if c > 0 else ""))
    msg += "\n"
    for f in compiled:
        msg += "        - \033[94m%s\033[0m -> \033[92m%s\033[0m" % f
        msg += "\n"

    msg += "\n"

    msg += "    \033[94mignored %r files\033[0m from %s" %\
        (i, "".join(p) + (":" if i > 0 else ""))
    for f in ignored:
        msg += "        - \033[94m%s\033[0m" % f[0]
        msg += "\n"

    i += 1

    if not quite:
        center("DONE!\n" + get_loader(1) + msg)
        signal.signal(signal.SIGINT, s)
        if not force:
            confirm(msg=False)
        raise KeyboardInterrupt


def get_file():
    if isfile('Lakefile'):
        lake_file = True
        config = json.loads((file('Lakefile').read()))
    else:
        lake_file = False
        config = {}
    ignore = [i + ".less" for i in config['ignore']] if 'ignore' in config\
        else []

    return  lake_file, config, ignore


def fix_path(path):
    """
    fixes paths to be 'a_dir/' and
    '/a_dir/sub_dir'
    """
    if isinstance(path, list):
        path = [fix_path(p) for p in path]
    else:  # is str and single
        path = str(path)
        if path.startswith('./'):
            path = path[2:]
        if path == ".":
            path = ""
    return path


def get_vars():
    path = "less/"
    nw_path = "static/css/"
    paths=[path] # Need to fix
    path = fix_path(path)
    nw_path = fix_path(nw_path)
    Lakefile, config, ignore = get_file()

    paths_l = []
    for n in range(len(paths)):
        if n == 0:
            paths_l.append(paths[n])
        elif n + 1 == len(paths):
            paths_l.append("and " + paths[n])
        else:
            paths_l.append(", " + paths[n])

    lesses = [i
              for o in [[(path, (f[:2] if f.startswith("./") else f))
                        for f in ls(path)
                        if f.endswith('.less')]
                        for path in paths]
              for i in o]

    files = []
    for less in lesses:
        if less not in ignore:
            old_file = "/".join(less)
            nw_file = nw_path + (less[1][:-5]
                                 if less[1].endswith('.less') else less[1])
            nw_file += ".css"
            files.append((old_file, nw_file))

    parser = OptionParser()
    parser.add_option("-o", "--orign", dest="orign", default=path,
                      help="Orign Folder of less files", metavar="FILE")
    parser.add_option("-d", "--destination", dest="dest", default=nw_path,
                      help="Destination Folder for less files", metavar="FILE")
    parser.add_option("-f", "--force",
                      action="store_true", dest="force", default=False,
                      help="ignore warnings")
    parser.add_option("-q", "--quite",
                      action="store_true", dest="quite", default=False,
                      help="suppress output")
    force = parser.parse_args()[0].force
    quite = parser.parse_args()[0].quite
    nw_path = parser.parse_args()[0].dest

    paths=[path] # Need to fix

    return vars()


def confirm(msg=True):
    if msg:
        try:
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            old[3] = old[3] | termios.ECHO
            tty.setcbreak(sys.stdin)
            n = 0
            while True:
                print
                sys.stdout.write(bcolors.WARNING +
                                 "is this correct ?  ( y or n ): " +
                                 bcolors.ENDC +
                                 bcolors.HEADER)
                ans = sys.stdin.read(1)
                sys.stdout.write(ans)
                if not ans or ans not in ['y', 'Y', 'n', 'N']:
                    print
                    print bcolors.FAIL + 'invalid input' + bcolors.ENDC
                    n += 1
                    if n >= 3:
                        print bcolors.FAIL
                        print "Please read -h " + \
                            "to craft a greater understanding in"
                        print "how to configure lake" + \
                            "for your project structure"
                        print bcolors.ENDC
                        termios.tcsetattr(fd, termios.TCSADRAIN, old)
                        sys.exit(0)
                    continue
                if ans in ['y', 'Y']:
                    break
                elif ans in ['n', 'N']:
                    print
                    print bcolors.FAIL
                    print "Please read -h to craft a greater understanding in"
                    print "how to configure lake for your project structure"
                    print bcolors.ENDC
                    termios.tcsetattr(fd, termios.TCSADRAIN, old)
                    sys.exit(0)
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
            sys.stdout.write(bcolors.ENDC)
        except KeyboardInterrupt:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
            sys.stdout.write("^C" + bcolors.ENDC)
            print
            raise KeyboardInterrupt
    else:
        try:
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            old[3] = old[3] | termios.ECHO
            tty.setcbreak(sys.stdin)
            sys.stdout.write(bcolors.WARNING +
                             "Press any key to exit " +
                             bcolors.ENDC +
                             bcolors.HEADER)
            sys.stdin.read(1)
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
            sys.stdout.write(bcolors.ENDC)
        except KeyboardInterrupt:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
            sys.stdout.write("^C" + bcolors.ENDC)
            print
            raise KeyboardInterrupt


def less(*args, **kwargs):
    c = "lessc %s %s" % args
    if (not 'compress' in kwargs) or kwargs['compress']:
        c += " --yui-compress"
    shell(c)


def getTerminalSize():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            import struct
            import os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
                                                 '1234'))
        except:
            return None
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (env['LINES'], env['COLUMNS'])
        except:
            cr = (25, 80)
    return int(cr[1] + 2), int(cr[0])


def center(s):
    screen_width, screen_height = getTerminalSize()
    center_width = screen_width
    center_height = screen_height / 2
    lines = s.split('\n')
    clear()
    print "\n" * (center_height -
                  len([line for line in lines if not line.startswith("    ")]))
    for line in lines:
        if not line.startswith("    "):
            s = center_width
            print line.center(s)
        else:
            print line


def get_loader(l):
    width = getTerminalSize()[0] * .8
    loaded = width * l
    bar = ">"  # u"\u2588"
    if loaded == width:
        l = bcolors.OKGREEN
        l += "|" + u"\u2588" + "|"
        l += (bar * int(width))
        l += "|" + u"\u2588" + "|"
        l += bcolors.ENDC
    else:
        to_load = width - loaded
        l = bcolors.OKBLUE
        l += "| | |"
        l += bcolors.ENDC
        l += bcolors.OKGREEN
        l += (bar * int(loaded))
        l += bcolors.ENDC
        l += bcolors.OKBLUE
        l += ("-" * int(to_load))
        l += "| | |"
        l += bcolors.ENDC
    return l


def clear():
    shell("clear")  # print "\n"*getTerminalSize()[1]


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


if __name__ == '__main__':
    try:
        main(**get_vars())
    except KeyboardInterrupt:
        print
        print "bye bye"
        print
