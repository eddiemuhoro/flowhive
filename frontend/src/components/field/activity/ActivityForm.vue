<!-- Activity Form Component -->
<!-- Form for creating and editing field activities -->

<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <!-- Title -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">
        Title <span class="text-red-500">*</span>
      </label>
      <input
        v-model="formData.title"
        type="text"
        required
        placeholder="Brief summary of activity"
        class="w-full rounded-lg border px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        :class="{ 'border-red-300': errors.title }"
      />
      <p v-if="errors.title" class="mt-1 text-sm text-red-600">
        {{ errors.title }}
      </p>
    </div>

    <!-- Task Category -->
    <CategorySelector
      v-model="formData.task_category_id"
      :workspace-id="workspaceId"
      label="Task Category"
      placeholder="Select task category"
      :allow-null="true"
      :error="errors.task_category_id"
    />

    <!-- Date -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">
        Date <span class="text-red-500">*</span>
      </label>
      <input
        v-model="formData.activity_date"
        type="date"
        required
        :max="today"
        class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        :class="{ 'border-red-300': errors.activity_date }"
      />
      <p v-if="errors.activity_date" class="mt-1 text-sm text-red-600">
        {{ errors.activity_date }}
      </p>
    </div>

    <!-- Time Range -->
    <div class="grid grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Start Time <span class="text-red-500">*</span>
        </label>
        <input
          v-model="formData.start_time"
          type="time"
          required
          class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          :class="{ 'border-red-300': errors.start_time }"
        />
        <p v-if="errors.start_time" class="mt-1 text-sm text-red-600">
          {{ errors.start_time }}
        </p>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          End Time <span class="text-red-500">*</span>
        </label>
        <input
          v-model="formData.end_time"
          type="time"
          required
          class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          :class="{ 'border-red-300': errors.end_time }"
        />
        <p v-if="errors.end_time" class="mt-1 text-sm text-red-600">
          {{ errors.end_time }}
        </p>
      </div>
    </div>

    <!-- Support Staff (if manager/executive creating for someone else) -->
    <div v-if="canSelectStaff">
      <label class="block text-sm font-medium text-gray-700 mb-1">
        Support Staff <span class="text-red-500">*</span>
      </label>
      <select
        v-model="formData.support_staff_id"
        required
        class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
      >
        <option :value="null">Select staff member</option>
        <option
          v-for="member in workspaceMembers"
          :key="member.user_id"
          :value="member.user_id"
        >
          {{ member.full_name || member.username }}
        </option>
      </select>
    </div>

    <!-- Customer Name -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">
        Customer Name <span class="text-red-500">*</span>
      </label>
      <div class="relative">
        <input
          v-model="customerSearch"
          @focus="showCustomerDropdown = true"
          @input="handleCustomerSearch"
          type="text"
          required
          placeholder="Search for customer..."
          class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          :class="{ 'border-red-300': errors.customer_name }"
        />
        <!-- Dropdown List -->
        <div
          v-if="showCustomerDropdown && filteredCustomers.length > 0"
          class="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto"
        >
          <button
            v-for="customer in filteredCustomers"
            :key="customer.id"
            type="button"
            @click="selectCustomer(customer)"
            class="w-full text-left px-3 py-2 hover:bg-blue-50 focus:bg-blue-50 focus:outline-none border-b border-gray-100 last:border-b-0"
          >
            <div class="font-medium text-gray-900">{{ customer.name }}</div>
            <div class="text-xs text-gray-500 truncate">
              {{ customer.address }}
            </div>
          </button>
        </div>
        <!-- Loading State -->
        <div
          v-if="loadingCustomers"
          class="absolute right-3 top-2.5 text-gray-400"
        >
          <svg
            class="animate-spin h-5 w-5"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            ></circle>
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
        </div>
      </div>
      <p v-if="errors.customer_name" class="mt-1 text-sm text-red-600">
        {{ errors.customer_name }}
      </p>
      <p v-if="formData.customer_id" class="mt-1 text-xs text-gray-500">
        Customer ID: {{ formData.customer_id }}
      </p>
    </div>

    <!-- Location -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">
        Location <span class="text-red-500">*</span>
      </label>
      <input
        v-model="formData.location"
        type="text"
        required
        placeholder="Site location or address"
        class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        :class="{ 'border-red-300': errors.location }"
      />
      <p v-if="errors.location" class="mt-1 text-sm text-red-600">
        {{ errors.location }}
      </p>
    </div>

    <!-- Task Description -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">
        Task Description <span class="text-red-500">*</span>
      </label>
      <RichTextEditor
        v-model="formData.task_description"
        placeholder="Detailed description of work performed (you can format text, add lists, headings, etc.)"
        :error="errors.task_description"
        min-height="200px"
      />
    </div>

    <!-- Remarks -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">
        Remarks (Optional)
      </label>
      <RichTextEditor
        v-model="formData.remarks"
        placeholder="Additional notes or observations"
        min-height="60px"
      />
    </div>

    <!-- Customer Rep -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">
        Customer Representative <span class="text-red-500">*</span>
      </label>
      <input
        v-model="formData.customer_rep"
        type="text"
        required
        placeholder="Contact person at customer site"
        class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        :class="{ 'border-red-300': errors.customer_rep }"
      />
      <p v-if="errors.customer_rep" class="mt-1 text-sm text-red-600">
        {{ errors.customer_rep }}
      </p>
    </div>

    <!-- Actions -->
    <div class="flex items-center justify-end space-x-3 border-t pt-4">
      <button
        type="button"
        @click="$emit('cancel')"
        :disabled="loading"
        class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
      >
        Cancel
      </button>
      <button
        type="submit"
        :disabled="loading"
        class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
      >
        {{
          loading ? "Saving..." : isEdit ? "Update Activity" : "Create Activity"
        }}
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onBeforeUnmount } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useWorkspaceStore } from "@/stores/workspace";
import { customerService } from "@/services/customer.service";
import CategorySelector from "@/components/field/category/CategorySelector.vue";
import RichTextEditor from "@/components/ui/RichTextEditor.vue";
import type {
  FieldActivityCreate,
  FieldActivityUpdate,
  FieldActivity,
  Customer,
} from "@/types/field";

interface Props {
  workspaceId: number;
  activity?: FieldActivity;
  loading?: boolean;
}

interface Emits {
  (e: "submit", data: FieldActivityCreate | FieldActivityUpdate): void;
  (e: "cancel"): void;
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
});

const emit = defineEmits<Emits>();

const authStore = useAuthStore();
const workspaceStore = useWorkspaceStore();

const currentUser = computed(() => authStore.user);
const workspaceMembers = computed(
  () => workspaceStore.currentWorkspace?.members || [],
);

const canSelectStaff = computed(() => {
  const role = currentUser.value?.role?.toUpperCase();
  return role === "MANAGER" || role === "EXECUTIVE";
});

const isEdit = computed(() => !!props.activity);

const today = computed(() => {
  return new Date().toISOString().split("T")[0];
});

const formData = ref<FieldActivityCreate>({
  workspace_id: props.workspaceId,
  support_staff_id: currentUser.value?.id || 0,
  title: "",
  activity_date: today.value,
  start_time: "09:00",
  end_time: "17:00",
  customer_id: null,
  customer_name: "",
  location: "",
  task_description: "",
  task_category_id: null,
  remarks: "",
  customer_rep: "",
});

const errors = ref<Record<string, string>>({});

// Customer search and selection
const customers = ref<Customer[]>([]);
const loadingCustomers = ref(false);
const customerSearch = ref("");
const showCustomerDropdown = ref(false);

const filteredCustomers = computed(() => {
  if (!customerSearch.value.trim()) {
    return customers.value.slice(0, 50); // Show first 50 by default
  }
  const search = customerSearch.value.toLowerCase();
  return customers.value
    .filter(
      (customer) =>
        customer.name.toLowerCase().includes(search) ||
        customer.address.toLowerCase().includes(search) ||
        customer.clientid.includes(search),
    )
    .slice(0, 50); // Limit to 50 results
});

const selectCustomer = (customer: Customer) => {
  formData.value.customer_id = customer.id;
  formData.value.customer_name = customer.name;
  customerSearch.value = customer.name;
  showCustomerDropdown.value = false;
};

const handleCustomerSearch = () => {
  showCustomerDropdown.value = true;
  // Clear customer_id if user is typing (manual entry)
  if (customerSearch.value !== formData.value.customer_name) {
    formData.value.customer_id = null;
    formData.value.customer_name = customerSearch.value;
  }
};

const loadCustomers = async () => {
  try {
    loadingCustomers.value = true;
    customers.value = await customerService.getCompanies();
  } catch (error) {
    console.error("Failed to load customers:", error);
  } finally {
    loadingCustomers.value = false;
  }
};

// Close dropdown when clicking outside
const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement;
  if (!target.closest(".relative")) {
    showCustomerDropdown.value = false;
  }
};

// Load existing activity data if editing
watch(
  () => props.activity,
  (activity) => {
    if (activity) {
      formData.value = {
        workspace_id: props.workspaceId,
        support_staff_id: activity.support_staff_id,
        title: activity.title,
        activity_date: activity.activity_date,
        start_time: activity.start_time,
        end_time: activity.end_time,
        customer_id: activity.customer_id,
        customer_name: activity.customer_name,
        location: activity.location,
        task_description: activity.task_description,
        task_category_id: activity.task_category_id,
        remarks: activity.remarks,
        customer_rep: activity.customer_rep,
      };
      customerSearch.value = activity.customer_name;
    }
  },
  { immediate: true },
);

const validateForm = (): boolean => {
  errors.value = {};
  let isValid = true;

  if (!formData.value.title?.trim()) {
    errors.value.title = "Title is required";
    isValid = false;
  }

  if (!formData.value.activity_date) {
    errors.value.activity_date = "Date is required";
    isValid = false;
  }

  if (!formData.value.start_time) {
    errors.value.start_time = "Start time is required";
    isValid = false;
  }

  if (!formData.value.end_time) {
    errors.value.end_time = "End time is required";
    isValid = false;
  }

  if (!formData.value.customer_name?.trim()) {
    errors.value.customer_name = "Customer name is required";
    isValid = false;
  }

  if (!formData.value.location?.trim()) {
    errors.value.location = "Location is required";
    isValid = false;
  }

  // Check if task_description has content (accounting for HTML tags)
  const tempDiv = document.createElement("div");
  tempDiv.innerHTML = formData.value.task_description || "";
  const textContent = tempDiv.textContent || tempDiv.innerText || "";

  if (!textContent.trim()) {
    errors.value.task_description = "Task description is required";
    isValid = false;
  }

  if (!formData.value.customer_rep?.trim()) {
    errors.value.customer_rep = "Customer representative is required";
    isValid = false;
  }

  return isValid;
};

const handleSubmit = () => {
  if (!validateForm()) {
    return;
  }

  if (isEdit.value) {
    const { workspace_id, support_staff_id, ...updateData } = formData.value;
    emit("submit", updateData as FieldActivityUpdate);
  } else {
    emit("submit", formData.value);
  }
};

onMounted(async () => {
  // Load workspace members if needed
  if (canSelectStaff.value && workspaceMembers.value.length === 0) {
    await workspaceStore.fetchWorkspace(props.workspaceId);
  }

  // Load customers
  await loadCustomers();

  // Add click outside listener
  document.addEventListener("click", handleClickOutside);
});

onBeforeUnmount(() => {
  // Remove click outside listener
  document.removeEventListener("click", handleClickOutside);
});
</script>
