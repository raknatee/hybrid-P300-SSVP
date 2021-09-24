const randRange = (min, max) => {
    return Math.random() * (max - min) + min
}
const randInt = (min, max) => {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}


const rangeRandomArray = (range) => {
    let rangeArray = [...Array(range).keys()]

    return shuffle(rangeArray)

}
const shuffle = (array) => {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array
}

export { randRange, randInt, rangeRandomArray }