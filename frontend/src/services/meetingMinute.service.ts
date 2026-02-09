// Meeting Minutes Service
import type {
  MeetingMinute,
  MeetingMinuteDetail,
  MeetingMinuteCreate,
  MeetingMinuteUpdate,
  MeetingMinuteFilters,
  MinuteAttachment,
  ActionItem,
  ActionItemCreate,
  ActionItemUpdate,
} from "@/types/meetingMinute";
import { apiClient } from "./api";

export const meetingMinuteService = {
  /**
   * Get all meeting minutes for a workspace
   */
  async getWorkspaceMinutes(
    workspaceId: number,
    filters?: MeetingMinuteFilters,
  ): Promise<MeetingMinute[]> {
    const response = await apiClient.get<MeetingMinute[]>(
      `/meeting-minutes/workspace/${workspaceId}`,
      { params: filters },
    );
    return response.data;
  },

  /**
   * Get a single meeting minute with full details
   */
  async getMinute(minuteId: number): Promise<MeetingMinuteDetail> {
    const response = await apiClient.get<MeetingMinuteDetail>(
      `/meeting-minutes/${minuteId}`,
    );
    return response.data;
  },

  /**
   * Create a new meeting minute
   */
  async createMinute(data: MeetingMinuteCreate): Promise<MeetingMinuteDetail> {
    const response = await apiClient.post<MeetingMinuteDetail>(
      "/meeting-minutes",
      data,
    );
    return response.data;
  },

  /**
   * Update a meeting minute
   */
  async updateMinute(
    minuteId: number,
    data: MeetingMinuteUpdate,
  ): Promise<MeetingMinute> {
    const response = await apiClient.put<MeetingMinute>(
      `/meeting-minutes/${minuteId}`,
      data,
    );
    return response.data;
  },

  /**
   * Delete a meeting minute
   */
  async deleteMinute(minuteId: number): Promise<void> {
    await apiClient.delete(`/meeting-minutes/${minuteId}`);
  },

  /**
   * Upload an attachment to a meeting minute
   */
  async uploadAttachment(
    minuteId: number,
    file: File,
  ): Promise<MinuteAttachment> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await apiClient.post<MinuteAttachment>(
      `/meeting-minutes/${minuteId}/attachments`,
      formData,
      {
        headers: { "Content-Type": "multipart/form-data" },
      },
    );
    return response.data;
  },

  /**
   * Delete an attachment from a meeting minute
   */
  async deleteAttachment(
    minuteId: number,
    attachmentId: number,
  ): Promise<void> {
    await apiClient.delete(
      `/meeting-minutes/${minuteId}/attachments/${attachmentId}`,
    );
  },

  /**
   * Create an action item for a meeting minute
   */
  async createActionItem(
    minuteId: number,
    data: ActionItemCreate,
  ): Promise<ActionItem> {
    const response = await apiClient.post<ActionItem>(
      `/meeting-minutes/${minuteId}/action-items`,
      data,
    );
    return response.data;
  },

  /**
   * Update an action item
   */
  async updateActionItem(
    minuteId: number,
    actionItemId: number,
    data: ActionItemUpdate,
  ): Promise<ActionItem> {
    const response = await apiClient.put<ActionItem>(
      `/meeting-minutes/${minuteId}/action-items/${actionItemId}`,
      data,
    );
    return response.data;
  },

  /**
   * Delete an action item
   */
  async deleteActionItem(
    minuteId: number,
    actionItemId: number,
  ): Promise<void> {
    await apiClient.delete(
      `/meeting-minutes/${minuteId}/action-items/${actionItemId}`,
    );
  },
};
