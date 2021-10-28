function sleep(ms:number):Promise<void>{
    return new Promise(resolve => setTimeout(resolve, ms));
}
const getNow = ():number => {
    return Date.now() / 1000
    // return performance.now() / 1000
}
const getPerformanceNow = ():number =>{
    return performance.now() / 1000

}
export {sleep,getNow,getPerformanceNow}