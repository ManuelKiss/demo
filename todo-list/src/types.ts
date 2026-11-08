/** 单条待办事项的数据结构 */
export interface Todo {
  /** 唯一标识（UUID，避免同毫秒添加时冲突） */
  id: string
  /** 待办内容 */
  text: string
  /** 是否已完成 */
  completed: boolean
}

/** 列表筛选状态 */
export type Filter = 'all' | 'active' | 'completed'
