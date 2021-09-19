const randRange = (min, max) => {
    return Math.random() * (max - min) + min
}
const randInt = (min, max) => {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

export { randRange, randInt }