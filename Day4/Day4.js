#!/usr/bin/node
var filename = process.argv.length > 2 ? process.argv[2] : 'input.txt' // Input file
var ld = require('lodash')

// Solves the challenge with input filename
function solve (filename) {
  fs = require('fs')
  fs.readFile(filename, 'utf8', function (err, data) {
    if (err) {
      return console.log(err)
    }

    const lines = data.split('\n')

    const drawn = lines[0].split(',')
    const boards = populateBoards(lines.slice(2))
  })
}

function populateBoards(lines) {
  const boards = []

  const spacer = /^\w*$/
  let board = []
  let row = 0
  for(let i = 0; i < lines.length; i++) {
    if (spacer.test(lines[i])) {
      if (board.length > 0) boards.push(board)
      board = []
      row = 0
      continue
    }

    const rowTiles = ld.compact(lines[i].split(' '))
    board[row] = []
    for(let col = 0; col < 5; col++) {
      const tile = rowTiles[col]
      board[row].push({tile: tile, hit: false})
    }
    row++
  }

  return boards
}

// run if script is run
console.log('Input file: ', filename)
var start = process.hrtime() // Time the solve attempt
solve(filename)
var end = process.hrtime(start)
console.log('solve(%s) took: %ds %dms', filename, end[0], end[1] / 1000000)
