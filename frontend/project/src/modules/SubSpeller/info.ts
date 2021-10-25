const subSpellerData = [
    ['ภ', 'ถ', '-ุ', '-ู', 'ๆ', 'ไ', 'ฎ', ' ำ', 'ฑ'],
    ['-ึ', 'ค', 'พ', 'ธ', 'ะ', '-ํ', '-ั', '-๊', '-ี', ],
    ['ต', 'จ', 'ข', 'ณ', 'ฯ', 'ญ', 'ร', 'น', 'ย'],
    ['ฐ', 'ช', 'ฅ', 'บ', 'ล', 'ฃ', '.', 'ง', ','],
    ['ฤ', 'ฆ', 'ฏ', 'ฟ', 'ห', '(', ')', 'ผ', 'ป'],
    ['ก', 'โ', 'ฌ', 'ด', 'เ', 'ฉ', 'ฮ', 'แ', 'อ'],
    ['-็', '-๋', 'ษ', '-้', '-่', 'า', '-ฺ', '-ิ', '-์'],
    ['ฒ', 'ศ', 'ซ', 'ส', 'ว', 'ฬ', '-ื', 'ท', 'ม'],
    null,
    null, ['ฦ', 'ฝ', 'ใ', 'A','B','C','D','0','BS'],
    ['7', '8', '9', '4', '5', '6', '1', '2', '3']
]

class fp{
    freq:number
    phare:number

	constructor(freq:number,phare:number) {
        this.freq = freq
        this.phare = phare
	}
   
}

const wavesData = [
    new fp(12.4, 0),
    new fp(12.6, .35),
    new fp(12.8, .7),
    new fp(13, 1.05),
    new fp(13.2, 1.4),
    new fp(13.4, 1.75),
    new fp(13.6, .1),
    new fp(13.8, .45),
    null, null,
    new fp(14, .8),
    new fp(14.2, 1.15),
]
// const wavesData = [
//     new fp(8, 0),
//     new fp(8, 0),
//     new fp(8, 0),
//     new fp(8, 0),
//     new fp(8, 0),
//     new fp(8, 0),
//     new fp(8, 0),
//     new fp(8, 0),
//     null, null,
//     new fp(8, 0),
//     new fp(8, 0),
// ]
export {
    subSpellerData,
    wavesData
}