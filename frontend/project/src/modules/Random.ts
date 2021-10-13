const randRange = (min:number, max:number):number => {
    return Math.random() * (max - min) + min
}
const randInt = (min:number, max:number):number => {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

const rangeArray = (range:number):number[] => {
    return [...Array(range).keys()]
}

const rangeRandomArray = (range:number):number[] => {

    return shuffle(rangeArray(range))

}
const shuffle = <T>(array:T[]):T[] => {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array
}

const choise = <T>(array:T[]):T => {
    return array[Math.floor(Math.random() * array.length)]
}

const checkerboard = (range:number):number[] => {
    const AllArr = extractWhiteBlack(rangeArray(range))

    
    const whiteArr = shuffle(AllArr[0])
    const blackArr = shuffle(AllArr[1])

    return [...whiteArr,...blackArr]

   
    

}

const extractWhiteBlack = (arr:number[]):number[][] =>{
    const whiteBlackArrs:number[][] = [[],[]]
    let pointer = 0
    for(let i =0;i<arr.length;i++){
        whiteBlackArrs[pointer].push(arr[i])
        pointer = (pointer+1)%2
    }
    return whiteBlackArrs

}
export { randRange, randInt, rangeRandomArray, choise, rangeArray,checkerboard }