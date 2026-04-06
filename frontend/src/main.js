import { createApp } from "vue";
import { createPlugin } from "vue-recaptcha-plugin-core";
import { createHeadRecaptcha } from "vue-recaptcha-head-loader";

import App from "./App.vue";
import router from "./router";
import "./styles.css";

const VueRecaptchaPlugin = createPlugin(createHeadRecaptcha);

createApp(App)
  .use(VueRecaptchaPlugin, {
    v2SiteKey: process.env.VUE_APP_RECAPTCHA_SITE_KEY || "6Lf2a6YsAAAAAMblsNffyJjC61bVoCYTDKChbV94",
  })
  .use(router)
  .mount("#app");
