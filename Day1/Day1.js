#!/usr/bin/node
var filename = process.argv.length > 2 ? process.argv[2] : 'input.txt' // Input file

// Solves the challenge with input filename
function solve (filename) {
  fs = require('fs')
  fs.readFile(filename, 'utf8', function (err, data) {
    if (err) {
      return console.log(err)
    }

    const lines = data.split('\n')
    let increasing = 0

    let prevSum = parseInt(lines[0])
    let currSum = 0
    let increasingSum = 0
    for (let i = 1; i < lines.length; i++) {
      let prev = parseInt(lines[i - 1])
      let curr = parseInt(lines[i])
      if (curr > prev) increasing++

      if (i >= 3) {
        currSum = prevSum - parseInt(lines[i - 3]) + curr
        if (currSum > prevSum) increasingSum++
        prevSum = currSum
      } else {
        prevSum += curr
      }
    }

    console.log('Part 1:', increasing)
    console.log('Part 2:', increasingSum)
  })
}

// run if script is run
console.log('Input file: ', filename)
var start = process.hrtime() // Time the solve attempt
solve(filename)
var end = process.hrtime(start)
console.log('solve(%s) took: %ds %dms', filename, end[0], end[1] / 1000000)
