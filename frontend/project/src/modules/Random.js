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

const checkerboard = (range) => {
    let AllArr = extractWhiteBlack(rangeArray(range))

    
    let whiteArr = shuffle(AllArr[0])
    let blackArr = shuffle(AllArr[1])

    return [...whiteArr,...blackArr]

   
    

}

const extractWhiteBlack = (arr) =>{
    let whiteBlackArrs = [[],[]]
    let pointer = 0
    for(let i =0;i<arr.length;i++){
        whiteBlackArrs[pointer].push(arr[i])
        pointer = (pointer+1)%2
    }
    return whiteBlackArrs

}
export { randRange, randInt, rangeRandomArray, choise, rangeArray,checkerboard }