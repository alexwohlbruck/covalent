import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './services/auth'
import VueNativeSock from 'vue-native-websocket'

import vuetify from './plugins/vuetify'

Vue.config.productionTip = false

let wsUrl = window.origin.toString().replace('http', 'ws')
if (process.env.NODE_ENV === 'development')
  wsUrl = wsUrl.replace('8080', '3000')

Vue.use(VueNativeSock, wsUrl, {
  store, reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 3000,
  passToStoreHandler: (eventName: string, event: any) => {
    if (!eventName.startsWith('SOCKET_')) return

    switch (eventName) {
      case 'SOCKET_onmessage': {
        const { name, data } = JSON.parse(event.data)
        store.commit(name, data)
      }
    }
  }
})

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount('#app')
