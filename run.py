
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

def runopts(args, opts):
  return run([m.format(**opts) for m in args])

def flatten(a):
  b = []
  for c in a: b += c
  return b



bsdir = '../bucklescript/jscomp'

bs_files = 'bin/config_whole_compiler.mli bin/config_whole_compiler.ml bin/js_compiler.mli bin/js_compiler.ml'.split()
bs_files = [join(bsdir, x) for x in bs_files]





pseudo_files = 'lazy.cmi js.cmi js_unsafe.cmi js_re.cmi js_array.cmi js_null.cmi js_undefined.cmi js_internal.cmi js_types.cmi js_null_undefined.cmi js_dict.cmi js_string.cmi'.split()
pseudo_files = flatten([['--file', '{}:/cmis/{}'.format(x, x)] for x in pseudo_files])

opam = '/Users/jared/.opam/4.02.3/lib'

def both():
  # Both together
  both = [
    'ocamlfind',
    'ocamlc',
    '-pp', "refmt --print binary",
    # '-bin-annot',
    # '-g',
    '-w', '-30-40',
    '-I', 'build/src',
    '-I', join(bsdir, 'bin'),
    # '-I', opam + '/ocaml-migrate-parsetree',
    # '-I', opam + '/reason',
    # '-I', opam + '/js_of_ocaml',
    '-package', 'reason,js_of_ocaml,ocaml-migrate-parsetree',
    '-o', 'build/both.byte',
    # '-g',
    '-linkpkg',
    '-impl', '../reason-tools/src/refmt/refmt.re'
  ] + bs_files

  js = [
    'js_of_ocaml',
    '--pretty',
    # '--linkall',
    '+weak.js',
    '+toplevel.js',
    '--disable', 'strict',
    '-o', 'build/both.js',

    bsdir + '/polyfill.js',
    '-I', opam + '/ocaml-migrate-parsetree',
    '-I', bsdir + '/bin',
    '-I', bsdir + '/stdlib',
    '-I', bsdir + '/others/',
    '-I', bsdir + '/runtime/',
    'build/both.byte',
  ] + pseudo_files

  print "both"
  print run(both)
  print "JS"
  # print run(js)


def refmt():

  # refmt
  refmt_byte = [
  'ocamlfind',
  'ocamlc',
  '-pp', "refmt --print binary",
  '-bin-annot', '-g', '-w', '-30-40',
  '-package', 'compiler-libs.common,reason,js_of_ocaml,menhirLib,ocaml-migrate-parsetree',
  '-o', 'build/refmt.byte',
  '-g',
  '-linkpkg',
  '-impl', '../reason-tools/src/refmt/refmt.re'
  ]

  refmt_js = [
    'js_of_ocaml',
    '--pretty',
    '--linkall',
    '+weak.js',
    '+toplevel.js',
    '--disable', 'strict',
    '-o', 'build/refmt.js',
    'build/refmt.byte',
  ]

  print "refmt"
  print run(refmt_byte)
  print "JS"
  print run(refmt_js)

def bs():

  # Just bs
  bs_byte = [
  'ocamlfind',
  'ocamlc',
  '-no-check-prims',
  '-bin-annot',
  '-g',
  '-w', '-30-40',
  '-I', join(bsdir, 'bin'),
  '-o', 'build/bs.byte',
  ] + bs_files

  bs_js = [
    'js_of_ocaml',
    '--toplevel',
    '+weak.js',
    bsdir + '/polyfill.js',
    'build/bs.byte',
    '-I', bsdir + '/bin',
    '-I', bsdir + '/stdlib',
    '-I', bsdir + '/others/',
    '-I', bsdir + '/runtime/',
    '-o', 'build/bs.js',
  ] + pseudo_files

  print "bs"
  print run(bs_byte)
  print "JS"
  print run(bs_js)

both()


