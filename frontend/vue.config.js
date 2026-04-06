const path = require("path");
const { defineConfig } = require("@vue/cli-service");

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    resolve: {
      alias: {
        "vue-recaptcha-plugin-core": path.resolve(__dirname, "node_modules/vue-recaptcha/dist/plugin.cjs"),
        "vue-recaptcha-head-loader": path.resolve(__dirname, "node_modules/vue-recaptcha/dist/script-manager/head.cjs"),
        "vue-recaptcha-provider": path.resolve(__dirname, "node_modules/vue-recaptcha/dist/composables/script-provider.cjs"),
        "vue-recaptcha-proxy": path.resolve(__dirname, "node_modules/vue-recaptcha/dist/composables/context.cjs"),
      },
    },
  },
});
