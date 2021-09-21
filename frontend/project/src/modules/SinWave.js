class SinWave {
    constructor(freq, phare) {
        this.freq = freq
        this.phare = phare
    }
    _get_y_t(time) {
        return Math.sin(2 * Math.PI * this.freq * time + this.phare)
    }
    getYNow() {
        return this._get_y_t(getNow())
    }
    isUp() {
        return this.isUpByTime(getNow())
    }
    isUpByTime(timenow) {

        return Math.abs(this._get_y_t(timenow) - 1) < 1e-1
    }
}
const getNow = () => {
    return Date.now() / 1000
}
export { SinWave, getNow }