
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


rtdir = '../reason-tools'
builddir = 'build'

unlinked = builddir + '/reasonToolsRefmt'
linked = builddir + '/reasonTools.byte'

bsdir = '../bucklescript/jscomp'
byte = 'build/bsjs.byte'

formatopts = {
  'rtdir': rtdir,
  'unlinked': unlinked,
  'linked': linked,
  'builddir': builddir,
}

first = [
'ocamlfind',
'ocamlc',
'-pp', "refmt --print binary",
'-bin-annot', '-g', '-w', '-30-40',
'-I', '{builddir}/src',
'-package', 'compiler-libs.common,reason,js_of_ocaml,menhirLib,ocaml-migrate-parsetree',
'-o', unlinked,
'-c',
'-impl', '{rtdir}/src/refmt/refmt.re'
]

bs_files = 'bin/config_whole_compiler.mli bin/config_whole_compiler.ml bin/js_compiler.mli bin/js_compiler.ml'.split()
bs_files = [join(bsdir, x) for x in bs_files]

bs_command = [
'ocamlc.opt',
'-w', '-30-40',
'-no-check-prims',
'-I', join(bsdir, 'bin')
] + bs_files + ['-o', byte]

# doubles
both_together = [
'ocamlfind',
'ocamlc',
'-pp', "refmt --print binary",
'-bin-annot', '-g',
'-no-check-prims',
'-w', '-30-40',
'-I', '{builddir}/src',
'-package', 'compiler-libs.common,reason,js_of_ocaml,menhirLib,ocaml-migrate-parsetree',
'-o', unlinked,
'-c',
'-impl', '{rtdir}/src/refmt/refmt.re'
] + bs_files










