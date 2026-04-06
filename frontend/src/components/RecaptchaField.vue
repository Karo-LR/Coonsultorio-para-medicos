<template>
  <div class="recaptcha-field">
    <div ref="container"></div>
  </div>
</template>

<script setup>
/* global defineProps, defineEmits */
import { onMounted, ref } from "vue";
import { useRecaptchaProvider } from "vue-recaptcha-provider";
import { useRecaptchaProxy } from "vue-recaptcha-proxy";

defineProps({
  modelValue: {
    type: String,
    default: "",
  },
});

const emit = defineEmits(["update:modelValue"]);
const siteKey =
  process.env.VUE_APP_RECAPTCHA_SITE_KEY || "6Lf2a6YsAAAAAMblsNffyJjC61bVoCYTDKChbV94";
const container = ref(null);

useRecaptchaProvider();
const proxy = useRecaptchaProxy();

onMounted(async () => {
  if (!container.value) {
    return;
  }

  await proxy.render(container.value, {
    sitekey: siteKey,
    theme: "light",
    size: "normal",
    callback: (token) => emit("update:modelValue", token || ""),
    "expired-callback": () => emit("update:modelValue", ""),
    "error-callback": () => emit("update:modelValue", ""),
  });
});
</script>
