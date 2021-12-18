#!/usr/bin/node
var filename = process.argv.length > 2 ? process.argv[2] : 'input.txt' // Input file

// Solves the challenge with input filename
function solve (filename) {
  fs = require('fs')
  fs.readFile(filename, 'utf-8', (err, data) => {
    if (err) {
      return console.log(err)
    }

    const code = data.trim()
    const packet = convertHexToBinary(code)
    const tree = parsePacket(packet)

    console.log('Part 1:', sumVersions(tree))
    console.log('Part 2:', processTree(tree))
  })
}

function parsePacket (packet) {
  const LITERAL_VALUE = 4
  const version = Number(convertBinaryToDecimal(packet.slice(0, 3)))
  const packetType = Number(convertBinaryToDecimal(packet.slice(3, 6)))
  const leftover = packet.slice(6)
  let output = { version, packetType, value: null, children: [] }
  if (packetType === LITERAL_VALUE) {
    output = { ...output, ...parseLiteralValue(leftover) }
  } else {
    output = { ...output, ...parseOperator(leftover) }
  }
  return output
}

function parseLiteralValue (bits) {
  const END_GROUP = '0'
  let value = ''
  for (let i = 0; i < bits.length; i += 5) {
    value += bits.slice(i + 1, i + 5)
    if (bits[i] === END_GROUP) {
      const dec = convertBinaryToDecimal(value)
      const leftover = bits.slice(i + 5)
      return {
        value: dec,
        leftover: leftover,
      }
    }
  }
}

function parseOperator (bits) {
  const lengthTypeId = bits[0]
  let children = []
  let leftover = ''
  if (lengthTypeId === '0') {
    const length = Number(convertBinaryToDecimal(bits.slice(1, 16)))
    leftover = bits.slice(16, 16 + length)

    while (leftover.length > 0) {
      const child = parsePacket(leftover)
      leftover = child.leftover
      children.push(child)
    }
    leftover = bits.slice(16 + length)
  } else {
    const length = convertBinaryToDecimal(bits.slice(1, 12))
    leftover = bits.slice(12)
    for (let i = 0; i < length; i++) {
      const child = parsePacket(leftover)
      leftover = child.leftover
      children.push(child)
    }
  }
  return {
    lengthTypeId,
    leftover,
    children,
  }
}

function convertHexToBinary (code) {
  hexToBin = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
  }
  output = ''
  for (let i = 0; i < code.length; i++) {
    output += hexToBin[code[i]]
  }
  return output
}

function convertBinaryToDecimal (bits) {
  dec = 0n
  for (let i = 0; i < bits.length; i++) {
    dec *= 2n

    if (bits[i] === '1') dec++
  }
  return dec
}

function sumVersions (tree) {
  let stack = [tree]
  let sum = 0
  while (stack.length > 0) {
    let curr = stack.pop()
    sum += curr.version
    curr.children.forEach(child => {
      stack.push(child)
    })
  }
  return sum
}

function processTree (tree) {
  if (tree.value !== null) return tree.value
  const SUM = 0
  const PRODUCT = 1
  const MIN = 2
  const MAX = 3
  const GREATER_THAN = 5
  const LESS_THAN = 6
  const EQUAL = 7
  switch (tree.packetType) {
    case SUM:
      processSumTree(tree)
      break
    case PRODUCT:
      processProductTree(tree)
      break
    case MIN:
      processMinTree(tree)
      break
    case MAX:
      processMaxTree(tree)
      break
    case GREATER_THAN:
      processGreaterThanTree(tree)
      break
    case LESS_THAN:
      processLessThanTree(tree)
      break
    case EQUAL:
      processEqualTree(tree)
      break
  }
  return tree.value
}

function processSumTree (tree) {
  let sum = 0n
  tree.children.forEach(child => {
    processTree(child)
    sum += child.value
  })
  tree.value = sum
}

function processProductTree (tree) {
  let prod = 1n
  tree.children.forEach(child => {
    processTree(child)
    prod *= child.value
  })
  tree.value = prod
}

function processMinTree (tree) {
  let min = tree.value
  tree.children.forEach(child => {
    processTree(child)
    if (min === null || child.value < min) min = child.value
  })
  tree.value = min
}

function processMaxTree (tree) {
  let max = tree.value
  tree.children.forEach(child => {
    processTree(child)
    if (max === null || child.value > max) max = child.value
  })
  tree.value = max
}

function processGreaterThanTree (tree) {
  tree.children.forEach(child => {
    processTree(child)
  })
  tree.value = tree.children[0].value > tree.children[1].value ? 1n : 0n
}

function processLessThanTree (tree) {
  tree.children.forEach(child => {
    processTree(child)
  })
  tree.value = tree.children[0].value < tree.children[1].value ? 1n : 0n
}

function processEqualTree (tree) {
  tree.children.forEach(child => {
    processTree(child)
  })
  tree.value = tree.children[0].value === tree.children[1].value ? 1n : 0n
}

function printPacketTree (tree) {
  let stack = [{ data: tree, level: 0 }]
  while (stack.length > 0) {
    let curr = stack.pop()
    console.log(
      ' '.repeat(curr.level),
      curr.data.version,
      curr.data.packetType,
      curr.data.value
    )
    curr.data.children.forEach(child => {
      stack.push({ data: child, level: curr.level + 1 })
    })
  }
}

// run if script is run
console.log('Input file: ', filename)
var start = process.hrtime() // Time the solve attempt
solve(filename)
var end = process.hrtime(start)
console.log('solve(%s) took: %ds %dms', filename, end[0], end[1] / 1000000)
