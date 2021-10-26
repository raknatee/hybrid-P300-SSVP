class SinWave {
    freq:number
    phare:number
    constructor(freq:number, phare:number) {
        this.freq = freq
        this.phare = phare
    }
    _get_y_t(time:number):number {
        return Math.sin(2* Math.PI * this.freq * time + this.phare)
    }
    getYNow():number {
        return this._get_y_t(getNow())
    }
    isUp():boolean {
        return this.isUpByTime(getNow())
    }
    isUpByTime(timenow:number):boolean {

        return Math.abs(this._get_y_t(timenow) - 1) < 1e-1
    }
}
const getNow = ():number => {
    return Date.now() / 1000
}
export { SinWave, getNow }