import { getActiveThemeName, setActiveThemeName } from "@@/utils/cache/local-storage"
import { setCssVar } from "@@/utils/css"

const DEFAULT_THEME_NAME = "normal"

type DefaultThemeName = typeof DEFAULT_THEME_NAME

/** 注册的主题名称, 其中 DefaultThemeName 是必填的 */
export type ThemeName = DefaultThemeName | "dark" | "dark-blue"

interface ThemeList {
  title: string
  name: ThemeName
}

/** 主题列表 */
const themeList: ThemeList[] = [
  {
    title: "默认",
    name: DEFAULT_THEME_NAME
  },
  {
    title: "黑暗",
    name: "dark"
  },
  {
    title: "深蓝",
    name: "dark-blue"
  }
]

/** 正在应用的主题名称 */
const activeThemeName = ref<ThemeName>(getActiveThemeName() || DEFAULT_THEME_NAME)

/** 设置主题 */
function setTheme({ clientX, clientY }: MouseEvent, value: ThemeName) {
  const maxRadius = Math.hypot(
    Math.max(clientX, window.innerWidth - clientX),
    Math.max(clientY, window.innerHeight - clientY)
  )
  setCssVar("--v3-theme-x", `${clientX}px`)
  setCssVar("--v3-theme-y", `${clientY}px`)
  setCssVar("--v3-theme-r", `${maxRadius}px`)
  
  // 根据主题类型设置不同的侧边栏颜色
  if (value === 'dark') {
    // 淡灰色主题
    setCssVar('--v3-sidebar-bg-color', '#e8e8e8')
    setCssVar('--v3-sidebar-text-color', '#505050')
    setCssVar('--v3-sidebar-hover-bg-color', '#d0d0d0')
    setCssVar('--v3-sidebar-active-text-color', '#333333')
  } else if (value === 'dark-blue') {
    // 肉色主题
    setCssVar('--v3-sidebar-bg-color', '#f9f0e6')
    setCssVar('--v3-sidebar-text-color', '#8b7d6b')
    setCssVar('--v3-sidebar-hover-bg-color', '#e8d7c6')
    setCssVar('--v3-sidebar-active-text-color', '#6d5d4b')
  } else {
    // 默认主题
    setCssVar('--v3-sidebar-bg-color', '#ffffff')
    setCssVar('--v3-sidebar-text-color', '#333333')
    setCssVar('--v3-sidebar-hover-bg-color', '#f5f7fa')
    setCssVar('--v3-sidebar-active-text-color', '#1890ff')
  }
  
  const handler = () => {
    activeThemeName.value = value
  }
  document.startViewTransition ? document.startViewTransition(handler) : handler()
}

/** 在 html 根元素上挂载 class */
function addHtmlClass(value: ThemeName) {
  document.documentElement.classList.add(value)
}

/** 在 html 根元素上移除其他主题 class */
function removeHtmlClass(value: ThemeName) {
  const otherThemeNameList = themeList.map(item => item.name).filter(name => name !== value)
  document.documentElement.classList.remove(...otherThemeNameList)
}

/** 初始化 */
function initTheme() {
  // watchEffect 来收集副作用
  watchEffect(() => {
    const value = activeThemeName.value
    removeHtmlClass(value)
    addHtmlClass(value)
    setActiveThemeName(value)
  })
}

/** 主题 Composable */
export function useTheme() {
  return { themeList, activeThemeName, initTheme, setTheme }
}
