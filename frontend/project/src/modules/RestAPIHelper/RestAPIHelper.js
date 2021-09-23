const restAPIGet = async(path, onFailure = () => {}) => {
    let resp = await fetch(path, { method: "GET" })
    if (resp.status === 200) {
        let jsonData = await resp.json()
        return jsonData
    } else {
        onFailure(resp)
    }
}
export { restAPIGet }