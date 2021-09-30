const randRange = (min, max) => {
    return Math.random() * (max - min) + min
}
const randInt = (min, max) => {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

const rangeArray = (range) => {
    return [...Array(range).keys()]
}

const rangeRandomArray = (range) => {

    return shuffle(rangeArray(range))

}
const shuffle = (array) => {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array
}

const choise = (array) => {
    return array[Math.floor(Math.random() * array.length)]
}

// const checkerboard = (range) => {
//     let rArr = rangeArray(range)
//     let oddArr = shuffle(rArr.filter((e) => e % 2 == 1))
//     let evenArr = shuffle(rArr.filter((e) => e % 2 == 0))

//     const merge = (arr1, arr2) => {
//         let returned = []
//         let arrs = [arr1, arr2]
//         let pointer = 0
//         let mergeN = arr1.length + arr2.length
//         for (let i = 0; i < mergeN; i++) {
//             returned.push(arrs[pointer].pop())
//             pointer = (pointer + 1) % 2
//         }
//         return returned
//     }
//     let returned = merge(oddArr, evenArr)
//     console.log(returned)
//     return returned

// }
export { randRange, randInt, rangeRandomArray, choise, rangeArray }