<!-- Category Badge Component -->
<!-- Displays a task category with color and icon -->

<template>
  <span
    v-if="category"
    :class="[
      'inline-flex items-center rounded-full px-3 py-1 text-xs font-medium',
      badgeClasses,
    ]"
    :style="badgeStyle"
  >
    <span v-if="category.icon" class="mr-1">{{ category.icon }}</span>
    <span>{{ showTitle ? category.title : category.name }}</span>
  </span>
  <span
    v-else
    class="inline-flex items-center rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-600"
  >
    No Category
  </span>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { TaskCategory } from "@/types/field";

interface Props {
  category: TaskCategory | null | undefined;
  showTitle?: boolean;
  variant?: "solid" | "outlined" | "light";
}

const props = withDefaults(defineProps<Props>(), {
  showTitle: true,
  variant: "light",
});

/**
 * Convert hex color to RGB values
 */
const hexToRgb = (hex: string): { r: number; g: number; b: number } | null => {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result
    ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16),
      }
    : null;
};

/**
 * Get contrasting text color (black or white) based on background
 */
const getContrastColor = (hexColor: string): string => {
  const rgb = hexToRgb(hexColor);
  if (!rgb) return "#000000";

  // Calculate luminance
  const luminance = (0.299 * rgb.r + 0.587 * rgb.g + 0.114 * rgb.b) / 255;
  return luminance > 0.5 ? "#000000" : "#ffffff";
};

const badgeStyle = computed(() => {
  if (!props.category?.color) return {};

  const color = props.category.color;

  if (props.variant === "solid") {
    return {
      backgroundColor: color,
      color: getContrastColor(color),
    };
  } else if (props.variant === "outlined") {
    return {
      borderColor: color,
      color: color,
      borderWidth: "1px",
      borderStyle: "solid",
      backgroundColor: "transparent",
    };
  } else {
    // light variant
    const rgb = hexToRgb(color);
    if (rgb) {
      return {
        backgroundColor: `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, 0.1)`,
        color: color,
      };
    }
  }

  return {};
});

const badgeClasses = computed(() => {
  return {
    border: props.variant === "outlined",
  };
});
</script>
