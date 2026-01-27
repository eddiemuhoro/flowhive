<!-- Field Operations Layout -->
<!-- Mobile-first layout for field workers with simplified navigation -->

<template>
  <div class="flex h-screen flex-col bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm">
      <div class="flex items-center justify-between px-4 py-3">
        <!-- Logo / Workspace Name -->
        <div class="flex items-center space-x-3">
          <button
            @click="toggleMenu"
            class="rounded-lg p-2 text-gray-600 hover:bg-gray-100 lg:hidden"
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
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </button>
          <h1 class="text-lg font-semibold text-gray-900">
            {{ currentWorkspace?.name || "Field Operations" }}
          </h1>
        </div>

        <!-- User Menu -->
        <div class="flex items-center space-x-2">
          <button
            @click="toggleUserMenu"
            class="flex items-center space-x-2 rounded-lg px-3 py-2 hover:bg-gray-100"
          >
            <div
              class="flex h-8 w-8 items-center justify-center rounded-full bg-blue-500 text-white text-sm font-medium"
            >
              {{ userInitials }}
            </div>
            <span class="hidden text-sm font-medium text-gray-700 sm:block">{{
              user?.full_name || user?.username
            }}</span>
          </button>
        </div>
      </div>
    </header>

    <!-- Mobile Menu Overlay -->
    <div
      v-if="showMenu"
      class="fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden"
      @click="toggleMenu"
    ></div>

    <!-- Sidebar Navigation -->
    <aside
      :class="[
        'fixed inset-y-0 left-0 z-50 w-64 transform bg-white shadow-lg transition-transform lg:relative lg:translate-x-0',
        showMenu ? 'translate-x-0' : '-translate-x-full',
      ]"
    >
      <nav class="flex h-full flex-col p-4">
        <!-- Navigation Links -->
        <div class="space-y-2">
          <router-link
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="flex items-center space-x-3 rounded-lg px-3 py-2 text-gray-700 hover:bg-gray-100"
            active-class="bg-blue-50 text-blue-600 hover:bg-blue-50"
            @click="showMenu = false"
          >
            <component :is="item.icon" class="h-5 w-5" />
            <span class="font-medium">{{ item.label }}</span>
          </router-link>
        </div>

        <!-- Bottom Actions -->
        <div class="mt-auto space-y-2 border-t pt-4">
          <button
            v-if="canManage"
            @click="navigateToSettings"
            class="flex w-full items-center space-x-3 rounded-lg px-3 py-2 text-gray-700 hover:bg-gray-100"
          >
            <svg
              class="h-5 w-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
              />
            </svg>
            <span class="font-medium">Settings</span>
          </button>
          <button
            @click="handleLogout"
            class="flex w-full items-center space-x-3 rounded-lg px-3 py-2 text-red-600 hover:bg-red-50"
          >
            <svg
              class="h-5 w-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
              />
            </svg>
            <span class="font-medium">Logout</span>
          </button>
        </div>
      </nav>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-auto">
      <router-view />
    </main>

    <!-- User Menu Dropdown -->
    <div
      v-if="showUserMenu"
      class="fixed right-4 top-16 z-50 w-64 rounded-lg bg-white shadow-lg"
    >
      <div class="p-4">
        <p class="text-sm font-medium text-gray-900">
          {{ user?.full_name || user?.username }}
        </p>
        <p class="text-xs text-gray-500">{{ user?.email }}</p>
        <p class="mt-2 text-xs text-gray-400">
          Role: {{ user?.role || "Team Member" }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useWorkspaceStore } from "@/stores/workspace";

const router = useRouter();
const authStore = useAuthStore();
const workspaceStore = useWorkspaceStore();

const showMenu = ref(false);
const showUserMenu = ref(false);

const user = computed(() => authStore.user);
const currentWorkspace = computed(() => workspaceStore.currentWorkspace);
const canManage = computed(() => {
  const role = user.value?.role?.toUpperCase();
  return role === "MANAGER" || role === "EXECUTIVE";
});

const userInitials = computed(() => {
  if (user.value?.full_name) {
    return user.value.full_name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase()
      .substring(0, 2);
  }
  return user.value?.username?.substring(0, 2).toUpperCase() || "U";
});

const navItems = computed(() => {
  const items = [
    {
      path: "/field",
      label: "Dashboard",
      icon: "svg", // Will be component
    },
    {
      path: "/field/activities",
      label: "Activity Log",
      icon: "svg",
    },
  ];

  if (canManage.value) {
    items.push({
      path: "/field/analytics",
      label: "Analytics",
      icon: "svg",
    });
  }

  return items;
});

const toggleMenu = () => {
  showMenu.value = !showMenu.value;
};

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value;
};

const navigateToSettings = () => {
  router.push("/field/settings");
  showMenu.value = false;
};

const handleLogout = async () => {
  await authStore.logout();
  router.push("/login");
};
</script>
