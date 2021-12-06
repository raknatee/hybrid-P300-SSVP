class fp{
    freq:number
    phare:number

    constructor(freq:number,phare:number) {
        this.freq = freq
        this.phare = phare
    }
   
}


// const subSpellerData = [
//     ['ภ', 'ถ', '-ุ', '-ู', 'ๆ', 'ไ', 'ฎ', ' ำ', 'ฑ'],
//     ['-ึ', 'ค', 'พ', 'ธ', 'ะ', '-ํ', '-ั', '-๊', '-ี', ],
//     ['ต', 'จ', 'ข', 'ณ', 'ฯ', 'ญ', 'ร', 'น', 'ย'],
//     ['ฐ', 'ช', 'ฅ', 'บ', 'ล', 'ฃ', '.', 'ง', ','],
//     ['ฤ', 'ฆ', 'ฏ', 'ฟ', 'ห', '(', ')', 'ผ', 'ป'],
//     ['ก', 'โ', 'ฌ', 'ด', 'เ', 'ฉ', 'ฮ', 'แ', 'อ'],
//     ['-็', '-๋', 'ษ', '-้', '-่', 'า', '-ฺ', '-ิ', '-์'],
//     ['ฒ', 'ศ', 'ซ', 'ส', 'ว', 'ฬ', '-ื', 'ท', 'ม'],
//     null,
//     null, ['ฦ', 'ฝ', 'ใ', 'A','B','C','D','0','BS'],
//     ['7', '8', '9', '4', '5', '6', '1', '2', '3']
// ]


// const wavesData = [
//     new fp(6, 0),
//     new fp(6.6, .5),
//     new fp(7.2, 0),
//     new fp(7.8, .5),
//     new fp(8.4, 0),
//     new fp(9, .5),
//     new fp(9.6, 0),
//     new fp(10.2, .5),
//     null, null,
//     new fp(10.8, 0),
//     new fp(11.4, .5),
// ]


const subSpellerData = [
    ['ภ', 'ถ', '-ุ', '-ู', 'ๆ', 'ไ', 'ฎ', ' ำ', 'ฑ'],
    ['-ึ', 'ค', 'พ', 'ธ', 'ะ', '-ํ', '-ั', '-๊', '-ี', ],
    ['ต', 'จ', 'ข', 'ณ', 'ฯ', 'ญ', 'ร', 'น', 'ย'],
    ['ฐ', 'ช', 'ฅ', 'บ', 'ล', 'ฃ', '.', 'ง', ','],
    null,
    null,
    null,
    null,
    null,
    null, null,
    null
]


const wavesData = [
    new fp(7, 0),
    new fp(9, 0),
    new fp(11, 0),
    new fp(13, 0),
    null,
    null,
    null,
    null, null,
    null,
    null,
]

// const wavesData = [
//     new fp(12.4, 0),
//     new fp(12.6, .35),
//     new fp(12.8, .7),
//     new fp(13, 1.05),
//     new fp(13.2, 1.4),
//     new fp(13.4, 1.75),
//     new fp(13.6, .1),
//     new fp(13.8, .45),
//     null, null,
//     new fp(14, .8),
//     new fp(14.2, 1.15),
// ]

// const fixed_freq = 6
// const wavesData = [
//     new fp(fixed_freq, 0),
//     new fp(fixed_freq,0),
//     new fp(fixed_freq, 0),
//     new fp(fixed_freq, 0),
//     new fp(fixed_freq, 0),
//     new fp(fixed_freq, 0),
//     new fp(fixed_freq, 0),
//     new fp(fixed_freq, 0),
//     null, null,
//     new fp(fixed_freq, 0),
//     new fp(fixed_freq, 0),
// ]

// const subSpellerData = [
//     null,
//     null,
//     ['พ'],
//     null,
//     ['ป'],
//     null,
//    null,
//     ['ท'],
//     null,
//     null, null,
//    null
// ]


// const wavesData = [
//     null,
//     null,
//     new fp(6, 0),
//     null,
//     new fp(10,0),
//     null,
//    null,
    
//     new fp(15,0),
//     null, null,
//    null,null
// ]

export {
    subSpellerData,
    wavesData
}