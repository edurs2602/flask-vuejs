/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App
 */

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

// Importando o Vue Router
import router from './router'

const app = createApp(App)

// Registrando plugins (como Vuetify)
registerPlugins(app)

// Integrando o Vue Router à aplicação
app.use(router)

// Montando a aplicação no DOM
app.mount('#app')
