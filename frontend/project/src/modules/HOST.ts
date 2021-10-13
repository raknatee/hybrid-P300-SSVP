const HOST_CONFIG = {
    ML_SERVER_HOSTNAME: 'localhost',
    ML_SERVER_PORT: 8000

}
const getSecureProtocol = ():string =>{
    if(location.protocol === "https:"){
        return "s"
    }
    else{
        return ""
    }
}
export {HOST_CONFIG,getSecureProtocol}