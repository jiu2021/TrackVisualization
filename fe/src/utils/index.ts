import { App } from "vue";
export default {
  install(app: App) {
    app.directive('focus', { //在创建自定义名称时不要带v-,使用时再携带
      mounted(el, binding) {
        // el 为携带自定义指令的dom节点
        // binding 为指令后携带的参数通过.value取出
        console.log(el.dataset.title);
      }
    });
  }
}