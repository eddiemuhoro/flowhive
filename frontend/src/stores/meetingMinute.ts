// Meeting Minutes Store
import { defineStore } from "pinia";
import { ref } from "vue";
import { meetingMinuteService } from "@/services/meetingMinute.service";
import type {
  MeetingMinute,
  MeetingMinuteDetail,
  MeetingMinuteCreate,
  MeetingMinuteUpdate,
  MeetingMinuteFilters,
  ActionItemCreate,
  ActionItemUpdate,
} from "@/types/meetingMinute";

export const useMeetingMinuteStore = defineStore("meetingMinute", () => {
  const minutes = ref<MeetingMinute[]>([]);
  const currentMinute = ref<MeetingMinuteDetail | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  /**
   * Fetch all minutes for a workspace
   */
  async function fetchMinutes(
    workspaceId: number,
    filters?: MeetingMinuteFilters,
  ) {
    loading.value = true;
    error.value = null;

    try {
      minutes.value = await meetingMinuteService.getWorkspaceMinutes(
        workspaceId,
        filters,
      );
    } catch (err: any) {
      error.value =
        err.response?.data?.detail || "Failed to fetch meeting minutes";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Fetch a single minute with full details
   */
  async function fetchMinute(minuteId: number) {
    loading.value = true;
    error.value = null;

    try {
      currentMinute.value = await meetingMinuteService.getMinute(minuteId);
    } catch (err: any) {
      error.value =
        err.response?.data?.detail || "Failed to fetch meeting minute";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Create a new minute
   */
  async function createMinute(
    data: MeetingMinuteCreate,
  ): Promise<MeetingMinuteDetail> {
    loading.value = true;
    error.value = null;

    try {
      const newMinute = await meetingMinuteService.createMinute(data);
      minutes.value.unshift(newMinute);
      return newMinute;
    } catch (err: any) {
      error.value =
        err.response?.data?.detail || "Failed to create meeting minute";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Update a minute
   */
  async function updateMinute(
    minuteId: number,
    data: MeetingMinuteUpdate,
  ): Promise<MeetingMinute> {
    loading.value = true;
    error.value = null;

    try {
      const updatedMinute = await meetingMinuteService.updateMinute(
        minuteId,
        data,
      );

      // Update in list
      const index = minutes.value.findIndex((m) => m.id === minuteId);
      if (index !== -1) {
        minutes.value[index] = updatedMinute;
      }

      // Update current minute if it's loaded
      if (currentMinute.value && currentMinute.value.id === minuteId) {
        currentMinute.value = { ...currentMinute.value, ...updatedMinute };
      }

      return updatedMinute;
    } catch (err: any) {
      error.value =
        err.response?.data?.detail || "Failed to update meeting minute";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Delete a minute
   */
  async function deleteMinute(minuteId: number) {
    loading.value = true;
    error.value = null;

    try {
      await meetingMinuteService.deleteMinute(minuteId);

      // Remove from list
      minutes.value = minutes.value.filter((m) => m.id !== minuteId);

      // Clear current minute if it's the deleted one
      if (currentMinute.value && currentMinute.value.id === minuteId) {
        currentMinute.value = null;
      }
    } catch (err: any) {
      error.value =
        err.response?.data?.detail || "Failed to delete meeting minute";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Upload an attachment
   */
  async function uploadAttachment(minuteId: number, file: File) {
    loading.value = true;
    error.value = null;

    try {
      const attachment = await meetingMinuteService.uploadAttachment(
        minuteId,
        file,
      );

      // Update current minute if loaded
      if (currentMinute.value && currentMinute.value.id === minuteId) {
        currentMinute.value.attachments.push(attachment);
        currentMinute.value.attachment_count++;
      }

      return attachment;
    } catch (err: any) {
      error.value = err.response?.data?.detail || "Failed to upload attachment";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Delete an attachment
   */
  async function deleteAttachment(minuteId: number, attachmentId: number) {
    loading.value = true;
    error.value = null;

    try {
      await meetingMinuteService.deleteAttachment(minuteId, attachmentId);

      // Update current minute if loaded
      if (currentMinute.value && currentMinute.value.id === minuteId) {
        currentMinute.value.attachments =
          currentMinute.value.attachments.filter((a) => a.id !== attachmentId);
        currentMinute.value.attachment_count--;
      }
    } catch (err: any) {
      error.value = err.response?.data?.detail || "Failed to delete attachment";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Create an action item
   */
  async function createActionItem(minuteId: number, data: ActionItemCreate) {
    loading.value = true;
    error.value = null;

    try {
      const actionItem = await meetingMinuteService.createActionItem(
        minuteId,
        data,
      );

      // Update current minute if loaded
      if (currentMinute.value && currentMinute.value.id === minuteId) {
        currentMinute.value.action_items.push(actionItem);
        currentMinute.value.action_item_count++;
      }

      return actionItem;
    } catch (err: any) {
      error.value =
        err.response?.data?.detail || "Failed to create action item";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Update an action item
   */
  async function updateActionItem(
    minuteId: number,
    actionItemId: number,
    data: ActionItemUpdate,
  ) {
    loading.value = true;
    error.value = null;

    try {
      const updatedActionItem = await meetingMinuteService.updateActionItem(
        minuteId,
        actionItemId,
        data,
      );

      // Update current minute if loaded
      if (currentMinute.value && currentMinute.value.id === minuteId) {
        const index = currentMinute.value.action_items.findIndex(
          (a) => a.id === actionItemId,
        );
        if (index !== -1) {
          currentMinute.value.action_items[index] = updatedActionItem;
        }
      }

      return updatedActionItem;
    } catch (err: any) {
      error.value =
        err.response?.data?.detail || "Failed to update action item";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Delete an action item
   */
  async function deleteActionItem(minuteId: number, actionItemId: number) {
    loading.value = true;
    error.value = null;

    try {
      await meetingMinuteService.deleteActionItem(minuteId, actionItemId);

      // Update current minute if loaded
      if (currentMinute.value && currentMinute.value.id === minuteId) {
        currentMinute.value.action_items =
          currentMinute.value.action_items.filter((a) => a.id !== actionItemId);
        currentMinute.value.action_item_count--;
      }
    } catch (err: any) {
      error.value =
        err.response?.data?.detail || "Failed to delete action item";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  return {
    minutes,
    currentMinute,
    loading,
    error,
    fetchMinutes,
    fetchMinute,
    createMinute,
    updateMinute,
    deleteMinute,
    uploadAttachment,
    deleteAttachment,
    createActionItem,
    updateActionItem,
    deleteActionItem,
  };
});
