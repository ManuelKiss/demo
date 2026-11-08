<script setup lang="ts">
import type { Todo } from '../types'

defineProps<{ todo: Todo }>()
defineEmits<{
  toggle: [id: string]
  remove: [id: string]
}>()
</script>

<template>
  <li
    class="group flex items-center gap-3 rounded-xl border border-slate-200 bg-white px-4 py-3 shadow-sm transition hover:shadow-md"
  >
    <!-- 完成状态复选框 -->
    <button
      type="button"
      class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full border-2 transition"
      :class="
        todo.completed
          ? 'border-emerald-500 bg-emerald-500 text-white'
          : 'border-slate-300 text-transparent hover:border-emerald-400'
      "
      :aria-label="todo.completed ? '标记为未完成' : '标记为已完成'"
      @click="$emit('toggle', todo.id)"
    >
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" class="h-4 w-4">
        <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
      </svg>
    </button>

    <!-- 待办内容：完成时显示删除线 -->
    <span
      class="flex-1 break-words text-sm transition"
      :class="todo.completed ? 'text-slate-400 line-through' : 'text-slate-700'"
    >
      {{ todo.text }}
    </span>

    <!-- 删除按钮：悬停列表项时显示 -->
    <button
      type="button"
      class="rounded-lg p-1.5 text-slate-300 opacity-0 transition group-hover:opacity-100 hover:bg-rose-50 hover:text-rose-500 focus:opacity-100"
      aria-label="删除待办"
      @click="$emit('remove', todo.id)"
    >
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="h-5 w-5">
        <path stroke-linecap="round" stroke-linejoin="round" d="M6 7h12M9 7V5a1 1 0 011-1h4a1 1 0 011 1v2m1 0l-.8 12a2 2 0 01-2 1.9H9.8a2 2 0 01-2-1.9L7 7" />
      </svg>
    </button>
  </li>
</template>
