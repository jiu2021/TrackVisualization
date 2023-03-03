import { App } from "vue";
export default {
  install(app: App) {
    app.directive('title', {
      mounted(el, binding) {
        // el 为携带自定义指令的dom节点
        // binding 为指令后携带的参数通过.value取出
        document.title = binding.value;
      }
    });
  }
}