<script lang="ts" setup>
import { useAppStore } from "@/pinia/stores/app"
import { usePermissionStore } from "@/pinia/stores/permission"
import { useSettingsStore } from "@/pinia/stores/settings"
import { useDevice } from "@@/composables/useDevice"
import { useLayoutMode } from "@@/composables/useLayoutMode"
import { getCssVar } from "@@/utils/css"
import { Logo } from "../index"
import Item from "./Item.vue"

const v3SidebarMenuBgColor = getCssVar("--v3-sidebar-menu-bg-color")
const v3SidebarMenuTextColor = getCssVar("--v3-sidebar-menu-text-color")
const v3SidebarMenuActiveTextColor = getCssVar("--v3-sidebar-menu-active-text-color")

const { isMobile } = useDevice()
const { isLeft, isTop } = useLayoutMode()
const route = useRoute()
const appStore = useAppStore()
const permissionStore = usePermissionStore()
const settingsStore = useSettingsStore()

const activeMenu = computed(() => route.meta.activeMenu || route.path)
const noHiddenRoutes = computed(() => permissionStore.routes.filter(item => !item.meta?.hidden))
const isCollapse = computed(() => !appStore.sidebar.opened)
const isLogo = computed(() => isLeft.value && settingsStore.showLogo)
const backgroundColor = computed(() => (isLeft.value ? v3SidebarMenuBgColor : undefined))
const textColor = computed(() => (isLeft.value ? v3SidebarMenuTextColor : undefined))
const activeTextColor = computed(() => (isLeft.value ? v3SidebarMenuActiveTextColor : undefined))
const sidebarMenuItemHeight = computed(() => !isTop.value ? "var(--v3-sidebar-menu-item-height)" : "var(--v3-navigationbar-height)")
const sidebarMenuHoverBgColor = computed(() => !isTop.value ? "var(--v3-sidebar-menu-hover-bg-color)" : "transparent")
const tipLineWidth = computed(() => !isTop.value ? "2px" : "0px")
</script>

<template>
  <div :class="{ 'has-logo': isLogo }">
    <Logo v-if="isLogo" :collapse="isCollapse" />
    <el-scrollbar wrap-class="scrollbar-wrapper">
      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse && !isTop"
        :background-color="backgroundColor"
        :text-color="textColor"
        :active-text-color="activeTextColor"
        :collapse-transition="false"
        :mode="isTop && !isMobile ? 'horizontal' : 'vertical'"
      >
        <Item
          v-for="noHiddenRoute in noHiddenRoutes"
          :key="noHiddenRoute.path"
          :item="noHiddenRoute"
          :base-path="noHiddenRoute.path"
        />
      </el-menu>
    </el-scrollbar>
  </div>
</template>

<style lang="scss" scoped>
%tip-line {
  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: v-bind(tipLineWidth);
    height: 100%;
    background-color: var(--v3-sidebar-menu-tip-line-bg-color);
    border-radius: 0 2px 2px 0;
  }
}

.has-logo {
  .el-scrollbar {
    height: calc(100% - var(--v3-header-height));
  }
}

.el-scrollbar {
  height: 100%;
  :deep(.scrollbar-wrapper) {
    // 限制水平宽度
    overflow-x: hidden;
    // 优化滚动条样式
    &::-webkit-scrollbar {
      width: 6px;
    }
    &::-webkit-scrollbar-track {
      background: rgba(0, 0, 0, 0.05);
    }
    &::-webkit-scrollbar-thumb {
      background: rgba(0, 0, 0, 0.2);
      border-radius: 3px;
      &:hover {
        background: rgba(0, 0, 0, 0.3);
      }
    }
  }
  // 滚动条
  :deep(.el-scrollbar__bar) {
    &.is-horizontal {
      // 隐藏水平滚动条
      display: none;
    }
  }
}

.el-menu {
  user-select: none;
  border: none;
  width: 100%;
  transition: background-color 0.3s ease;
}

.el-menu--horizontal {
  height: v-bind(sidebarMenuItemHeight);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

:deep(.el-menu-item),
:deep(.el-sub-menu__title),
:deep(.el-sub-menu .el-menu-item),
:deep(.el-menu--horizontal .el-menu-item) {
  height: v-bind(sidebarMenuItemHeight);
  line-height: v-bind(sidebarMenuItemHeight);
  transition: all 0.3s ease;
  border-radius: 0 4px 4px 0;
  position: relative;
  &.is-active,
  &:hover {
    background-color: v-bind(sidebarMenuHoverBgColor);
    transform: translateX(2px);
  }
}

:deep(.el-sub-menu) {
  &.is-active {
    > .el-sub-menu__title {
      color: v-bind(activeTextColor);
      font-weight: 500;
    }
  }
}

// 单独处理标题悬停效果
:deep(.el-sub-menu__title) {
  &:hover {
    color: v-bind(activeTextColor);
  }
}


:deep(.el-menu-item.is-active) {
  @extend %tip-line;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.el-menu--collapse {
  :deep(.el-sub-menu.is-active) {
    .el-sub-menu__title {
      @extend %tip-line;
      background-color: v-bind(sidebarMenuHoverBgColor);
      font-weight: 500;
      transform: translateX(2px);
    }
  }
}

// 添加图标样式优化
:deep(.el-menu-item i),
:deep(.el-sub-menu__title i) {
  font-size: 16px;
  width: 20px;
  text-align: center;
  margin-right: 12px;
  transition: all 0.3s ease;
}

// 添加侧边栏动画效果
.el-menu--collapse {
  :deep(.el-menu-item),
  :deep(.el-sub-menu__title) {
    i {
      margin-right: 0;
      font-size: 18px;
    }
  }
}

// 移动端优化
@media (max-width: 768px) {
  .el-menu {
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  }
}
</style>
