<!-- Photo Gallery Component -->
<!-- Display and manage photos attached to field activities -->

<template>
  <div>
    <!-- Gallery Grid -->
    <div
      v-if="photos.length > 0"
      class="grid grid-cols-2 gap-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5"
    >
      <div
        v-for="photo in photos"
        :key="photo.id"
        @click="openLightbox(photo)"
        class="group relative aspect-square cursor-pointer overflow-hidden rounded-lg border border-gray-200 bg-gray-100"
      >
        <!-- Photo Image -->
        <img
          :src="getPhotoUrl(photo.file_path)"
          :alt="photo.file_name"
          class="h-full w-full object-cover transition-transform group-hover:scale-110"
          loading="lazy"
        />

        <!-- Overlay on Hover -->
        <div
          class="absolute inset-0 bg-black/0 transition-colors group-hover:bg-black/40"
        ></div>

        <!-- Delete Button -->
        <button
          v-if="canDelete"
          @click.stop="handleDelete(photo.id)"
          type="button"
          class="absolute right-2 top-2 rounded-full bg-red-500 p-1.5 text-white opacity-0 shadow-lg transition-opacity hover:bg-red-600 group-hover:opacity-100"
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
              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
            />
          </svg>
        </button>

        <!-- File Info -->
        <div
          class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/60 to-transparent p-2 opacity-0 transition-opacity group-hover:opacity-100"
        >
          <p class="truncate text-xs text-white">{{ photo.file_name }}</p>
          <p class="text-xs text-gray-300">
            {{ formatFileSize(photo.file_size) }}
          </p>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div
      v-else
      class="rounded-lg border-2 border-dashed border-gray-300 bg-gray-50 p-8 text-center"
    >
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
      <p class="mt-2 text-sm text-gray-600">No photos yet</p>
    </div>

    <!-- Lightbox Modal -->
    <Teleport to="body">
      <div
        v-if="lightboxPhoto"
        @click="closeLightbox"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/90 p-4"
      >
        <button
          @click="closeLightbox"
          class="absolute right-4 top-4 rounded-full bg-white/10 p-2 text-white hover:bg-white/20"
        >
          <svg
            class="h-6 w-6"
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

        <!-- Navigation Arrows -->
        <button
          v-if="photos.length > 1"
          @click.stop="navigatePrevious"
          class="absolute left-4 rounded-full bg-white/10 p-2 text-white hover:bg-white/20"
        >
          <svg
            class="h-6 w-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M15 19l-7-7 7-7"
            />
          </svg>
        </button>

        <button
          v-if="photos.length > 1"
          @click.stop="navigateNext"
          class="absolute right-4 rounded-full bg-white/10 p-2 text-white hover:bg-white/20"
        >
          <svg
            class="h-6 w-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 5l7 7-7 7"
            />
          </svg>
        </button>

        <!-- Main Image -->
        <div @click.stop class="relative max-h-[90vh] max-w-[90vw]">
          <img
            :src="getPhotoUrl(lightboxPhoto.file_path)"
            :alt="lightboxPhoto.file_name"
            class="max-h-[90vh] max-w-[90vw] object-contain"
          />

          <!-- Photo Info -->
          <div
            class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4"
          >
            <p class="text-sm font-medium text-white">
              {{ lightboxPhoto.file_name }}
            </p>
            <p class="text-xs text-gray-300">
              {{ formatFileSize(lightboxPhoto.file_size) }} • Uploaded
              {{ formatDate(lightboxPhoto.uploaded_at) }}
            </p>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import type { FieldActivityPhoto } from "@/types/field";

interface Props {
  photos: FieldActivityPhoto[];
  canDelete?: boolean;
  baseUrl?: string;
}

interface Emits {
  (e: "delete", photoId: number): void;
}

const props = withDefaults(defineProps<Props>(), {
  canDelete: false,
  baseUrl: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

const emit = defineEmits<Emits>();

const lightboxPhoto = ref<FieldActivityPhoto | null>(null);
const currentPhotoIndex = ref(0);

const getPhotoUrl = (filePath: string): string => {
  // Construct full URL for photo
  // Adjust this based on your backend's static file serving
  return `${props.baseUrl}/uploads/${filePath}`;
};

const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};

const formatDate = (dateStr: string): string => {
  const date = new Date(dateStr);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffMins < 1) return "just now";
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;

  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
};

const openLightbox = (photo: FieldActivityPhoto) => {
  lightboxPhoto.value = photo;
  currentPhotoIndex.value = props.photos.findIndex((p) => p.id === photo.id);
};

const closeLightbox = () => {
  lightboxPhoto.value = null;
};

const navigateNext = () => {
  currentPhotoIndex.value = (currentPhotoIndex.value + 1) % props.photos.length;
  lightboxPhoto.value = props.photos[currentPhotoIndex.value];
};

const navigatePrevious = () => {
  currentPhotoIndex.value =
    (currentPhotoIndex.value - 1 + props.photos.length) % props.photos.length;
  lightboxPhoto.value = props.photos[currentPhotoIndex.value];
};

const handleDelete = (photoId: number) => {
  if (confirm("Are you sure you want to delete this photo?")) {
    emit("delete", photoId);
  }
};

// Keyboard navigation in lightbox
const handleKeydown = (event: KeyboardEvent) => {
  if (!lightboxPhoto.value) return;

  if (event.key === "Escape") {
    closeLightbox();
  } else if (event.key === "ArrowRight") {
    navigateNext();
  } else if (event.key === "ArrowLeft") {
    navigatePrevious();
  }
};

// Add keyboard listener
if (typeof window !== "undefined") {
  window.addEventListener("keydown", handleKeydown);
}
</script>
