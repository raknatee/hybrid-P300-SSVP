const getJsonFromWSMessage = (msg) => {
    return JSON.parse(msg.data)
}

export { getJsonFromWSMessage }