// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import SuiVue from 'semantic-ui-vue'
import echarts from 'echarts'
import './style/demo1.css'
import screenfull from 'screenfull'


Vue.use(SuiVue);
Vue.use(echarts);
Vue.use(screenfull);

Vue.config.productionTip = false;
Vue.prototype.$axios = axios;
Vue.prototype.$echarts = echarts;
Vue.prototype.$screenfull = screenfull;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
});
