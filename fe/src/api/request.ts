import axios, { AxiosRequestConfig, AxiosResponse } from "axios";
// import qs from "qs";

const requests = axios.create({
  baseURL: "/api",
  validateStatus() {
    // 使用async-await，处理reject情况较为繁琐，所以全部返回resolve，在业务代码中处理异常
    return true;
  },
});

// 请求拦截器
requests.interceptors.request.use(
  (config) => {
    // 获取token，并将其添加至请求头中
    const token = localStorage.getItem('token');
    if (token) {
      // !非空断言
      config.headers!.Authorization = "Bearer " + token;
      console.log("发送token");
    }
    // config.data = config.method === "get" ? qs.stringify(config.data) : config.data;
    console.log("发送请求");
    return config;
  },
  (error) => {
    return Promise.resolve(error);
  }
);

// 响应拦截器
requests.interceptors.response.use(
  (response: AxiosResponse) => {
    console.log(response);
    const status = response.status;
    if (status < 200 || status >= 300) {
      // 处理http错误，抛到业务代码
      console.log('请求失败')
    } else {
      console.log('请求成功')
    }
    return response;
  },
  (error) => {
    return Promise.resolve(error);
  }
);

export default requests;