<!-- Photo Upload Component -->
<!-- Handle photo upload with preview for field activities -->

<template>
  <div>
    <!-- Upload Area -->
    <div
      @click="triggerFileInput"
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @drop.prevent="handleDrop"
      :class="[
        'relative cursor-pointer rounded-lg border-2 border-dashed p-6 text-center transition-colors',
        isDragging
          ? 'border-blue-500 bg-blue-50'
          : 'border-gray-300 bg-gray-50 hover:bg-gray-100',
        disabled ? 'cursor-not-allowed opacity-50' : '',
      ]"
    >
      <input
        ref="fileInputRef"
        type="file"
        accept="image/*"
        multiple
        :disabled="disabled"
        @change="handleFileSelect"
        class="hidden"
      />

      <svg
        class="mx-auto h-12 w-12 text-gray-400"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
        />
      </svg>

      <p class="mt-2 text-sm font-medium text-gray-700">
        {{
          isDragging ? "Drop photos here" : "Click to upload or drag and drop"
        }}
      </p>
      <p class="mt-1 text-xs text-gray-500">PNG, JPG, GIF up to 10MB each</p>
    </div>

    <!-- Error Message -->
    <p v-if="error" class="mt-2 text-sm text-red-600">{{ error }}</p>

    <!-- Preview Area -->
    <div v-if="previews.length > 0" class="mt-4 space-y-2">
      <h4 class="text-sm font-medium text-gray-700">
        Selected Photos ({{ previews.length }})
      </h4>
      <div class="grid grid-cols-2 gap-2 sm:grid-cols-3 md:grid-cols-4">
        <div
          v-for="(preview, index) in previews"
          :key="index"
          class="group relative aspect-square overflow-hidden rounded-lg border border-gray-200"
        >
          <img
            :src="preview.url"
            :alt="preview.file.name"
            class="h-full w-full object-cover"
          />

          <!-- File Info Overlay -->
          <div
            class="absolute inset-0 flex items-end bg-gradient-to-t from-black/60 to-transparent p-2 opacity-0 transition-opacity group-hover:opacity-100"
          >
            <p class="truncate text-xs text-white">{{ preview.file.name }}</p>
          </div>

          <!-- Remove Button -->
          <button
            @click.stop="removePreview(index)"
            type="button"
            class="absolute right-1 top-1 rounded-full bg-red-500 p-1 text-white opacity-0 shadow-lg transition-opacity hover:bg-red-600 group-hover:opacity-100"
          >
            <svg
              class="h-4 w-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>

          <!-- Upload Progress -->
          <div
            v-if="preview.uploading"
            class="absolute inset-0 flex items-center justify-center bg-black/50"
          >
            <div class="text-center">
              <div
                class="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-white border-r-transparent"
              ></div>
              <p class="mt-1 text-xs text-white">Uploading...</p>
            </div>
          </div>

          <!-- Upload Success -->
          <div
            v-if="preview.uploaded"
            class="absolute inset-0 flex items-center justify-center bg-green-500/80"
          >
            <svg
              class="h-8 w-8 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M5 13l4 4L19 7"
              />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Upload Button -->
    <div
      v-if="previews.length > 0 && !autoUpload"
      class="mt-4 flex justify-end"
    >
      <button
        @click="uploadAll"
        :disabled="uploading || disabled"
        type="button"
        class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
      >
        {{
          uploading
            ? `Uploading... (${uploadProgress}/${previews.length})`
            : `Upload ${previews.length} Photo${previews.length > 1 ? "s" : ""}`
        }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";

interface PhotoPreview {
  file: File;
  url: string;
  uploading: boolean;
  uploaded: boolean;
}

interface Props {
  disabled?: boolean;
  autoUpload?: boolean;
  maxSize?: number; // in bytes, default 10MB
}

interface Emits {
  (e: "upload", files: File[]): void;
  (e: "error", message: string): void;
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false,
  autoUpload: false,
  maxSize: 10 * 1024 * 1024, // 10MB
});

const emit = defineEmits<Emits>();

const fileInputRef = ref<HTMLInputElement | null>(null);
const previews = ref<PhotoPreview[]>([]);
const isDragging = ref(false);
const uploading = ref(false);
const uploadProgress = ref(0);
const error = ref("");

const triggerFileInput = () => {
  if (!props.disabled) {
    fileInputRef.value?.click();
  }
};

const validateFile = (file: File): string | null => {
  if (!file.type.startsWith("image/")) {
    return `${file.name} is not an image file`;
  }

  if (file.size > props.maxSize) {
    const maxMB = props.maxSize / (1024 * 1024);
    return `${file.name} exceeds ${maxMB}MB size limit`;
  }

  return null;
};

const addFiles = (files: FileList | File[]) => {
  error.value = "";
  const fileArray = Array.from(files);

  for (const file of fileArray) {
    const validationError = validateFile(file);
    if (validationError) {
      error.value = validationError;
      emit("error", validationError);
      continue;
    }

    const url = URL.createObjectURL(file);
    previews.value.push({
      file,
      url,
      uploading: false,
      uploaded: false,
    });
  }

  if (props.autoUpload && previews.value.length > 0) {
    uploadAll();
  }
};

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    addFiles(target.files);
    // Reset input to allow selecting the same file again
    target.value = "";
  }
};

const handleDrop = (event: DragEvent) => {
  isDragging.value = false;
  if (props.disabled) return;

  const files = event.dataTransfer?.files;
  if (files && files.length > 0) {
    addFiles(files);
  }
};

const removePreview = (index: number) => {
  const preview = previews.value[index];
  URL.revokeObjectURL(preview.url);
  previews.value.splice(index, 1);
};

const uploadAll = async () => {
  uploading.value = true;
  uploadProgress.value = 0;

  const filesToUpload = previews.value
    .filter((p) => !p.uploaded && !p.uploading)
    .map((p) => p.file);

  if (filesToUpload.length === 0) {
    uploading.value = false;
    return;
  }

  emit("upload", filesToUpload);

  // Mark all as uploading (parent component will handle actual upload)
  previews.value.forEach((p) => {
    if (!p.uploaded) {
      p.uploading = true;
    }
  });
};

// Method to be called by parent after successful upload
const markAsUploaded = (fileName: string) => {
  const preview = previews.value.find((p) => p.file.name === fileName);
  if (preview) {
    preview.uploading = false;
    preview.uploaded = true;
    uploadProgress.value++;

    // Check if all done
    if (uploadProgress.value === previews.value.length) {
      setTimeout(() => {
        previews.value.forEach((p) => URL.revokeObjectURL(p.url));
        previews.value = [];
        uploading.value = false;
        uploadProgress.value = 0;
      }, 1000);
    }
  }
};

// Method to handle upload errors
const markAsError = (fileName: string) => {
  const preview = previews.value.find((p) => p.file.name === fileName);
  if (preview) {
    preview.uploading = false;
    uploadProgress.value++;
  }
};

// Cleanup on unmount
watch(
  () => previews.value,
  (newPreviews, oldPreviews) => {
    if (oldPreviews) {
      oldPreviews.forEach((p) => {
        if (!newPreviews.find((np) => np.url === p.url)) {
          URL.revokeObjectURL(p.url);
        }
      });
    }
  },
);

defineExpose({ markAsUploaded, markAsError });
</script>
