/*eslint-disable*/

import 'bootstrap/dist/css/bootstrap.min.css';
import Vue from 'vue';
import 'font-awesome/css/font-awesome.min.css';

import App from './App.vue';
import router from './router';

export const EventBus = new Vue();

Vue.config.productionTip = false;
Vue.component('VueFontawesome', require('vue-fontawesome-icon/VueFontawesome.vue').default);

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
