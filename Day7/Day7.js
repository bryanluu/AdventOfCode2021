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
    const positions = lines[0]
      .split(',')
      .map(x => parseInt(x))
      .sort()
    const positionMap = {}

    for (let i = 0; i < positions.length; i++) {
      if (positionMap[positions[i]] === undefined) {
        positionMap[positions[i]] = 0
      }
      positionMap[positions[i]]++
    }

    const { partOne, partTwo } = getOptimumPositions(positions)

    console.log(`Part 1: ${partOne.optimum} @ ${partOne.bestPosition}`)
    console.log(`Part 2: ${partTwo.optimum} @ ${partTwo.bestPosition}`)
  })
}

function getOptimumPositions (positions) {
  let partOneOptimum = null
  let partOneBestPosition = null
  let partTwoOptimum = null
  let partTwoBestPosition = null
  for (let chosen = positions[0]; chosen <= positions[positions.length - 1]; chosen++) {
    let partOneDistance = 0
    let partTwoDistance = 0
    for (let i = 0; i < positions.length; i++) {
      let dx = Math.abs(positions[i] - chosen)
      partOneDistance += dx
      partTwoDistance += (dx * (dx + 1)) / 2
    }
    if (partOneOptimum === null || partOneDistance < partOneOptimum) {
      partOneOptimum = partOneDistance
      partOneBestPosition = chosen
    }
    if (partTwoOptimum === null || partTwoDistance < partTwoOptimum) {
      partTwoOptimum = partTwoDistance
      partTwoBestPosition = chosen
    }
  }
  return {
    partOne: { optimum: partOneOptimum, bestPosition: partOneBestPosition },
    partTwo: { optimum: partTwoOptimum, bestPosition: partTwoBestPosition },
  }
}

// run if script is run
console.log('Input file: ', filename)
var start = process.hrtime() // Time the solve attempt
solve(filename)
var end = process.hrtime(start)
console.log('solve(%s) took: %ds %dms', filename, end[0], end[1] / 1000000)
