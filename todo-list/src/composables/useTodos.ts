import { ref, watch } from 'vue'
import type { Todo } from '../types'

/** localStorage 存储键名 */
const STORAGE_KEY = 'vue-todo-list'

/** 从 localStorage 读取待办列表，数据损坏时返回空列表 */
function loadTodos(): Todo[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? (JSON.parse(raw) as Todo[]) : []
  } catch {
    return []
  }
}

/**
 * 待办事项核心逻辑：
 * 状态变化时自动写入 localStorage，页面刷新后数据不丢失。
 */
export function useTodos() {
  const todos = ref<Todo[]>(loadTodos())

  // 深度监听：任何增删改都会同步持久化
  watch(
    todos,
    (value) => localStorage.setItem(STORAGE_KEY, JSON.stringify(value)),
    { deep: true },
  )

  /** 添加待办（忽略空白内容），返回是否成功 */
  function addTodo(text: string): boolean {
    const trimmed = text.trim()
    if (!trimmed) return false
    todos.value.unshift({
      id: crypto.randomUUID(),
      text: trimmed,
      completed: false,
    })
    return true
  }

  /** 按 id 删除待办 */
  function removeTodo(id: string) {
    todos.value = todos.value.filter((todo) => todo.id !== id)
  }

  /** 切换完成/未完成状态 */
  function toggleTodo(id: string) {
    const todo = todos.value.find((t) => t.id === id)
    if (todo) todo.completed = !todo.completed
  }

  /** 清空所有已完成项 */
  function clearCompleted() {
    todos.value = todos.value.filter((t) => !t.completed)
  }

  return { todos, addTodo, removeTodo, toggleTodo, clearCompleted }
}
