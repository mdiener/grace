#!/usr/bin/env python

from grace.management import execute_commands
import sys

args = sys.argv
execute_commands(args[1:])
