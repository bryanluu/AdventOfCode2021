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
    const errorScore = { ')': 3, ']': 57, '}': 1197, '>': 25137 }
    const completionScore = { ')': 1, ']': 2, '}': 3, '>': 4 }

    let totalErrorScore = 0
    let completionScores = []
    for (let i = 0; i < lines.length; i++) {
      const result = scanForErrors(lines[i])
      if (result.part === 1) {
        totalErrorScore += errorScore[result.error]
      } else {
        if (result.fix.length === 0) continue

        let score = 0
        for (let i = 0; i < result.fix.length; i++) {
          score *= 5
          score += completionScore[result.fix[i]]
        }
        completionScores.push(score)
      }
    }
    completionScores.sort((x, y) => parseInt(x) - parseInt(y))
    const middleScore = completionScores[Math.floor(completionScores.length / 2)]

    console.log('Part 1:', totalErrorScore)
    console.log('Part 2:', middleScore)
  })
}

function scanForErrors (line) {
  const pairing = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<',
  }
  const openBrackets = ['(', '[', '{', '<']
  let stack = []
  const top = () => stack.length - 1
  for (let i = 0; i < line.length; i++) {
    if (openBrackets.includes(line[i])) {
      stack.push(line[i])
    } else {
      if (stack[top()] === pairing[line[i]]) {
        stack.pop()
      } else {
        return { part: 1, error: line[i] }
      }
    }
  }
  let fix = ''
  while (top() >= 0) {
    fix += pairing[stack.pop()]
  }
  return { part: 2, fix: fix }
}

// run if script is run
console.log('Input file: ', filename)
var start = process.hrtime() // Time the solve attempt
solve(filename)
var end = process.hrtime(start)
console.log('solve(%s) took: %ds %dms', filename, end[0], end[1] / 1000000)
