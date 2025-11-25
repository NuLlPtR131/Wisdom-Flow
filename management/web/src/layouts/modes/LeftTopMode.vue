<script lang="ts" setup>
import { useAppStore } from "@/pinia/stores/app"
import { useSettingsStore } from "@/pinia/stores/settings"
import { AppMain, Logo, NavigationBar, Sidebar, TagsView } from "../components"

const appStore = useAppStore()
const settingsStore = useSettingsStore()
const { showTagsView, showLogo } = storeToRefs(settingsStore)

/** 定义计算属性 layoutClasses，用于控制布局的类名 */
const layoutClasses = computed(() => {
  return {
    hideSidebar: !appStore.sidebar.opened
  }
})
</script>

<template>
  <div :class="layoutClasses" class="app-wrapper">
    <!-- 头部导航栏和标签栏 -->
    <div class="fixed-header layout-header">
      <Logo v-if="showLogo" :collapse="false" class="logo" />
      <div class="content">
        <NavigationBar />
        <TagsView v-show="showTagsView" />
      </div>
    </div>
    <!-- 主容器 -->
    <div :class="{ hasTagsView: showTagsView }" class="main-container">
      <!-- 左侧边栏 -->
      <Sidebar class="sidebar-container" />
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
  display: flex;
  box-shadow: var(--v3-header-box-shadow);
  .logo {
    flex: none;
    width: var(--v3-sidebar-width);
    transition: width $transition-time;
  }
  .content {
    flex: 1;
    overflow: hidden;
    min-width: 0;
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

.sidebar-container {
  background-color: #ffffff;
  transition: width $transition-time, box-shadow $transition-time;
  width: var(--v3-sidebar-width);
  height: 100vh;
  position: fixed;
  left: 0;
  z-index: 1001;
  overflow: hidden;
  border-right: 1px solid #f0f0f0;
  padding-top: var(--v3-navigationbar-height);
  box-shadow: 1px 0 6px rgba(0, 0, 0, 0.05);
}

.app-main {
  transition: padding-left $transition-time, padding-top $transition-time;
  padding-top: calc(var(--v3-spacing-lg) + var(--v3-navigationbar-height));
  padding-left: var(--v3-sidebar-width);
  height: 100vh;
  overflow: auto;
  background-color: var(--el-bg-color-page);
  border-radius: var(--v3-border-radius-lg);
  margin: var(--v3-spacing-md);
  padding-right: var(--v3-spacing-lg);
  box-shadow: var(--el-box-shadow-light);
  flex: 1;
}

.hideSidebar {
  .sidebar-container {
    width: var(--v3-sidebar-hide-width);
    box-shadow: 1px 0 4px rgba(0, 0, 0, 0.08);
  }
  .app-main {
    padding-left: var(--v3-sidebar-hide-width);
  }
  .fixed-header .logo {
    width: var(--v3-sidebar-hide-width);
  }
}

.hasTagsView {
  .sidebar-container {
    padding-top: var(--v3-header-height);
  }
  .app-main {
    padding-top: calc(var(--v3-spacing-lg) + var(--v3-header-height));
  }
}

.fixed-header .logo {
  display: flex;
  align-items: center;
  justify-content: center;
  height: var(--v3-navigationbar-height);
  background-color: var(--v3-sidebar-bg-color, #ffffff);
  border-right: 1px solid var(--v3-sidebar-border-right, #f0f0f0);
  color: var(--v3-sidebar-text-color, #333333);
  font-weight: bold;
  font-size: 18px;
  overflow: hidden;
  box-shadow: 1px 0 4px rgba(0, 0, 0, 0.05);
}
</style>
