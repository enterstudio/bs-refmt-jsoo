// require('./build/bs.js')
var refmt = require('./build/both.js')
console.log(refmt)
const src = 'Js.log "hi"'
var ast = refmt.refmt_to_bs(src)
let res = refmt.refmt(src, 'RE', 'implementation', 'ML')
console.log(res)

try {
  console.log(ocaml.compile(res[1]))
} catch (e) {
  console.log('failed')
}

try {
  console.log(ocaml.from_ast(ast, res[1]))
} catch (e) {
  console.log('failed')
}
