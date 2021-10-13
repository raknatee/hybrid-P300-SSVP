const getSizeW = (percentage) => {
    return getSize(percentage, 'w')

}
const getSizeH = (percentage) => {
    return getSize(percentage, 'h')
}

const getSize = (percentage, site) => {
    if (site == "w") {
        return percentage * window.innerWidth
    }
    if (site == "h") {
        return percentage * window.innerHeight
    }
}
export { getSizeW, getSizeH }