module.exports = {
    
    pwa: {
        workboxOptions: {
            skipWaiting: true
        }
    },
    configureWebpack:{
        devServer: {    
            disableHostCheck: true,
            host: '0.0.0.0',
            public: "0.0.0.0",
            port:8080,
           
        }
    },
  
}