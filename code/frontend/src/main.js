import { BootstrapVue, BootstrapVueIcons, FormFilePlugin, ImagePlugin } from 'bootstrap-vue';


import VueLogger from 'vuejs-logger';
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import 'bootstrap/dist/css/bootstrap.css';
import FlashMessage from '@smartweb/vue-flash-message'; // https://smwbtech.github.io/vue-flash-message/

const isProduction = process.env.NODE_ENV === 'production';

// Vue.config.productionTip = false;
// Vue.prototype.$BASEURL = (Vue.config.productionTip) ? 'https://hostname' : 'http://127.0.0.1:5000';

const options = {
  isEnabled: true,
  logLevel: isProduction ? 'error' : 'debug',
  stringifyArguments: true,
  showLogLevel: false,
  showMethodName: false,
  separator: '|',
  showConsoleColors: true,
};

Vue.use(VueLogger, options); // logLevels:['debug', 'info', 'warn', 'error', 'fatal']
Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);
Vue.use(FormFilePlugin);
Vue.use(ImagePlugin);

Vue.use(FlashMessage, {
  name: "flashMessage",
  tag: "FlashMessage",
  time: 4000,
  strategy: "multiple"
}); // success, error, warning, info


new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');


store.subscribe((mutation, state) => {
  // cache store data
  localStorage.setItem('store', JSON.stringify(state));
});
