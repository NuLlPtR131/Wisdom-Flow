<script lang="ts" setup>
import { useSettingsStore } from "@/pinia/stores/settings"
import { AppMain, Logo, NavigationBar, TagsView } from "../components"

const settingsStore = useSettingsStore()
const { showTagsView, showLogo } = storeToRefs(settingsStore)
</script>

<template>
  <div class="app-wrapper">
    <!-- 头部导航栏和标签栏 -->
    <div class="fixed-header layout-header">
      <div class="content">
        <Logo v-if="showLogo" :collapse="false" class="logo" />
        <NavigationBar class="navigation-bar" />
      </div>
      <TagsView v-show="showTagsView" />
    </div>
    <!-- 主容器 -->
    <div :class="{ hasTagsView: showTagsView }" class="main-container">
      <!-- 页面主体内容 -->
      <AppMain class="app-main" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import "@@/assets/styles/mixins.scss";
$transition-time: var(--v3-transition-normal);

.app-wrapper {
  @extend %clearfix;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.fixed-header {
  position: fixed;
  top: 0;
  z-index: 1002;
  width: 100%;
  box-shadow: var(--v3-header-box-shadow);
  .logo {
    width: var(--v3-sidebar-width);
    display: flex;
    align-items: center;
    justify-content: center;
    height: var(--v3-navigationbar-height);
    background-color: var(--v3-sidebar-menu-bg-color);
    border-right: var(--v3-sidebar-border-right);
    color: #ffffff;
    font-weight: bold;
    font-size: 18px;
    overflow: hidden;
  }
  .content {
    display: flex;
    .navigation-bar {
      flex: 1;
    }
  }
}

.layout-header {
  background-color: var(--v3-header-bg-color);
  box-shadow: var(--v3-header-box-shadow);
  border-bottom: var(--v3-header-border-bottom);
}

.main-container {
  min-height: 100vh;
  display: flex;
  flex: 1;
}

.app-main {
  transition: padding-left $transition-time, padding-top $transition-time;
  padding-top: calc(var(--v3-spacing-lg) + var(--v3-navigationbar-height));
  height: 100vh;
  overflow: auto;
  background-color: var(--el-bg-color-page);
  border-radius: var(--v3-border-radius-lg);
  margin: var(--v3-spacing-md);
  padding: var(--v3-spacing-lg);
  box-shadow: var(--el-box-shadow-light);
  flex: 1;
}

.hasTagsView {
  .app-main {
    padding-top: calc(var(--v3-spacing-lg) + var(--v3-header-height));
  }
}
</style>
