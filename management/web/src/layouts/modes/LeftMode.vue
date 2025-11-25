<script lang="ts" setup>
import { useAppStore } from "@/pinia/stores/app"
import { useSettingsStore } from "@/pinia/stores/settings"
import { useDevice } from "@@/composables/useDevice"
import { useLayoutMode } from "@@/composables/useLayoutMode"
import { AppMain, NavigationBar, Sidebar, TagsView } from "../components"

const { isMobile } = useDevice()
const { isLeft } = useLayoutMode()
const appStore = useAppStore()
const settingsStore = useSettingsStore()
const { showTagsView, fixedHeader } = storeToRefs(settingsStore)

/** 定义计算属性 layoutClasses，用于控制布局的类名 */
const layoutClasses = computed(() => {
  return {
    hideSidebar: !appStore.sidebar.opened,
    openSidebar: appStore.sidebar.opened,
    withoutAnimation: appStore.sidebar.withoutAnimation,
    mobile: isMobile.value,
    noLeft: !isLeft.value
  }
})

/** 用于处理点击 mobile 端侧边栏遮罩层的事件 */
function handleClickOutside() {
  appStore.closeSidebar(false)
}
</script>

<template>
  <div :class="layoutClasses" class="app-wrapper">
    <!-- mobile 端侧边栏遮罩层 -->
    <div v-if="layoutClasses.mobile && layoutClasses.openSidebar" class="drawer-bg" @click="handleClickOutside" />
    <!-- 左侧边栏 -->
    <Sidebar class="sidebar-container" />
    <!-- 主容器 -->
    <div :class="{ hasTagsView: showTagsView }" class="main-container">
      <!-- 头部导航栏和标签栏 -->
      <div :class="{ 'fixed-header': fixedHeader }" class="layout-header">
        <NavigationBar />
        <TagsView v-show="showTagsView" />
      </div>
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
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.drawer-bg {
  background-color: var(--el-mask-color);
  width: 100%;
  top: 0;
  height: 100%;
  position: absolute;
  z-index: 999;
  transition: opacity var(--v3-transition-fast);
  opacity: 0;
  animation: fadeIn 0.3s forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.sidebar-container {
  background-color: var(--v3-sidebar-menu-bg-color);
  transition: width $transition-time, box-shadow $transition-time, transform $transition-time;
  width: var(--v3-sidebar-width);
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1001;
  overflow: hidden;
  border-right: var(--v3-sidebar-border-right);
  box-shadow: 1px 0 6px rgba(0, 0, 0, 0.1);
}

.main-container {
  min-height: 100vh;
  transition: margin-left $transition-time;
  margin-left: var(--v3-sidebar-width);
  position: relative;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.fixed-header {
  position: fixed !important;
  top: 0;
  right: 0;
  z-index: 9;
  width: calc(100% - var(--v3-sidebar-width));
  transition: width $transition-time, box-shadow $transition-time;
  box-shadow: var(--v3-header-box-shadow);
  border-bottom-left-radius: var(--v3-border-radius-md);
}

.layout-header {
  position: relative;
  z-index: 9;
  background-color: var(--v3-header-bg-color);
  box-shadow: var(--v3-header-box-shadow);
  border-bottom: var(--v3-header-border-bottom);
}

.app-main {
  min-height: calc(100vh - var(--v3-navigationbar-height));
  position: relative;
  overflow: hidden;
  background-color: var(--el-bg-color-page);
  border-radius: var(--v3-border-radius-lg);
  margin: var(--v3-spacing-md);
  padding: var(--v3-spacing-lg);
  box-shadow: var(--el-box-shadow-light);
}

.fixed-header + .app-main {
  padding-top: calc(var(--v3-spacing-lg) + var(--v3-navigationbar-height));
  margin-top: var(--v3-spacing-sm);
  height: 100vh;
  overflow: auto;
}

.hasTagsView {
  .app-main {
    min-height: calc(100vh - var(--v3-header-height));
  }
  .fixed-header + .app-main {
    padding-top: calc(var(--v3-spacing-lg) + var(--v3-header-height));
  }
}

.hideSidebar {
  .sidebar-container {
    width: var(--v3-sidebar-hide-width);
    box-shadow: 1px 0 4px rgba(0, 0, 0, 0.08);
  }
  .main-container {
    margin-left: var(--v3-sidebar-hide-width);
  }
  .fixed-header {
    width: calc(100% - var(--v3-sidebar-hide-width));
  }
}

// 适配 mobile 端
.mobile {
  .sidebar-container {
    transition: transform $transition-time, box-shadow $transition-time;
    width: var(--v3-sidebar-width);
    box-shadow: 2px 0 12px rgba(0, 0, 0, 0.15);
    transform: translate3d(calc(0px - var(--v3-sidebar-width)), 0, 0);
  }
  .main-container {
    margin-left: 0px;
  }
  .fixed-header {
    width: 100%;
    border-bottom-left-radius: 0;
  }
  &.openSidebar {
    position: fixed;
    top: 0;
    .sidebar-container {
      transform: translate3d(0, 0, 0);
    }
  }
  &.hideSidebar {
    .sidebar-container {
      pointer-events: none;
      transition-duration: var(--v3-transition-normal);
      transform: translate3d(calc(0px - var(--v3-sidebar-width)), 0, 0);
    }
  }
  // 既是 mobile 又是顶部或混合布局模式
  &.noLeft {
    .sidebar-container {
      background-color: var(--el-bg-color);
    }
  }
}

.withoutAnimation {
  .sidebar-container,
  .main-container,
  .fixed-header {
    transition: none !important;
  }
}
</style>
