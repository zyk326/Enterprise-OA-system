import http from './http'

const publishInform = (data) => {
    const path = '/inform/inform'
    return http.post(path, data)
}

export default {
    publishInform
}