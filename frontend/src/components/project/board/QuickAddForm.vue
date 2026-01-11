<template>
  <div v-if="show" class="mb-2 space-y-2">
    <input
      v-model="title"
      @keyup.enter="handleSubmit"
      @keyup.esc="handleCancel"
      type="text"
      placeholder="Task title..."
      :class="['w-full px-3 py-2 text-sm rounded focus:outline-none focus:ring-2', inputClasses]"
      autofocus
    />
    <input
      v-model="dueDate"
      @keyup.enter="handleSubmit"
      @keyup.esc="handleCancel"
      type="date"
      :class="['w-full px-3 py-2 text-sm rounded focus:outline-none focus:ring-2', inputClasses]"
    />
    <div class="flex gap-2">
      <button
        @click="handleSubmit"
        :class="['flex-1 px-3 py-1.5 text-xs font-medium text-white rounded transition', buttonClasses]"
      >
        Add Task
      </button>
      <button
        @click="handleCancel"
        class="px-3 py-1.5 text-xs font-medium text-gray-600 bg-gray-100 rounded hover:bg-gray-200 transition"
      >
        Cancel
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

interface Props {
  show: boolean
  status: string
  inputClasses?: string
  buttonClasses?: string
}

const props = withDefaults(defineProps<Props>(), {
  inputClasses: 'border border-gray-300 focus:ring-primary-500 focus:border-primary-500',
  buttonClasses: 'bg-primary-600 hover:bg-primary-700'
})

const emit = defineEmits<{
  submit: [title: string, dueDate: string]
  cancel: []
}>()

const title = ref('')
const dueDate = ref('')

// Clear inputs when form is hidden
watch(() => props.show, (newShow) => {
  if (!newShow) {
    title.value = ''
    dueDate.value = ''
  }
})

const handleSubmit = () => {
  if (!title.value.trim()) return
  emit('submit', title.value.trim(), dueDate.value)
  title.value = ''
  dueDate.value = ''
}

const handleCancel = () => {
  title.value = ''
  dueDate.value = ''
  emit('cancel')
}
</script>
