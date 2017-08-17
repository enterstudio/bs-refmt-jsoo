const requirejs = require('requirejs')
requirejs.config({
  nodeRequire: require
})
var x = require('../reason-tools/_build/refmt/app.js')
var y = require('./bsjs.js')
requirejs(['../bucklescript/docs/js-demo/stdlib/list.js'], (result) => {
  console.log('loaded')
console.log('hi')
var res = `let x = 10;
  print_endline "hi";
  List.iter
  (fun x => print_endline x)
  ["hi", "ho"];
  `
  var mls =     `
  let () = List.iter
  (fun x -> print_endline x)
  ["hi"; "ho"]`
  const src = x.refmt(res, "RE", "implementation", "ML")
  console.log(src)
  // console.log(global.ocaml.from_ast(x.refmt_to_bs(src), x.refmt(src, "RE", "implementation", "ML")[1]))
  console.log(global.ocaml.compile(mls))
  console.log(global.ocaml.compile(src[1]))
})

// global.ocamlh
