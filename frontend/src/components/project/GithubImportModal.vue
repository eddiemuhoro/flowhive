<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
    @click="$emit('close')"
  >
    <div
      class="relative top-10 mx-auto p-5 border w-full max-w-3xl shadow-lg rounded-md bg-white"
      @click.stop
    >
      <div class="mt-3">
        <h3 class="text-lg font-medium text-gray-900 mb-4">
          Import from GitHub
        </h3>

        <!-- Repository Selection -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Repository
          </label>
          <div class="space-y-2">
            <select
              v-model="selectedRepoOption"
              @change="handleRepoChange"
              :disabled="isLoadingRepos"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
            >
              <option value="custom">Custom Repository...</option>
              <option
                v-for="repo in repos"
                :key="repo.full_name"
                :value="repo.full_name"
              >
                {{ repo.full_name }}
                {{ repo.description ? ` - ${repo.description}` : "" }}
              </option>
            </select>

            <!-- Custom repo inputs -->
            <div
              v-if="selectedRepoOption === 'custom'"
              class="grid grid-cols-2 gap-2"
            >
              <input
                v-model="customRepoOwner"
                type="text"
                placeholder="Owner (e.g., username)"
                class="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              />
              <input
                v-model="customRepoName"
                type="text"
                placeholder="Repository name"
                class="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              />
            </div>
          </div>
          <p class="mt-1 text-xs text-gray-500">
            Select a repository or enter custom owner and name
          </p>
        </div>

        <!-- Date Filter -->
        <div class="mb-4">
          <label
            for="sinceDate"
            class="block text-sm font-medium text-gray-700 mb-2"
          >
            Show commits since
          </label>
          <div class="flex gap-3">
            <input
              id="sinceDate"
              v-model="sinceDate"
              type="date"
              class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
            />
            <button
              @click="loadCommits"
              :disabled="isLoadingCommits"
              class="px-4 py-2 bg-gray-600 text-white text-sm font-medium rounded-md hover:bg-gray-700 disabled:opacity-50"
            >
              {{ isLoadingCommits ? "Loading..." : "Load Commits" }}
            </button>
          </div>
          <p class="mt-1 text-xs text-gray-500">
            Select a date to see all your commits from that point forward
          </p>
        </div>

        <!-- Loading State -->
        <div
          v-if="isLoadingCommits"
          class="flex items-center justify-center py-12"
        >
          <div class="text-center">
            <div
              class="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-gray-600 border-r-transparent"
            ></div>
            <p class="mt-2 text-sm text-gray-600">Loading commits...</p>
          </div>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="rounded-lg bg-red-50 p-4 mb-4">
          <p class="text-sm text-red-700">{{ error }}</p>
        </div>

        <!-- Commits List -->
        <div v-else-if="commits.length > 0" class="space-y-4">
          <div class="flex items-center justify-between mb-2">
            <p class="text-sm text-gray-600">
              {{ commits.length }} commit(s) found. Select the ones to import:
            </p>
            <div class="flex gap-2">
              <button
                @click="selectAll"
                class="text-sm text-primary-600 hover:text-primary-700"
              >
                Select All
              </button>
              <span class="text-gray-300">|</span>
              <button
                @click="deselectAll"
                class="text-sm text-primary-600 hover:text-primary-700"
              >
                Deselect All
              </button>
            </div>
          </div>

          <div
            class="max-h-96 overflow-y-auto border border-gray-200 rounded-md divide-y divide-gray-200"
          >
            <label
              v-for="commit in commits"
              :key="commit.sha"
              class="flex items-start p-3 hover:bg-gray-50 cursor-pointer"
            >
              <input
                type="checkbox"
                :value="commit.sha"
                v-model="selectedCommits"
                class="mt-1 h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <div class="ml-3 flex-1">
                <div class="flex items-start justify-between">
                  <p class="text-sm font-medium text-gray-900">
                    {{ commit.message.split("\n")[0] }}
                  </p>
                  <span
                    class="ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800"
                  >
                    {{ commit.sha.substring(0, 7) }}
                  </span>
                </div>
                <p class="text-xs text-gray-500 mt-1">
                  {{ formatDate(commit.date) }} • {{ commit.author }}
                </p>
                <a
                  :href="commit.url"
                  target="_blank"
                  class="text-xs text-primary-600 hover:text-primary-700 mt-1 inline-block"
                  @click.stop
                >
                  View on GitHub →
                </a>
              </div>
            </label>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="!isLoadingCommits" class="text-center py-8">
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
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
          </svg>
          <p class="mt-2 text-sm text-gray-500">
            Select a repository and date, then click "Load Commits"
          </p>
        </div>

        <!-- Action Buttons -->
        <div class="flex justify-end space-x-3 mt-5">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 bg-white text-gray-700 text-sm font-medium rounded-md border border-gray-300 hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            @click="handleImport"
            :disabled="selectedCommits.length === 0 || isImporting"
            class="px-4 py-2 bg-gray-600 text-white text-sm font-medium rounded-md hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            <svg
              v-if="!isImporting"
              class="w-4 h-4"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"
              />
            </svg>
            <svg
              v-else
              class="w-4 h-4 animate-spin"
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
            {{
              isImporting
                ? "Importing..."
                : `Import ${selectedCommits.length} commit(s)`
            }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { useTaskStore } from "@/stores/task";

interface Commit {
  sha: string;
  message: string;
  url: string;
  date: string;
  author: string;
}

interface Repo {
  name: string;
  full_name: string;
  owner: string;
  description: string;
  private: boolean;
  url: string;
}

interface Props {
  show: boolean;
  projectId: number;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  (e: "close"): void;
  (e: "imported", count: number): void;
}>();

const taskStore = useTaskStore();

const sinceDate = ref<string>("");
const repos = ref<Repo[]>([]);
const selectedRepoOption = ref<string>("custom");
const customRepoOwner = ref<string>("eddiemuhoro");
const customRepoName = ref<string>("flowhive");
const commits = ref<Commit[]>([]);
const selectedCommits = ref<string[]>([]);
const isLoadingRepos = ref(false);
const isLoadingCommits = ref(false);
const isImporting = ref(false);
const error = ref<string | null>(null);

// Set default date to today when modal opens
watch(
  () => props.show,
  (newValue) => {
    if (newValue) {
      const today = new Date();
      sinceDate.value = today.toISOString().split("T")[0];
      // Load repos when modal opens
      loadRepos();
    } else {
      // Reset state when modal closes
      commits.value = [];
      selectedCommits.value = [];
      selectedRepoOption.value = "custom";
      customRepoOwner.value = "eddiemuhoro";
      customRepoName.value = "flowhive";
      error.value = null;
    }
  },
);

const loadRepos = async () => {
  isLoadingRepos.value = true;
  error.value = null;

  try {
    repos.value = await taskStore.fetchGithubRepos();
    // Auto-select first repo if available
    if (repos.value.length > 0) {
      selectedRepoOption.value = repos.value[0].full_name;
    }
  } catch (err: any) {
    console.error("Error loading repos:", err);
    // Don't show error, just let user enter custom repo
    selectedRepoOption.value = "custom";
  } finally {
    isLoadingRepos.value = false;
  }
};

const handleRepoChange = () => {
  // Clear commits when repo changes
  commits.value = [];
  selectedCommits.value = [];
  error.value = null;
};

const getRepoInfo = (): { owner: string; name: string } | null => {
  if (selectedRepoOption.value === "custom") {
    if (!customRepoOwner.value || !customRepoName.value) {
      return null;
    }
    return {
      owner: customRepoOwner.value,
      name: customRepoName.value,
    };
  } else {
    const [owner, name] = selectedRepoOption.value.split("/");
    return { owner, name };
  }
};

const loadCommits = async () => {
  const repoInfo = getRepoInfo();
  if (!repoInfo) {
    error.value = "Please select a repository or enter owner and name";
    return;
  }

  if (!sinceDate.value) {
    error.value = "Please select a date";
    return;
  }

  isLoadingCommits.value = true;
  error.value = null;

  try {
    const sinceISO = `${sinceDate.value}T00:00:00Z`;
    commits.value = await taskStore.fetchGithubCommits(
      repoInfo.owner,
      repoInfo.name,
      sinceISO,
    );
    selectedCommits.value = []; // Reset selection when loading new commits
  } catch (err: any) {
    error.value =
      err.response?.data?.detail ||
      err.message ||
      "Failed to load commits from GitHub";
    console.error("Error loading commits:", err);
  } finally {
    isLoadingCommits.value = false;
  }
};

const selectAll = () => {
  selectedCommits.value = commits.value.map((c) => c.sha);
};

const deselectAll = () => {
  selectedCommits.value = [];
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

const handleImport = async () => {
  if (selectedCommits.value.length === 0) return;

  const repoInfo = getRepoInfo();
  if (!repoInfo) {
    error.value = "Please select a repository or enter owner and name";
    return;
  }

  isImporting.value = true;
  error.value = null;

  try {
    const createdTasks = await taskStore.createTasksFromGithub(
      props.projectId,
      repoInfo.owner,
      repoInfo.name,
      selectedCommits.value,
    );

    emit("imported", createdTasks.length);
    emit("close");
  } catch (err: any) {
    error.value =
      err.response?.data?.detail ||
      err.message ||
      "Failed to import tasks from GitHub";
    console.error("Error importing commits:", err);
  } finally {
    isImporting.value = false;
  }
};
</script>
