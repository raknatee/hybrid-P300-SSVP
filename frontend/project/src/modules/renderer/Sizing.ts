const getSizeW = (percentage:number):number => {
    return getSize(percentage, 'w')

}
const getSizeH = (percentage:number):number => {
    return getSize(percentage, 'h')
}

const getSize = (percentage:number, site:string):number => {
    if (site == "w") {
        return percentage * window.innerWidth
    }
    if (site == "h") {
        return percentage * window.innerHeight
    }
    return 0
}
export { getSizeW, getSizeH }