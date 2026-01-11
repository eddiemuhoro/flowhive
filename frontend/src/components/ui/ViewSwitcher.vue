<template>
  <div class="flex items-center bg-gray-100 rounded-md p-1">
    <button
      v-for="view in views"
      :key="view.value"
      @click="$emit('update:modelValue', view.value)"
      :class="['px-3 py-1.5 text-sm font-medium rounded transition-colors',
               modelValue === view.value
                 ? 'bg-white text-gray-900 shadow-sm'
                 : 'text-gray-600 hover:text-gray-900']"
      :title="view.label"
    >
      <component :is="view.icon" class="w-4 h-4" />
    </button>
  </div>
</template>

<script setup lang="ts">
import { h } from 'vue'

interface View {
  value: string
  label: string
  icon: any
}

interface Props {
  modelValue: string
  views: View[]
}

defineProps<Props>()
defineEmits<{
  'update:modelValue': [value: string]
}>()

// Icon components
const BoardIcon = () => h('svg', {
  fill: 'none',
  stroke: 'currentColor',
  viewBox: '0 0 24 24'
}, [
  h('path', {
    'stroke-linecap': 'round',
    'stroke-linejoin': 'round',
    'stroke-width': '2',
    d: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2'
  })
])

const ListIcon = () => h('svg', {
  fill: 'none',
  stroke: 'currentColor',
  viewBox: '0 0 24 24'
}, [
  h('path', {
    'stroke-linecap': 'round',
    'stroke-linejoin': 'round',
    'stroke-width': '2',
    d: 'M4 6h16M4 10h16M4 14h16M4 18h16'
  })
])

const CalendarIcon = () => h('svg', {
  fill: 'none',
  stroke: 'currentColor',
  viewBox: '0 0 24 24'
}, [
  h('path', {
    'stroke-linecap': 'round',
    'stroke-linejoin': 'round',
    'stroke-width': '2',
    d: 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z'
  })
])

// Export for use in parent
export { BoardIcon, ListIcon, CalendarIcon }
</script>
