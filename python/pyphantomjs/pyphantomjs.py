#!/usr/bin/env python
'''
  This file is part of the PyPhantomJS project.

  Copyright (C) 2011 James Roe <roejames12@hotmail.com>

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

# automatically convert Qt types by using api 2
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

import sys
import codecs

from PyQt4.QtCore import qInstallMsgHandler
from PyQt4.QtGui import QIcon, QApplication

from plugincontroller import Bunch, do_action
# load plugins if running script directly
if __name__ == '__main__':
    from plugincontroller import load_plugins
    load_plugins()

import resources
from phantom import Phantom
from utils import argParser, MessageHandler, version

# make keyboard interrupt quit program
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

# output unicode safe text
from utils import SafeStreamFilter
sys.stdout = SafeStreamFilter(sys.stdout)
sys.stderr = SafeStreamFilter(sys.stderr)


def parseArgs(args):
    # Handle all command-line options
    p = argParser()
    arg_data = p.parse_known_args(args)
    args = arg_data[0]
    args.script_args = arg_data[1]

    if args.proxy:
        item = args.proxy.split(':')
        if len(item) < 2 or not len(item[1]):
            p.print_help()
            sys.exit(1)
        args.proxy = item

    do_action('ParseArgs', Bunch(locals()))

    if not args.script:
        p.print_help()
        sys.exit(1)

    try:
        with codecs.open(args.script, encoding='utf-8') as script:
            args.script_name = script.name
            args.script = script.read()
    except IOError as (errno, stderr):
        sys.exit('%s: \'%s\'' % (stderr, args.script))

    return args


def main():
    args = parseArgs(sys.argv[1:])

    # register an alternative Message Handler
    messageHandler = MessageHandler(args.verbose)
    qInstallMsgHandler(messageHandler.process)

    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon(':/resources/pyphantomjs-icon.png'))
    app.setApplicationName('PyPhantomJS')
    app.setOrganizationName('Umaclan Development')
    app.setOrganizationDomain('www.umaclan.com')
    app.setApplicationVersion(version)

    phantom = Phantom(args, app)

    do_action('Main', Bunch(locals()))

    if phantom.execute():
        app.exec_()
    return phantom.returnValue()


do_action('PyPhantomJS', Bunch(locals()))


if __name__ == '__main__':
    sys.exit(main())