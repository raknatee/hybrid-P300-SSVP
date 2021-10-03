const restAPIGet = async(path, onFailure = () => {}) => {
    let resp = await fetch(path, { method: "GET" })
    if (resp.status === 200) {
        let jsonData = await resp.json()
        return jsonData
    } else {
        onFailure(resp)
    }
}

const restAPIMethod = async(path, method, body, onSuccess = () => {}, onFailure = () => {}) => {
    let resp = await fetch(path, {
        method,
        headers: {
            'Content-Type': 'application/json'
        },
        "body": JSON.stringify(body)
    })
    if (resp.status === 200) {
        let jsonData = await resp.json()
        onSuccess(jsonData)
    } else {
        onFailure(resp)
    }
}
const restAPIPost = async(path, body, onSuccess = () => {}, onFailure = () => {}) => {
    await restAPIMethod(path, "POST", body, onSuccess, onFailure)
}
export { restAPIGet, restAPIPost }