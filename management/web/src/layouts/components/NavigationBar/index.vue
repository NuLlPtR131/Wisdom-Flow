<script lang="ts" setup>
import { useAppStore } from "@/pinia/stores/app"
import { useSettingsStore } from "@/pinia/stores/settings"
import { useUserStore } from "@/pinia/stores/user"
import Notify from "@@/components/Notify/index.vue"
import Screenfull from "@@/components/Screenfull/index.vue"
import SearchMenu from "@@/components/SearchMenu/index.vue"
import ThemeSwitch from "@@/components/ThemeSwitch/index.vue"
import { useDevice } from "@@/composables/useDevice"
import { useLayoutMode } from "@@/composables/useLayoutMode"
import { UserFilled } from "@element-plus/icons-vue"
import { Breadcrumb, Hamburger, Sidebar } from "../index"

const { isMobile } = useDevice()
const { isTop } = useLayoutMode()
const router = useRouter()
const appStore = useAppStore()
const userStore = useUserStore()
const settingsStore = useSettingsStore()
const { showNotify, showThemeSwitch, showScreenfull, showSearchMenu } = storeToRefs(settingsStore)

/** 切换侧边栏 */
function toggleSidebar() {
  appStore.toggleSidebar(false)
}

/** 登出 */
function logout() {
  userStore.logout()
  router.push("/login")
}
</script>

<template>
  <div class="navigation-bar">
    <Hamburger
      v-if="!isTop || isMobile"
      :is-active="appStore.sidebar.opened"
      class="hamburger"
      @toggle-click="toggleSidebar"
    />
    <Breadcrumb v-if="!isTop || isMobile" class="breadcrumb" />
    <Sidebar v-if="isTop && !isMobile" class="sidebar" />
    <div class="right-menu">
      <SearchMenu v-if="showSearchMenu" class="right-menu-item" />
      <Screenfull v-if="showScreenfull" class="right-menu-item" />
      <ThemeSwitch v-if="showThemeSwitch" class="right-menu-item" />
      <Notify v-if="showNotify" class="right-menu-item" />
      <el-dropdown>
        <div class="right-menu-item user">
          <el-avatar :src="userStore.avatar" :size="30" />
          <span>{{ userStore.username }}</span>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="logout">
              退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.navigation-bar {
  height: var(--v3-navigationbar-height);
  box-shadow: var(--v3-header-box-shadow);
  border-bottom: var(--v3-header-border-bottom);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--v3-spacing-lg);
  background-color: var(--v3-header-bg-color);
  position: relative;
  z-index: 100;
  transition: all var(--v3-transition-normal);
  .hamburger {
    color: var(--v3-header-text-color);
    cursor: pointer;
    font-size: 20px;
    padding: var(--v3-spacing-sm);
    border-radius: var(--v3-border-radius-md);
    transition: all var(--v3-transition-fast);
    display: flex;
    align-items: center;
    height: 100%;
    &:hover {
      background-color: var(--v3-header-hover-bg-color);
      color: var(--v3-header-hover-text-color);
      transform: scale(1.05);
    }
  }
  .breadcrumb {
    flex: 1;
    margin-left: var(--v3-spacing-lg);
    @media screen and (max-width: 576px) {
      display: none;
    }
    .el-breadcrumb {
      .el-breadcrumb__item {
        font-size: 14px;
        .el-breadcrumb__inner {
          color: var(--el-text-color-primary);
          font-weight: 500;
          &:hover {
            color: var(--el-color-primary);
          }
        }
        .el-breadcrumb__separator {
          color: var(--el-text-color-secondary);
          margin: 0 var(--v3-spacing-sm);
        }
      }
    }
  }
  .sidebar {
    flex: 1;
    // 设置 min-width 是为了让 Sidebar 里的 el-menu 宽度自适应
    min-width: 0px;
    :deep(.el-menu) {
      background-color: transparent;
    }
    :deep(.el-sub-menu) {
      &.is-active {
        .el-sub-menu__title {
          color: var(--el-color-primary);
        }
      }
    }
  }
  .right-menu {
    display: flex;
    align-items: center;
    gap: var(--v3-spacing-sm);
    &-item {
      margin: 0;
      cursor: pointer;
      color: var(--v3-header-text-color);
      position: relative;
      transition: all var(--v3-transition-fast);
      padding: var(--v3-spacing-sm) var(--v3-spacing-md);
      border-radius: var(--v3-border-radius-md);
      display: flex;
      align-items: center;
      justify-content: center;
      &:hover {
        color: var(--v3-header-hover-text-color);
        background-color: var(--v3-header-hover-bg-color);
        transform: translateY(-1px);
      }
      &:active {
        transform: translateY(0);
      }
      .badge {
        position: absolute;
        top: 2px;
        right: 2px;
        min-width: 16px;
        height: 16px;
        padding: 0 6px;
        font-size: 12px;
        line-height: 16px;
        border-radius: 8px;
        background-color: var(--el-color-danger);
        color: #ffffff;
        text-align: center;
        transform: scale(0.8);
      }
    }
    .user {
      display: flex;
      align-items: center;
      cursor: pointer;
      color: var(--v3-header-text-color);
      padding: var(--v3-spacing-xs) var(--v3-spacing-sm);
      border-radius: var(--v3-border-radius-md);
      transition: all var(--v3-transition-fast);
      &:hover {
        color: var(--v3-header-hover-text-color);
        background-color: var(--v3-header-hover-bg-color);
      }
      .el-avatar {
        width: 36px;
        height: 36px;
        margin-right: var(--v3-spacing-sm);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: all var(--v3-transition-fast);
        border: 2px solid transparent;
        &:hover {
          border-color: var(--el-color-primary);
          box-shadow: 0 0 0 2px var(--el-color-primary-light-9);
        }
      }
      span {
        font-size: 14px;
        font-weight: 500;
      }
    }
  }
}

// 移动端响应式设计
@media screen and (max-width: 768px) {
  .navigation-bar {
    padding: 0 var(--v3-spacing-md);
  }
  .breadcrumb {
    display: none;
  }
  .right-menu {
    .right-menu-item {
      padding: var(--v3-spacing-sm);
    }
    .user span {
      display: none;
    }
  }
}

// 平板设备优化
@media screen and (max-width: 1024px) {
  .navigation-bar .breadcrumb {
    margin-left: var(--v3-spacing-md);
    .el-breadcrumb {
      .el-breadcrumb__item {
        font-size: 13px;
      }
    }
  }
}
</style>
