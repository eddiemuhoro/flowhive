<!-- Rich Text Editor Component -->
<!-- WYSIWYG editor using Tiptap for formatted content -->

<template>
  <div class="rich-text-editor">
    <!-- Toolbar -->
    <div
      v-if="editor"
      class="toolbar flex flex-wrap items-center gap-1 rounded-t-lg border border-gray-300 bg-gray-50 p-2"
      :class="{ 'border-red-300': error }"
    >
      <!-- Bold -->
      <button
        type="button"
        @click="editor.chain().focus().toggleBold().run()"
        :class="{ 'is-active': editor.isActive('bold') }"
        class="toolbar-btn"
        title="Bold (Ctrl+B)"
      >
        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 4h8a4 4 0 014 4 4 4 0 01-4 4H6z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 12h9a4 4 0 014 4 4 4 0 01-4 4H6z" />
        </svg>
      </button>

      <!-- Italic -->
      <button
        type="button"
        @click="editor.chain().focus().toggleItalic().run()"
        :class="{ 'is-active': editor.isActive('italic') }"
        class="toolbar-btn"
        title="Italic (Ctrl+I)"
      >
        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m-4 4h8m-8 8h8" />
        </svg>
      </button>

      <!-- Underline -->
      <button
        type="button"
        @click="editor.chain().focus().toggleUnderline().run()"
        :class="{ 'is-active': editor.isActive('underline') }"
        class="toolbar-btn"
        title="Underline (Ctrl+U)"
      >
        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 3v10a5 5 0 0010 0V3M4 21h16" />
        </svg>
      </button>

      <div class="mx-1 h-6 w-px bg-gray-300"></div>

      <!-- Heading 1 -->
      <button
        type="button"
        @click="editor.chain().focus().toggleHeading({ level: 1 }).run()"
        :class="{ 'is-active': editor.isActive('heading', { level: 1 }) }"
        class="toolbar-btn"
        title="Heading 1"
      >
        H1
      </button>

      <!-- Heading 2 -->
      <button
        type="button"
        @click="editor.chain().focus().toggleHeading({ level: 2 }).run()"
        :class="{ 'is-active': editor.isActive('heading', { level: 2 }) }"
        class="toolbar-btn"
        title="Heading 2"
      >
        H2
      </button>

      <!-- Heading 3 -->
      <button
        type="button"
        @click="editor.chain().focus().toggleHeading({ level: 3 }).run()"
        :class="{ 'is-active': editor.isActive('heading', { level: 3 }) }"
        class="toolbar-btn"
        title="Heading 3"
      >
        H3
      </button>

      <div class="mx-1 h-6 w-px bg-gray-300"></div>

      <!-- Bullet List -->
      <button
        type="button"
        @click="editor.chain().focus().toggleBulletList().run()"
        :class="{ 'is-active': editor.isActive('bulletList') }"
        class="toolbar-btn"
        title="Bullet List"
      >
        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>

      <!-- Ordered List -->
      <button
        type="button"
        @click="editor.chain().focus().toggleOrderedList().run()"
        :class="{ 'is-active': editor.isActive('orderedList') }"
        class="toolbar-btn"
        title="Numbered List"
      >
        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5h12M9 12h12M9 19h12M3 5v4m0 0l2-2m-2 2L1 7m2 9v4m0 0l2-2m-2 2l-2-2" />
        </svg>
      </button>

      <div class="mx-1 h-6 w-px bg-gray-300"></div>

      <!-- Blockquote -->
      <button
        type="button"
        @click="editor.chain().focus().toggleBlockquote().run()"
        :class="{ 'is-active': editor.isActive('blockquote') }"
        class="toolbar-btn"
        title="Quote"
      >
        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
      </button>

      <!-- Horizontal Rule -->
      <button
        type="button"
        @click="editor.chain().focus().setHorizontalRule().run()"
        class="toolbar-btn"
        title="Horizontal Line"
      >
        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 12h16" />
        </svg>
      </button>

      <div class="mx-1 h-6 w-px bg-gray-300"></div>

      <!-- Undo -->
      <button
        type="button"
        @click="editor.chain().focus().undo().run()"
        :disabled="!editor.can().undo()"
        class="toolbar-btn"
        title="Undo (Ctrl+Z)"
      >
        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" />
        </svg>
      </button>

      <!-- Redo -->
      <button
        type="button"
        @click="editor.chain().focus().redo().run()"
        :disabled="!editor.can().redo()"
        class="toolbar-btn"
        title="Redo (Ctrl+Y)"
      >
        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 10h-10a8 8 0 00-8 8v2m18-10l-6 6m6-6l-6-6" />
        </svg>
      </button>

      <div class="mx-1 h-6 w-px bg-gray-300"></div>

      <!-- Clear Formatting -->
      <button
        type="button"
        @click="editor.chain().focus().clearNodes().unsetAllMarks().run()"
        class="toolbar-btn"
        title="Clear Formatting"
      >
        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- Editor Content -->
    <editor-content
      :editor="editor"
      class="editor-content rounded-b-lg border border-t-0 border-gray-300 px-3 py-2 focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500"
      :class="{ 'border-red-300': error }"
    />

    <!-- Error Message -->
    <p v-if="error" class="mt-1 text-sm text-red-600">
      {{ error }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { watch, onBeforeUnmount } from "vue";
import { useEditor, EditorContent } from "@tiptap/vue-3";
import StarterKit from "@tiptap/starter-kit";
import Underline from "@tiptap/extension-underline";

interface Props {
  modelValue: string;
  placeholder?: string;
  error?: string;
  minHeight?: string;
}

interface Emits {
  (e: "update:modelValue", value: string): void;
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: "Start typing...",
  minHeight: "150px",
});

const emit = defineEmits<Emits>();

const editor = useEditor({
  content: props.modelValue,
  extensions: [
    StarterKit.configure({
      heading: {
        levels: [1, 2, 3],
      },
    }),
    Underline,
  ],
  editorProps: {
    attributes: {
      class: "prose prose-sm max-w-none focus:outline-none",
      style: `min-height: ${props.minHeight}`,
    },
  },
  onUpdate: ({ editor }) => {
    const html = editor.getHTML();
    // Only emit if content is not just empty paragraph
    if (html === "<p></p>") {
      emit("update:modelValue", "");
    } else {
      emit("update:modelValue", html);
    }
  },
});

// Watch for external changes to modelValue
watch(
  () => props.modelValue,
  (newValue) => {
    if (editor.value) {
      const currentContent = editor.value.getHTML();
      // Only update if the content is actually different
      if (currentContent !== newValue && newValue !== currentContent) {
        editor.value.commands.setContent(newValue || "");
      }
    }
  }
);

onBeforeUnmount(() => {
  if (editor.value) {
    editor.value.destroy();
  }
});
</script>

<style scoped>
/* Toolbar Button Styles */
.toolbar-btn {
  @apply rounded px-2 py-1 text-gray-700 hover:bg-gray-200 disabled:cursor-not-allowed disabled:opacity-50;
}

.toolbar-btn.is-active {
  @apply bg-blue-100 text-blue-700;
}

/* Editor Content Styles */
:deep(.ProseMirror) {
  outline: none;
  min-height: 150px;
  padding: 0.5rem;
}

:deep(.ProseMirror p) {
  margin: 0.5rem 0;
}

:deep(.ProseMirror p:first-child) {
  margin-top: 0;
}

:deep(.ProseMirror p:last-child) {
  margin-bottom: 0;
}

:deep(.ProseMirror h1) {
  font-size: 1.875rem;
  font-weight: 700;
  margin: 1rem 0 0.5rem;
  line-height: 1.25;
}

:deep(.ProseMirror h2) {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0.875rem 0 0.5rem;
  line-height: 1.3;
}

:deep(.ProseMirror h3) {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0.75rem 0 0.5rem;
  line-height: 1.4;
}

:deep(.ProseMirror ul),
:deep(.ProseMirror ol) {
  padding-left: 1.5rem;
  margin: 0.5rem 0;
}

:deep(.ProseMirror ul) {
  list-style-type: disc;
}

:deep(.ProseMirror ol) {
  list-style-type: decimal;
}

:deep(.ProseMirror li) {
  margin: 0.25rem 0;
}

:deep(.ProseMirror blockquote) {
  border-left: 3px solid #e5e7eb;
  padding-left: 1rem;
  margin: 0.5rem 0;
  color: #6b7280;
  font-style: italic;
}

:deep(.ProseMirror hr) {
  border: none;
  border-top: 2px solid #e5e7eb;
  margin: 1rem 0;
}

:deep(.ProseMirror strong) {
  font-weight: 700;
}

:deep(.ProseMirror em) {
  font-style: italic;
}

:deep(.ProseMirror u) {
  text-decoration: underline;
}

/* Placeholder */
:deep(.ProseMirror p.is-editor-empty:first-child::before) {
  content: attr(data-placeholder);
  float: left;
  color: #9ca3af;
  pointer-events: none;
  height: 0;
}
</style>
