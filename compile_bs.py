
import os
from os.path import join
import subprocess

def run(cmd):
  print "running", " ".join(cmd)
  try:
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT,
        env=os.environ)
  except Exception as e:
    print 'err', e
    if hasattr(e, 'output'):
      return e.output
    return e.message

def flatten(a):
  b = []
  for c in a: b += c
  return b




bsdir = '../bucklescript/jscomp'
byte = 'build/bsjs.byte'

bs_files = 'bin/config_whole_compiler.mli bin/config_whole_compiler.ml bin/js_compiler.mli bin/js_compiler.ml'.split()
bs_files = [join(bsdir, x) for x in bs_files]
bs_command = ['ocamlc.opt', '-w', '-30-40', '-no-check-prims', '-I', join(bsdir, 'bin')] + bs_files + ['-o', byte]

print "ocamlc"
print run(bs_command)



outjs = 'build/bsjs.js'
pseudo_files = 'lazy.cmi js.cmi js_unsafe.cmi js_re.cmi js_array.cmi js_null.cmi js_undefined.cmi js_internal.cmi js_types.cmi js_null_undefined.cmi js_dict.cmi js_string.cmi'.split()
jsc = [
  'js_of_ocaml',
  '--toplevel',
  '+weak.js',
  '{bsdir}/polyfill.js',
  '{byte}',
  '-I', '{bsdir}/bin',
  '-I', '{bsdir}/stdlib',
  '-I', '{bsdir}/others/',
  '-I', '{bsdir}/runtime/',
]
formatargs = {'bsdir': bsdir, 'byte': byte}
jsc = [arg.format(**formatargs) for arg in jsc]

jsc_command = jsc + flatten([['--file', '{}:/cmis/{}'.format(x, x)] for x in pseudo_files]) + ['-o', outjs]



print "jsoo"
print run(jsc_command)
