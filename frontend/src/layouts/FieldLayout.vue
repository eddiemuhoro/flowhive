<!-- Field Operations Layout -->
<!-- Mobile-first layout for field workers with simplified navigation -->

<template>
  <div class="flex h-screen bg-gray-50">
    <!-- Desktop Sidebar -->
    <aside
      class="hidden lg:flex lg:w-64 lg:flex-col lg:bg-white lg:border-r lg:border-gray-200"
    >
      <!-- Sidebar Header -->
      <div class="flex h-16 items-center border-b border-gray-200 px-4">
        <div class="flex items-center space-x-2">
          <div
            class="flex h-8 w-8 items-center justify-center rounded bg-blue-600"
          >
            <svg
              class="h-5 w-5 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
          </div>
          <span class="text-lg font-semibold text-gray-900">Field Ops</span>
        </div>
      </div>

      <!-- Workspace Switcher -->
      <div class="border-b border-gray-200 p-4">
        <WorkspaceSwitcher />
      </div>

      <!-- Navigation Links -->
      <nav class="flex-1 space-y-1 overflow-y-auto p-4">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="group flex items-center rounded-lg px-3 py-2.5 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-100 hover:text-gray-900"
          active-class="bg-blue-50 text-blue-600 hover:bg-blue-50 hover:text-blue-600"
        >
          <component :is="item.icon" class="mr-3 h-5 w-5 flex-shrink-0" />
          {{ item.label }}
        </router-link>
      </nav>

      <!-- Settings & User -->
      <div class="border-t border-gray-200 p-4 space-y-1">
        <button
          v-if="canManage"
          @click="navigateToSettings"
          class="group flex w-full items-center rounded-lg px-3 py-2.5 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-100"
        >
          <svg
            class="mr-3 h-5 w-5 flex-shrink-0"
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
          Settings
        </button>

        <div class="relative">
          <button
            @click="toggleUserMenu"
            class="group flex w-full items-center rounded-lg px-3 py-2.5 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-100"
          >
            <div
              class="mr-3 flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-blue-500 text-sm font-medium text-white"
            >
              {{ userInitials }}
            </div>
            <div class="flex-1 truncate text-left">
              <p class="truncate text-sm font-medium text-gray-900">
                {{ user?.full_name || user?.username }}
              </p>
              <p class="truncate text-xs text-gray-500">{{ user?.email }}</p>
            </div>
          </button>

          <!-- User Dropdown -->
          <div
            v-if="showUserMenu"
            class="absolute bottom-full left-0 mb-2 w-full rounded-lg border border-gray-200 bg-white py-1 shadow-lg"
          >
            <button
              @click="handleLogout"
              class="flex w-full items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              <svg
                class="mr-3 h-4 w-4"
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
              Logout
            </button>
          </div>
        </div>
      </div>
    </aside>

    <!-- Mobile/Desktop Content Area -->
    <div class="flex flex-1 flex-col overflow-hidden">
      <!-- Mobile Header -->
      <header class="bg-white border-b border-gray-200 lg:hidden">
        <div class="flex items-center justify-between px-4 py-3">
          <button
            @click="toggleMenu"
            class="rounded-lg p-2 text-gray-600 hover:bg-gray-100"
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

          <button
            @click="toggleUserMenu"
            class="rounded-lg p-2 hover:bg-gray-100"
          >
            <div
              class="flex h-8 w-8 items-center justify-center rounded-full bg-blue-500 text-sm font-medium text-white"
            >
              {{ userInitials }}
            </div>
          </button>
        </div>
      </header>

      <!-- Main Content -->
      <main class="flex-1 overflow-y-auto">
        <router-view />
      </main>

      <!-- Mobile Bottom Navigation -->
      <nav class="border-t border-gray-200 bg-white lg:hidden">
        <div class="flex items-center justify-around">
          <router-link
            v-for="item in mobileNavItems"
            :key="item.path"
            :to="item.path"
            class="flex flex-1 flex-col items-center py-3 text-xs font-medium text-gray-600 hover:text-gray-900"
            active-class="text-blue-600"
          >
            <component :is="item.icon" class="mb-1 h-6 w-6" />
            {{ item.label }}
          </router-link>
        </div>
      </nav>
    </div>

    <!-- Mobile Sidebar Overlay -->
    <div
      v-if="showMenu"
      class="fixed inset-0 z-50 lg:hidden"
      @click="toggleMenu"
    >
      <div class="absolute inset-0 bg-black bg-opacity-50"></div>
      <aside
        class="absolute inset-y-0 left-0 w-64 bg-white shadow-xl"
        @click.stop
      >
        <div class="flex h-full flex-col">
          <!-- Mobile Sidebar Header -->
          <div
            class="flex h-16 items-center justify-between border-b border-gray-200 px-4"
          >
            <div class="flex items-center space-x-2">
              <div
                class="flex h-8 w-8 items-center justify-center rounded bg-blue-600"
              >
                <svg
                  class="h-5 w-5 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
              </div>
              <span class="text-lg font-semibold text-gray-900">Field Ops</span>
            </div>
            <button
              @click="toggleMenu"
              class="rounded-lg p-2 text-gray-600 hover:bg-gray-100"
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
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>

          <!-- Workspace Switcher -->
          <div class="border-b border-gray-200 p-4">
            <WorkspaceSwitcher />
          </div>

          <!-- Mobile Navigation Links -->
          <nav class="flex-1 space-y-1 overflow-y-auto p-4">
            <router-link
              v-for="item in navItems"
              :key="item.path"
              :to="item.path"
              @click="showMenu = false"
              class="group flex items-center rounded-lg px-3 py-2.5 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-100"
              active-class="bg-blue-50 text-blue-600"
            >
              <component :is="item.icon" class="mr-3 h-5 w-5 flex-shrink-0" />
              {{ item.label }}
            </router-link>
          </nav>

          <!-- Mobile Settings & User -->
          <div class="border-t border-gray-200 p-4 space-y-1">
            <button
              v-if="canManage"
              @click="navigateToSettings"
              class="flex w-full items-center rounded-lg px-3 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-100"
            >
              <svg
                class="mr-3 h-5 w-5 flex-shrink-0"
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
              Settings
            </button>

            <button
              @click="handleLogout"
              class="flex w-full items-center rounded-lg px-3 py-2.5 text-sm font-medium text-red-600 hover:bg-red-50"
            >
              <svg
                class="mr-3 h-5 w-5 flex-shrink-0"
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
              Logout
            </button>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, h } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useWorkspaceStore } from "@/stores/workspace";
import WorkspaceSwitcher from "@/components/ui/WorkspaceSwitcher.vue";

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

// SVG Icon Components
const DashboardIcon = () =>
  h(
    "svg",
    {
      class: "h-5 w-5",
      fill: "none",
      stroke: "currentColor",
      viewBox: "0 0 24 24",
    },
    [
      h("path", {
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
        "stroke-width": "2",
        d: "M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6",
      }),
    ],
  );

const ActivityIcon = () =>
  h(
    "svg",
    {
      class: "h-5 w-5",
      fill: "none",
      stroke: "currentColor",
      viewBox: "0 0 24 24",
    },
    [
      h("path", {
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
        "stroke-width": "2",
        d: "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z",
      }),
    ],
  );

const AnalyticsIcon = () =>
  h(
    "svg",
    {
      class: "h-5 w-5",
      fill: "none",
      stroke: "currentColor",
      viewBox: "0 0 24 24",
    },
    [
      h("path", {
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
        "stroke-width": "2",
        d: "M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z",
      }),
    ],
  );

const navItems = computed(() => {
  const items = [
    {
      path: "/field",
      label: "Dashboard",
      icon: DashboardIcon,
    },
    {
      path: "/field/activities",
      label: "Activity Log",
      icon: ActivityIcon,
    },
    {
      path: "/field/minutes",
      label: "Minutes",
      icon: ActivityIcon,
    },
  ];

  if (canManage.value) {
    items.push({
      path: "/field/analytics",
      label: "Analytics",
      icon: AnalyticsIcon,
    });
  }

  return items;
});

// Mobile bottom navigation (shows all items)
const mobileNavItems = computed(() => {
  const items = [
    {
      path: "/field",
      label: "Home",
      icon: DashboardIcon,
    },
    {
      path: "/field/activities",
      label: "Activities",
      icon: ActivityIcon,
    },
  ];

  if (canManage.value) {
    items.push({
      path: "/field/analytics",
      label: "Analytics",
      icon: AnalyticsIcon,
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
