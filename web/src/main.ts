import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './services/auth'
import VueNativeSock from 'vue-native-websocket'

import vuetify from './plugins/vuetify'

Vue.config.productionTip = false

Vue.use(VueNativeSock, 'ws://localhost:3000', {
  store: store, reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 3000,
  passToStoreHandler: (eventName: string, event: any) => {
    console.log(eventName, event)

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
