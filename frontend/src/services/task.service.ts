import { apiClient } from "./api";
import type { Task, TaskDetail, Comment, Attachment } from "@/types/task";

export const taskService = {
  async getTasks(params?: {
    project_id?: number;
    assignee_id?: number;
    status?: string;
  }): Promise<Task[]> {
    const response = await apiClient.get<Task[]>("/tasks", { params });
    return response.data;
  },

  async getMyTasks(status?: string): Promise<Task[]> {
    const response = await apiClient.get<Task[]>("/tasks/my-tasks", {
      params: status ? { status } : undefined,
    });
    return response.data;
  },

  async getTask(id: number): Promise<TaskDetail> {
    const response = await apiClient.get<TaskDetail>(`/tasks/${id}`);
    return response.data;
  },

  async createTask(data: Partial<Task>): Promise<Task> {
    const response = await apiClient.post<Task>("/tasks", data);
    return response.data;
  },

  async updateTask(id: number, data: Partial<Task>): Promise<Task> {
    const response = await apiClient.patch<Task>(`/tasks/${id}`, data);
    return response.data;
  },

  async deleteTask(id: number): Promise<void> {
    await apiClient.delete(`/tasks/${id}`);
  },

  async getSubtasks(taskId: number): Promise<Task[]> {
    const response = await apiClient.get<Task[]>(`/tasks/${taskId}/subtasks`);
    return response.data;
  },

  async createTasksFromGithub(
    projectId: number,
    repoOwner: string,
    repoName: string,
    commitShas?: string[],
    since?: string,
  ): Promise<Task[]> {
    const params: Record<string, any> = {
      project_id: projectId.toString(),
      repo_owner: repoOwner,
      repo_name: repoName,
    };
    if (since) {
      params.since = since;
    }
    if (commitShas && commitShas.length > 0) {
      params.commit_shas = commitShas;
    }
    const response = await apiClient.post<Task[]>(
      "/tasks/create-tasks-from-github",
      null,
      {
        params,
        paramsSerializer: {
          indexes: null // this tells axios not to use brackets for arrays!
        }
      },
    );
    return response.data;
  },

  async getGithubCommits(
    repoOwner: string,
    repoName: string,
    since?: string,
  ): Promise<any[]> {
    const params: Record<string, string> = {
      repo_owner: repoOwner,
      repo_name: repoName,
    };
    if (since) {
      params.since = since;
    }
    const response = await apiClient.get("/tasks/github-commits", { params });
    return response.data;
  },

  async getGithubRepos(): Promise<any[]> {
    const response = await apiClient.get("/tasks/github-repos");
    return response.data;
  },
};

export const commentService = {
  async getTaskComments(taskId: number): Promise<Comment[]> {
    const response = await apiClient.get<Comment[]>(`/comments/task/${taskId}`);
    return response.data;
  },

  async createComment(data: Partial<Comment>): Promise<Comment> {
    const response = await apiClient.post<Comment>("/comments", data);
    return response.data;
  },

  async updateComment(id: number, content: string): Promise<Comment> {
    const response = await apiClient.patch<Comment>(`/comments/${id}`, {
      content,
    });
    return response.data;
  },

  async deleteComment(id: number): Promise<void> {
    await apiClient.delete(`/comments/${id}`);
  },
};

export const attachmentService = {
  async getTaskAttachments(taskId: number): Promise<Attachment[]> {
    const response = await apiClient.get<Attachment[]>(
      `/attachments/task/${taskId}`,
    );
    return response.data;
  },

  async uploadAttachment(taskId: number, file: File): Promise<Attachment> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await apiClient.post<Attachment>(
      `/attachments?task_id=${taskId}`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      },
    );
    return response.data;
  },

  async deleteAttachment(id: number): Promise<void> {
    await apiClient.delete(`/attachments/${id}`);
  },
};
