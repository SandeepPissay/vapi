# Copyright 2013 VMware, Inc.  All rights reserved. -- VMware Confidential

"""
manifest gradle build bootstrap.
"""

import subprocess
import os
import sys
import platform

# don't need any pycs
sys.dont_write_bytecode = True

def useCmdArgs(args, env, pos_args=[]):
   target = ''

   for a in args[1:]:
      try:
         key, val = a.split('=', 1)
      except:
         target = a
         pos_args.append(a)
         continue

      if a.startswith('-'):
         pos_args.append(a)

      env[key] = val

   return target


def execWithEnv(cmd, env):
   _env = {}
   for k, v in env.iteritems():
      _env[k] = str(v)

   print 'execWithEnv:', cmd
   print 'with Env:', _env

   sys.stdout.flush()
   subprocess.check_call(cmd, env=_env)


env = {
      #'BUILD_NUMBER' : '0',
      }

# needed on windows
env['SystemRoot'] = os.environ.get('SYSTEMROOT', '')
env['PROCESSOR_ARCHITECTURE'] = os.environ.get('PROCESSOR_ARCHITECTURE', '')
env['TMP'] = os.environ.get('TMP', '')
env['TEMP'] = os.environ.get('TEMP', '')

env['TCROOT'] = os.environ.get('TCROOT', '/build/toolchain')

# main

pos_args = []

target = useCmdArgs(sys.argv, env, pos_args)
env['TARGET'] = target

gradle_bin = os.path.join(env['GRADLE_HOME'], 'bin', 'gradle')

# debug
#print 'system environment: %s' % os.environ


print 'Env:'
for key, val in sorted(env.iteritems()):
   print '%s=%s' % (key, val)

print 'Positional Args: %s' % pos_args

print 'gradle_bin = %s' % gradle_bin
print 'target = [%s]' % target

cmd = [gradle_bin]
cmd.extend(pos_args)

execWithEnv(cmd, env)
