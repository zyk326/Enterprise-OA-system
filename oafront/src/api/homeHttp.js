import http from './http'

const getDepartmentStaffCount = () => {
    const path = 'home/department/staff/count'
    return http.get(path)
}

const getLatestInforms = () => {
    const path = '/home/latest/inform'
    return http.get(path)
}

const getLatesAbsents = () => {
    const path = '/home/latest/absent'
    return http.get(path)
}

export default{
    getDepartmentStaffCount,
    getLatestInforms,
    getLatesAbsents
}