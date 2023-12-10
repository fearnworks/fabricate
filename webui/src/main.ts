// main.ts
import { createApp } from 'vue'

import {router} from '@/routes/routes'
import { Quasar } from 'quasar'
import './style.css'
// Import icon libraries
import '@quasar/extras/material-icons/material-icons.css'

// Import Quasar css
import 'quasar/src/css/index.sass'



import App from './App.vue'
import './assets/tailwind.css'
console.log("Starting Vue app...")
const app = createApp(App)

app.use(Quasar, {
  plugins: {}, // import Quasar plugins and add here
})
app.use(router)

// Assumes you have a <div id="app"></div> in your index.html
app.mount('#app')
