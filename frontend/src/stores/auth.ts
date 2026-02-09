import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { authService } from "@/services/auth.service";
import type { User, LoginRequest, RegisterRequest } from "@/types/auth";

export const useAuthStore = defineStore("auth", () => {
  const user = ref<User | null>(null);
  const token = ref<string | null>(localStorage.getItem("access_token"));
  const loading = ref(false);
  const error = ref<string | null>(null);

  const isAuthenticated = computed(() => !!token.value && !!user.value);
  const isExecutive = computed(() => user.value?.role === "executive");
  const isManager = computed(
    () => user.value?.role === "manager" || isExecutive.value,
  );

  async function login(credentials: LoginRequest) {
    try {
      loading.value = true;
      error.value = null;

      // Call backend API
      const response = await authService.login(credentials);
      token.value = response.access_token;
      localStorage.setItem("access_token", response.access_token);

      // Fetch current user data
      await fetchCurrentUser();
    } catch (err: any) {
      error.value = err.response?.data?.detail || "Login failed";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function register(data: RegisterRequest) {
    try {
      loading.value = true;
      error.value = null;

      await authService.register(data);

      // Auto login after registration
      await login({
        username: data.username,
        password: data.password,
      });
    } catch (err: any) {
      error.value = err.response?.data?.detail || "Registration failed";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function fetchCurrentUser() {
    try {
      user.value = await authService.getCurrentUser();
    } catch (err: any) {
      error.value = err.response?.data?.detail || "Failed to fetch user";
      logout();
      throw err;
    }
  }

  async function logout() {
    user.value = null;
    token.value = null;
    localStorage.removeItem("access_token");

    // Clear workspace data
    try {
      const { useWorkspaceStore } = await import("./workspace");
      const workspaceStore = useWorkspaceStore();
      workspaceStore.clearWorkspace();
    } catch (err) {
      console.error("Failed to clear workspace on logout:", err);
    }
  }

  async function initialize() {
    if (token.value) {
      try {
        await fetchCurrentUser();
      } catch (err: any) {
        // Only logout on authentication errors (401), not network errors
        if (err.response?.status === 401) {
          console.log("Token expired or invalid, logging out");
          logout();
        } else {
          console.error("Failed to fetch user, but keeping token:", err);
          // Keep the token, will retry on next navigation
        }
      }
    }
  }

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    isExecutive,
    isManager,
    login,
    register,
    logout,
    fetchCurrentUser,
    initialize,
  };
});
