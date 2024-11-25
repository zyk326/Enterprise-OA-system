import axios from "axios";
import { useAuthStore } from "@/stores/auth";

class Http {
  constructor() {
    this.instance = axios.create({
      baseURL: import.meta.env.VITE_BASE_URL,
      timeout: 6000,
    });

    this.instance.interceptors.request.use((config) => {
      const authStore = useAuthStore();
      const token = authStore.token;
      if (token) {
        config.headers.Authorization = "JWT " + token;
      }
      return config;
    });
  }

  post(path, data) {
    // return this.instance.post(path, data)
    return new Promise(async (resolve, reject) => {
      // await: 网络请求发送后会挂起进程，直到数据到达后线程回到然后继续执行，如果用await就一定要用async
      try {
        let result = await this.instance.post(path, data);
        // console.log(result)
        resolve(result.data);
      } catch (err) {
        let detail = err.response.data.detail;
        reject(detail);
      }
    });
  }

  get(path, params) {
    return new Promise(async (resolve, reject) => {
      try {
        let result = await this.instance.get(path, params);
        resolve(result.data);
      } catch (err) {
        let detail = err.response.data.detail;
        reject(detail);
      }
    });
  }

  put(path, data) {
    return new Promise(async (resolve, reject) => {
      try {
        let result = await this.instance.put(path, data);
        resolve(result.data);
      } catch (err) {
        let detail = err.response.data.detail;
        reject(detail);
      }
    });
  }
}

export default new Http();
