const repeat = (arr, n) => {
    let returnedArr = []
    for (let iN = 0; iN < n; iN++) {
        for (let i = 0; i < arr.length; i++) {
            returnedArr.push(arr[i])
        }

    }
    return returnedArr
}

export { repeat }