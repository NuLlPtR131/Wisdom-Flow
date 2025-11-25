<script lang="ts" setup>
import type { TagView } from "@/pinia/stores/tags-view"
import type { RouteLocationNormalizedGeneric, RouteRecordRaw, RouterLink } from "vue-router"
import { usePermissionStore } from "@/pinia/stores/permission"
import { useTagsViewStore } from "@/pinia/stores/tags-view"
import { useRouteListener } from "@@/composables/useRouteListener"
import { Close } from "@element-plus/icons-vue"
import path from "path-browserify"
import ScrollPane from "./ScrollPane.vue"

const router = useRouter()

const route = useRoute()

const tagsViewStore = useTagsViewStore()

const permissionStore = usePermissionStore()

const { listenerRouteChange } = useRouteListener()

/** 标签页组件元素的引用数组 */
const tagRefs = ref<InstanceType<typeof RouterLink>[]>([])

/** 右键菜单的状态 */
const visible = ref(false)

/** 右键菜单的 top 位置 */
const top = ref(0)

/** 右键菜单的 left 位置 */
const left = ref(0)

/** 当前正在右键操作的标签页 */
const selectedTag = ref<TagView>({})

/** 固定的标签页 */
let affixTags: TagView[] = []

/** 判断标签页是否激活 */
function isActive(tag: TagView) {
  return tag.path === route.path
}

/** 判断标签页是否固定 */
function isAffix(tag: TagView) {
  return tag.meta?.affix
}

/** 筛选出固定标签页 */
function filterAffixTags(routes: RouteRecordRaw[], basePath = "/") {
  const tags: TagView[] = []
  routes.forEach((route) => {
    if (isAffix(route)) {
      const tagPath = path.resolve(basePath, route.path)
      tags.push({
        fullPath: tagPath,
        path: tagPath,
        name: route.name,
        meta: { ...route.meta }
      })
    }
    if (route.children) {
      const childTags = filterAffixTags(route.children, route.path)
      tags.push(...childTags)
    }
  })
  return tags
}

/** 初始化标签页 */
function initTags() {
  affixTags = filterAffixTags(permissionStore.routes)
  for (const tag of affixTags) {
    // 必须含有 name 属性
    tag.name && tagsViewStore.addVisitedView(tag)
  }
}

/** 添加标签页 */
function addTags(route: RouteLocationNormalizedGeneric) {
  if (route.name) {
    tagsViewStore.addVisitedView(route)
    tagsViewStore.addCachedView(route)
  }
}

/** 刷新当前正在右键操作的标签页 */
function refreshSelectedTag(view: TagView) {
  tagsViewStore.delCachedView(view)
  router.replace({ path: `/redirect${view.path}`, query: view.query })
}

/** 关闭当前正在右键操作的标签页 */
function closeSelectedTag(view: TagView) {
  tagsViewStore.delVisitedView(view)
  tagsViewStore.delCachedView(view)
  isActive(view) && toLastView(tagsViewStore.visitedViews, view)
}

/** 关闭其他标签页 */
function closeOthersTags() {
  const fullPath = selectedTag.value.fullPath
  if (fullPath !== route.path && fullPath !== undefined) {
    router.push(fullPath)
  }
  tagsViewStore.delOthersVisitedViews(selectedTag.value)
  tagsViewStore.delOthersCachedViews(selectedTag.value)
}

/** 关闭所有标签页 */
function closeAllTags(view: TagView) {
  tagsViewStore.delAllVisitedViews()
  tagsViewStore.delAllCachedViews()
  if (affixTags.some(tag => tag.path === route.path)) return
  toLastView(tagsViewStore.visitedViews, view)
}

/** 跳转到最后一个标签页 */
function toLastView(visitedViews: TagView[], view: TagView) {
  const latestView = visitedViews.slice(-1)[0]
  const fullPath = latestView?.fullPath
  if (fullPath !== undefined) {
    router.push(fullPath)
  } else {
    // 如果 TagsView 全部被关闭了，则默认重定向到主页
    if (view.name === "Dashboard") {
      // 重新加载主页
      router.push({ path: `/redirect${view.path}`, query: view.query })
    } else {
      router.push("/")
    }
  }
}

/** 打开右键菜单面板 */
function openMenu(tag: TagView, e: MouseEvent) {
  const menuMinWidth = 100
  // 当前页面宽度
  const offsetWidth = document.body.offsetWidth
  // 面板的最大左边距
  const maxLeft = offsetWidth - menuMinWidth
  // 面板距离鼠标指针的距离
  const left15 = e.clientX + 10
  left.value = left15 > maxLeft ? maxLeft : left15
  top.value = e.clientY
  // 显示面板
  visible.value = true
  // 更新当前正在右键操作的标签页
  selectedTag.value = tag
}

/** 关闭右键菜单面板 */
function closeMenu() {
  visible.value = false
}

watch(visible, (value) => {
  value ? document.body.addEventListener("click", closeMenu) : document.body.removeEventListener("click", closeMenu)
})

initTags()

// 监听路由变化
listenerRouteChange((route) => {
  addTags(route)
}, true)
</script>

<template>
  <div class="tags-view-container">
    <ScrollPane class="tags-view-wrapper" :tag-refs="tagRefs">
      <router-link
        v-for="tag in tagsViewStore.visitedViews"
        :key="tag.path"
        ref="tagRefs"
        :class="{ active: isActive(tag) }"
        class="tags-view-item"
        :to="{ path: tag.path, query: tag.query }"
        @click.middle="!isAffix(tag) && closeSelectedTag(tag)"
        @contextmenu.prevent="openMenu(tag, $event)"
      >
        {{ tag.meta?.title }}
        <el-icon v-if="!isAffix(tag)" :size="12" @click.prevent.stop="closeSelectedTag(tag)">
          <Close />
        </el-icon>
      </router-link>
    </ScrollPane>
    <ul v-show="visible" class="contextmenu" :style="{ left: `${left}px`, top: `${top}px` }">
      <li @click="refreshSelectedTag(selectedTag)">
        刷新
      </li>
      <li v-if="!isAffix(selectedTag)" @click="closeSelectedTag(selectedTag)">
        关闭
      </li>
      <li @click="closeOthersTags">
        关闭其它
      </li>
      <li @click="closeAllTags(selectedTag)">
        关闭所有
      </li>
    </ul>
  </div>
</template>

<style lang="scss" scoped>
.tags-view-container {
  height: var(--v3-tagsview-height);
  width: 100%;
  color: var(--v3-tagsview-text-color);
  overflow: hidden;
  height: var(--v3-tagsview-height);
  display: flex;
  align-items: center;
  .tags-view-wrapper {
    display: flex;
    align-items: center;
    padding: 0 var(--v3-spacing-md);
    .tags-view-item {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      position: relative;
      cursor: pointer;
      height: 32px;
      line-height: 32px;
      border: 1px solid var(--v3-tagsview-tag-border-color);
      border-radius: var(--v3-tagsview-tag-border-radius);
      background-color: var(--v3-tagsview-tag-bg-color);
      padding: 0 12px;
      font-size: 13px;
      margin-left: var(--v3-spacing-sm);
      transition: all var(--v3-transition-fast);
      user-select: none;
      &:first-of-type {
        margin-left: 0;
      }
      &:hover {
        background-color: var(--el-bg-color-overlay);
        border-color: var(--el-border-color);
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      }
      &.active {
        background-color: var(--v3-tagsview-tag-active-bg-color);
        color: var(--v3-tagsview-tag-active-text-color);
        border-color: var(--v3-tagsview-tag-active-border-color);
        box-shadow: 0 2px 6px rgba(64, 158, 255, 0.2);
      }
      .el-icon {
        margin-left: var(--v3-spacing-sm);
        margin-right: 2px;
        border-radius: 50%;
        width: 16px;
        height: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        transition: all var(--v3-transition-fast);
        opacity: 0.8;
        &:hover {
          background-color: var(--v3-tagsview-tag-icon-hover-bg-color);
          color: var(--v3-tagsview-tag-icon-hover-color);
          opacity: 1;
          transform: scale(1.1);
        }
      }
    }
  }
  .contextmenu {
    margin: 0;
    z-index: 3000;
    position: fixed;
    list-style-type: none;
    padding: var(--v3-spacing-xs) 0;
    border-radius: var(--v3-tagsview-contextmenu-border-radius);
    font-size: 13px;
    color: var(--v3-tagsview-contextmenu-text-color);
    background-color: var(--v3-tagsview-contextmenu-bg-color);
    box-shadow: var(--v3-tagsview-contextmenu-box-shadow);
    border: 1px solid var(--el-border-color);
    animation: contextMenuFadeIn 0.2s ease;
    li {
      margin: 0;
      padding: var(--v3-spacing-sm) var(--v3-spacing-lg);
      cursor: pointer;
      transition: all var(--v3-transition-fast);
      &:hover {
        color: var(--v3-tagsview-contextmenu-hover-text-color);
        background-color: var(--v3-tagsview-contextmenu-hover-bg-color);
        padding-left: calc(var(--v3-spacing-lg) + 2px);
      }
      &:hover:not(:last-child) {
        border-bottom: 1px solid transparent;
      }
    }
  }
  
  @keyframes contextMenuFadeIn {
    from {
      opacity: 0;
      transform: translateY(-4px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
}
</style>
