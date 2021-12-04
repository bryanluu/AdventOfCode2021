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
    let firstScore = 0
    let lastScore = 0

    for(let i = 0; i < drawn.length; i++) {
      const num = drawn[i]
      markNumber(num, boards)
      winners = bingo(boards)
      if (winners.length > 0) {
        if(firstScore === 0) {
          firstScore = sumUnmarked(winners[0]) * parseInt(num)
        }
        lastScore = sumUnmarked(winners.at(-1)) * parseInt(num)
      }
    }

    console.log(`Part 1: ${firstScore}`)
    console.log(`Part 2: ${lastScore}`)
  })
}

function populateBoards(lines) {
  const boards = []

  const spacer = /^ *$/
  let board = []
  let row = 0
  for(let i = 0; i < lines.length; i++) {
    if (spacer.test(lines[i])) {
      if (board.length > 0) {
        board[0][0].won = false
        boards.push(board)
      }
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

function markNumber(number, boards) {
  for(let i = 0; i < boards.length; i++) {
    if (boards[i][0][0].won) continue

    for(let row = 0; row < 5; row++) {
      for(let col = 0; col < 5; col++) {
        if (boards[i][row][col].tile === number) boards[i][row][col].hit = true
      }
    }
  }
}

function bingo(boards) {
  const winners = []
  for(let i = 0; i < boards.length; i++) {
    const board = boards[i]
    if (board[0][0].won) continue

    const colHit = [true, true, true, true, true]
    for(let row = 0; row < 5; row++) {
      let rowHit = true
      for(let col = 0; col < 5; col++) {
        let hit = board[row][col].hit
        rowHit = rowHit && hit
        colHit[col] = colHit[col] && hit
      }
      if (rowHit) {
        board[0][0].won = true
        break
      }
    }
    if (colHit.some(hit => hit)) {
      board[0][0].won = true
    }
    if (board[0][0].won) {
      winners.push(board)
    }
  }

  return winners
}

function sumUnmarked(board) {
  let sum = 0
  for(let row = 0; row < 5; row++) {
    for(let col = 0; col < 5; col++) {
      if (!board[row][col].hit) sum += parseInt(board[row][col].tile)
    }
  }
  return sum
}

// run if script is run
console.log('Input file: ', filename)
var start = process.hrtime() // Time the solve attempt
solve(filename)
var end = process.hrtime(start)
console.log('solve(%s) took: %ds %dms', filename, end[0], end[1] / 1000000)
