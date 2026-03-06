// Simple composable to fetch dev tasks from workspace 2
import { ref, computed } from "vue";
import { taskService } from "@/services/task.service";
import type { Task } from "@/types/task";

export function useDevTasks() {
  const tasks = ref<Task[]>([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  const fetchTasks = async (projectId?: number, status?: string, assigneeId?: number) => {
    isLoading.value = true;
    error.value = null;

    try {
      const params: { project_id?: number; status?: string; assignee_id?: number } = {};
      if (projectId) params.project_id = projectId;
      if (status) params.status = status;
      if (assigneeId) params.assignee_id = assigneeId;

      tasks.value = await taskService.getTasks(params);
    } catch (err: any) {
      error.value =
        err.response?.data?.detail || err.message || "Failed to load dev tasks";
      console.error("Error fetching dev tasks:", err);
    } finally {
      isLoading.value = false;
    }
  };

  // Group tasks by status
  const tasksByStatus = computed(() => {
    const grouped: Record<string, Task[]> = {
      todo: [],
      in_progress: [],
      in_review: [],
      completed: [],
      blocked: [],
    };

    tasks.value.forEach((task) => {
      if (grouped[task.status]) {
        grouped[task.status].push(task);
      }
    });

    return grouped;
  });

  // Summary stats
  const summary = computed(() => {
    const total = tasks.value.length;
    const completed = tasks.value.filter(
      (t) => t.status === "completed",
    ).length;
    const inProgress = tasks.value.filter(
      (t) => t.status === "in_progress",
    ).length;
    const blocked = tasks.value.filter((t) => t.status === "blocked").length;

    return { total, completed, inProgress, blocked };
  });

  return {
    tasks,
    isLoading,
    error,
    fetchTasks,
    tasksByStatus,
    summary,
  };
}
