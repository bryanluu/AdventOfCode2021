#!/usr/bin/node
var filename = process.argv.length > 2 ? process.argv[2] : 'input.txt' // Input file

// Solves the challenge with input filename
function solve (filename) {
  fs = require('fs')
  fs.readFile(filename, 'utf8', function(err, data) {
    if (err) {
      return console.log(err)
    }

    const lines = data.split("\n")

    const { paper, instructions } = parseManual(lines)

    for (let i = 0; i < instructions.length; i++) {
      const line = parseInstruction(instructions[i])
      foldAlongLine(paper, line)
      if (i === 0) {
        console.log(`Part 1: ${Object.keys(paper).length}`)
      }
    }
    displayPaper(paper)
  })
}

function parseManual(lines) {
  let paper = {}
  let instructions = []
  let section = 1
  for (let i = 0; i < lines.length; i++) {
    let line = lines[i]
    if (line === '') {
      section++
      continue
    }

    if (section === 1) {
      paper[line] = true
    } else {
      instructions.push(line)
    }
  }
  return { paper, instructions }
}

function parseCoord(coordStr) {
  const coord = coordStr.split(',')
  return { x: parseInt(coord[0]), y: parseInt(coord[1]) }
}

function toCoordStr(x, y) {
  return `${x},${y}`
}

function parseInstruction(instruction) {
  let line = instruction.slice(11).split('=')
  return { along: line[0], at: parseInt(line[1]) }
}

function foldAlongLine(paper, line) {
  let dots = Object.keys(paper)
  console.log(line)

  for (let i = 0; i < dots.length; i++) {
    let dot = parseCoord(dots[i])
    if (line.along === 'x') {
      if (dot.x > line.at) {
        let offset = dot.x - line.at
        paper[toCoordStr(line.at - offset, dot.y)] = true
        delete paper[dots[i]]
      }
    } else {
      if (dot.y > line.at) {
        let offset = dot.y - line.at
        paper[toCoordStr(dot.x, line.at - offset)] = true
        delete paper[dots[i]]
      }
    }
  }
}

function displayPaper(paper) {
  let dots = Object.keys(paper).map(coord => parseCoord(coord))

  dots.sort((dot1, dot2) => dot2.x - dot1.x)
  const maxX = dots[0].x
  dots.sort((dot1, dot2) => dot2.y - dot1.y)
  const maxY = dots[0].y


  let output = ""
  for (let y = 0; y <= maxY; y++) {
    for (let x = 0; x <= maxX; x++) {
      output += (paper[toCoordStr(x, y)] ? '#' : ' ')
    }
    output += '\n'
  }
  console.log(output)
}

// run if script is run
console.log('Input file: ', filename)
var start = process.hrtime() // Time the solve attempt
solve(filename)
var end = process.hrtime(start)
console.log('solve(%s) took: %ds %dms', filename, end[0], end[1] / 1000000)
