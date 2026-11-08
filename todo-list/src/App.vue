<script setup lang="ts">
import { computed, ref } from 'vue'
import TodoItem from './components/TodoItem.vue'
import { useTodos } from './composables/useTodos'
import type { Filter } from './types'

const { todos, addTodo, removeTodo, toggleTodo, clearCompleted } = useTodos()

/** 新待办的输入内容 */
const draft = ref('')

/** 当前筛选状态 */
const filter = ref<Filter>('all')

const filters: { value: Filter; label: string }[] = [
  { value: 'all', label: '全部' },
  { value: 'active', label: '未完成' },
  { value: 'completed', label: '已完成' },
]

/** 按当前筛选状态过滤后的列表 */
const visibleTodos = computed(() => {
  switch (filter.value) {
    case 'active':
      return todos.value.filter((t) => !t.completed)
    case 'completed':
      return todos.value.filter((t) => t.completed)
    default:
      return todos.value
  }
})

const remainingCount = computed(() => todos.value.filter((t) => !t.completed).length)
const completedCount = computed(() => todos.value.length - remainingCount.value)

/** 心情图标：根据待办完成情况自动变化 */
const mood = computed<{ icon: string; text: string }>(() => {
  const total = todos.value.length
  if (total === 0) return { icon: '😌', text: '暂无待办，享受当下' }
  const doneRatio = completedCount.value / total
  if (doneRatio === 1) return { icon: '🎉', text: '全部完成，太棒了！' }
  if (doneRatio >= 0.6) return { icon: '😄', text: '接近目标，加把劲' }
  if (doneRatio >= 0.3) return { icon: '🙂', text: '稳步推进中' }
  if (remainingCount.value >= 5) return { icon: '😫', text: '任务有点多，深呼吸' }
  return { icon: '😐', text: '刚起步，慢慢来' }
})

function submit() {
  if (addTodo(draft.value)) draft.value = ''
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-sky-50 px-4 py-10">
    <main class="mx-auto w-full max-w-xl">
      <!-- 标题 -->
      <header class="mb-6 text-center">
        <h1 class="flex items-center justify-center gap-2 text-3xl font-bold tracking-tight text-slate-800">
          📝 待办清单
          <!-- 心情小图标：随完成度变化，悬停显示说明 -->
          <span
            class="inline-block cursor-default select-none text-2xl transition-transform hover:scale-125"
            :title="mood.text"
            >{{ mood.icon }}</span
          >
        </h1>
        <p class="mt-1 text-sm text-slate-500">{{ mood.text }} · 数据保存在浏览器本地，刷新页面不丢失</p>
      </header>

      <!-- 添加表单 -->
      <form class="mb-5 flex gap-2" @submit.prevent="submit">
        <input
          v-model="draft"
          type="text"
          placeholder="输入新的待办事项…"
          maxlength="200"
          class="flex-1 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm text-slate-700 shadow-sm outline-none transition placeholder:text-slate-400 focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100"
        />
        <button
          type="submit"
          :disabled="!draft.trim()"
          class="rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-medium text-white shadow-sm transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-40"
        >
          添加
        </button>
      </form>

      <!-- 状态筛选 -->
      <div class="mb-4 flex items-center justify-between">
        <div class="flex gap-1 rounded-xl bg-slate-100 p-1">
          <button
            v-for="f in filters"
            :key="f.value"
            type="button"
            class="rounded-lg px-3.5 py-1.5 text-sm transition"
            :class="
              filter === f.value
                ? 'bg-white font-medium text-indigo-600 shadow-sm'
                : 'text-slate-500 hover:text-slate-700'
            "
            @click="filter = f.value"
          >
            {{ f.label }}
          </button>
        </div>
        <span class="text-xs text-slate-500">剩余 {{ remainingCount }} 项未完成</span>
      </div>

      <!-- 待办列表 -->
      <ul v-if="visibleTodos.length" class="space-y-2.5">
        <TodoItem
          v-for="todo in visibleTodos"
          :key="todo.id"
          :todo="todo"
          @toggle="toggleTodo"
          @remove="removeTodo"
        />
      </ul>

      <!-- 空状态 -->
      <div v-else class="rounded-xl border border-dashed border-slate-300 bg-white/60 py-12 text-center">
        <p class="text-sm text-slate-400">
          {{ todos.length ? '当前筛选条件下没有待办' : '还没有待办事项，添加一条吧 ✨' }}
        </p>
      </div>

      <!-- 底部操作 -->
      <footer v-if="completedCount" class="mt-5 text-center">
        <button
          type="button"
          class="text-sm text-slate-400 underline-offset-4 transition hover:text-rose-500 hover:underline"
          @click="clearCompleted"
        >
          清除 {{ completedCount }} 条已完成
        </button>
      </footer>
    </main>
  </div>
</template>
