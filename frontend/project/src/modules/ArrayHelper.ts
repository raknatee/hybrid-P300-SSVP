const repeat = <T extends any[]>(arr:T, n:number):T[] =>  {
    let returnedArr:T[] = [] 


    for (let iN = 0; iN < n; iN++) {
        for (let i = 0; i < arr.length; i++) {
            returnedArr.push(arr[i])
        }

    }
    return returnedArr
}

export { repeat }