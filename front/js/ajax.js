const axios = require("axios")
const url = require("url")
const baseUrl = "/pastebin"
const backendPrefix = "/pastebinBackend"//后端接口形如backendPrefix/api/xxxx
const locationStruct = url.parse(location.href)
/*
开发环境下，url格式为localhost:8080/xxxx
生产环境下，url格式为localhost/appName/xxxx
前端一律采用相对路径，后端一律采用绝对路径
后端接口一定形如/api/xxx
本程序关键在于对get请求和post请求的url进行改写
* 如果是开发模式，直接请求/api/xxxx即可，
* 如果是生产模式，需要在url前面加上后端服务的前缀
*/
const isProduction = locationStruct.path.startsWith(baseUrl)
module.exports = {
    get(url, ...args) {
        return new Promise((resolve, reject) => {
            if (isProduction) {
                url = backendPrefix + url
            }
            axios
                .get(url, ...args)
                .then(resp => {
                    resolve(resp)
                })
                .catch(err => {
                    reject(err)
                })
        })
    },
    post(url, ...args) {
        return new Promise((resolve, reject) => {
            if (isProduction) {
                url = backendPrefix + url
            }
            axios
                .post(url, ...args)
                .then(resp => {
                    resolve(resp)
                })
                .catch(err => {
                    reject(err)
                })
        })
    },
}