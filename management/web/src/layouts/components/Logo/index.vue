<script lang="ts" setup>
import logoText1 from "@@/assets/images/layouts/logo-text-1.png?url"
import logoText2 from "@@/assets/images/layouts/logo-text-2.png?url"
import logo from "@@/assets/images/layouts/logo.png?url"
import { useLayoutMode } from "@@/composables/useLayoutMode"

interface Props {
  collapse?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  collapse: true
})

const { isLeft, isTop } = useLayoutMode()
</script>

<template>
  <div class="layout-logo-container" :class="{ 'collapse': props.collapse, 'layout-mode-top': isTop }">
    <transition name="layout-logo-fade">
      <router-link v-if="props.collapse" key="collapse" to="/">
        <img :src="logo" class="layout-logo" alt="Logo" title="Logo">
      </router-link>
      <router-link v-else key="expand" to="/">
        <img :src="!isLeft ? logoText2 : logoText1" class="layout-logo-text" alt="系统Logo" title="系统Logo">
      </router-link>
    </transition>
  </div>
</template>

<style lang="scss" scoped>
.layout-logo-container {
  position: relative;
  width: 100%;
  height: var(--v3-header-height);
  line-height: var(--v3-header-height);
  text-align: center;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px;
  box-sizing: border-box;
  .layout-logo {
    display: none;
  }
  .layout-logo-text {
    max-height: calc(var(--v3-header-height) - 16px);
    max-width: 180px;
    object-fit: contain;
    vertical-align: middle;
  }
}

.layout-mode-top {
  height: var(--v3-header-height);
  line-height: var(--v3-header-height);
  .layout-logo-text {
    max-width: 160px;
  }
}

.collapse {
  .layout-logo {
    width: auto;
    height: calc(100% - 16px);
    max-height: 32px;
    max-width: 32px;
    object-fit: contain;
    vertical-align: middle;
    display: block;
    margin: 0 auto;
  }
  .layout-logo-text {
    display: none;
  }
}
</style>
