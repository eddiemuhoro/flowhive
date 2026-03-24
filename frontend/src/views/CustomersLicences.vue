<template>
  <div class="space-y-6 p-2 md:p-6">
    <div class="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Licence Health Dashboard</h1>
        <p class="mt-1 text-sm text-gray-600">
          Monitor licence expiry risk using Sajsoft customer records.
        </p>
      </div>

      <div class="grid w-full gap-3 md:w-auto md:grid-cols-2">
        <div>
          <label for="licence-search" class="mb-1 block text-sm font-medium text-gray-700">Search</label>
          <input
            id="licence-search"
            v-model="searchQuery"
            type="text"
            placeholder="Customer, client id, rep, category"
            class="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        <div>
          <label for="status-filter" class="mb-1 block text-sm font-medium text-gray-700">Status Filter</label>
          <select
            id="status-filter"
            v-model="statusFilter"
            class="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="risk">Risk Only</option>
            <option value="all">All</option>
            <option value="expired">Expired</option>
            <option value="expired30">Expired 0-30 Days</option>
            <option value="expired90">Expired 31-90 Days</option>
            <option value="expired365">Expired 91-365 Days</option>
            <option value="expiredLegacy">Expired 365+ Days</option>
            <option value="due30">Due in 30 Days</option>
            <option value="due60">Due in 31-60 Days</option>
            <option value="dataIssues">Data Quality Issues</option>
            <option value="missing">Missing Date</option>
            <option value="invalid">Invalid Date</option>
            <option value="active">Active</option>
          </select>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
      <button
        type="button"
        class="rounded-lg border p-4 text-left shadow-sm transition focus:outline-none focus:ring-2 focus:ring-offset-1"
        :class="getCardClass('all', 'border-gray-200 bg-white focus:ring-gray-400')"
        @click="setStatusFilter('all')"
      >
        <p class="text-xs font-semibold uppercase tracking-wide text-gray-500">Total Records</p>
        <p class="mt-1 text-xs text-gray-500">All customers.</p>
        <p class="mt-2 text-2xl font-bold text-gray-900">{{ totalRecords }}</p>
      </button>

      <button
        type="button"
        class="rounded-lg border p-4 text-left shadow-sm transition focus:outline-none focus:ring-2 focus:ring-offset-1"
        :class="getCardClass('expired', 'border-red-200 bg-red-50 focus:ring-red-400')"
        @click="setStatusFilter('expired')"
      >
        <p class="text-xs font-semibold uppercase tracking-wide text-red-700">Expired</p>
        <p class="mt-1 text-xs text-red-700">Licence end date has already passed.</p>
        <p class="mt-2 text-2xl font-bold text-red-900">{{ expiredCount }}</p>
      </button>

      <button
        type="button"
        class="rounded-lg border p-4 text-left shadow-sm transition focus:outline-none focus:ring-2 focus:ring-offset-1"
        :class="getCardClass('due30', 'border-amber-200 bg-amber-50 focus:ring-amber-400')"
        @click="setStatusFilter('due30')"
      >
        <p class="text-xs font-semibold uppercase tracking-wide text-amber-700">Due in 30 Days</p>
        <p class="mt-1 text-xs text-amber-700">Needs urgent renewal follow-up.</p>
        <p class="mt-2 text-2xl font-bold text-amber-900">{{ dueIn30Count }}</p>
      </button>

      <button
        type="button"
        class="rounded-lg border p-4 text-left shadow-sm transition focus:outline-none focus:ring-2 focus:ring-offset-1"
        :class="getCardClass('due60', 'border-orange-200 bg-orange-50 focus:ring-orange-400')"
        @click="setStatusFilter('due60')"
      >
        <p class="text-xs font-semibold uppercase tracking-wide text-orange-700">Due in 31-60 Days</p>
        <p class="mt-1 text-xs text-orange-700">Upcoming renewals to schedule now.</p>
        <p class="mt-2 text-2xl font-bold text-orange-900">{{ dueIn60Count }}</p>
      </button>

      <button
        type="button"
        class="rounded-lg border p-4 text-left shadow-sm transition focus:outline-none focus:ring-2 focus:ring-offset-1"
        :class="getCardClass('active', 'border-green-200 bg-green-50 focus:ring-green-400')"
        @click="setStatusFilter('active')"
      >
        <p class="text-xs font-semibold uppercase tracking-wide text-green-700">Active</p>
        <p class="mt-1 text-xs text-green-700">Valid licence beyond 60 days.</p>
        <p class="mt-2 text-2xl font-bold text-green-900">{{ activeCount }}</p>
      </button>

      <button
        type="button"
        class="rounded-lg border p-4 text-left shadow-sm transition focus:outline-none focus:ring-2 focus:ring-offset-1"
        :class="getCardClass('dataIssues', 'border-slate-200 bg-slate-50 focus:ring-slate-400')"
        @click="setStatusFilter('dataIssues')"
      >
        <p class="text-xs font-semibold uppercase tracking-wide text-slate-700">Data Quality Issues</p>
        <p class="mt-1 text-xs text-slate-700">Missing or invalid issued/expiry dates.</p>
        <p class="mt-2 text-2xl font-bold text-slate-900">{{ dataIssueCount }}</p>
      </button>
    </div>

    <div class="rounded-lg border border-gray-200 bg-white shadow-sm">
      <button
        type="button"
        class="flex w-full items-center justify-between px-4 py-3 text-left"
        @click="showExpiredBreakdown = !showExpiredBreakdown"
      >
        <div>
          <p class="text-sm font-semibold text-gray-900">Expired Breakdown</p>
          <p class="text-xs text-gray-500">Segment older expiries for investigation and churn tracking.</p>
        </div>
        <span class="text-xs font-medium text-gray-600">{{ showExpiredBreakdown ? 'Hide' : 'Show' }}</span>
      </button>

      <div v-if="showExpiredBreakdown" class="grid grid-cols-1 gap-3 border-t border-gray-100 p-3 sm:grid-cols-2 xl:grid-cols-4">
        <button
          type="button"
          class="rounded-lg border p-3 text-left shadow-sm transition focus:outline-none focus:ring-2 focus:ring-offset-1"
          :class="getCardClass('expired30', 'border-red-200 bg-red-50 focus:ring-red-400')"
          @click="setStatusFilter('expired30')"
        >
          <p class="text-xs font-semibold uppercase tracking-wide text-red-700">Expired 0-30 Days</p>
          <p class="mt-1 text-xs text-red-700">Recent expiries with high recovery chance.</p>
          <p class="mt-1 text-xl font-bold text-red-900">{{ expired0To30Count }}</p>
        </button>

        <button
          type="button"
          class="rounded-lg border p-3 text-left shadow-sm transition focus:outline-none focus:ring-2 focus:ring-offset-1"
          :class="getCardClass('expired90', 'border-orange-200 bg-orange-50 focus:ring-orange-400')"
          @click="setStatusFilter('expired90')"
        >
          <p class="text-xs font-semibold uppercase tracking-wide text-orange-700">Expired 31-90 Days</p>
          <p class="mt-1 text-xs text-orange-700">Medium-term expiries, at-risk churn group.</p>
          <p class="mt-1 text-xl font-bold text-orange-900">{{ expired31To90Count }}</p>
        </button>

        <button
          type="button"
          class="rounded-lg border p-3 text-left shadow-sm transition focus:outline-none focus:ring-2 focus:ring-offset-1"
          :class="getCardClass('expired365', 'border-amber-200 bg-amber-50 focus:ring-amber-400')"
          @click="setStatusFilter('expired365')"
        >
          <p class="text-xs font-semibold uppercase tracking-wide text-amber-700">Expired 91-365 Days</p>
          <p class="mt-1 text-xs text-amber-700">Long-expired accounts needing investigation.</p>
          <p class="mt-1 text-xl font-bold text-amber-900">{{ expired91To365Count }}</p>
        </button>

        <button
          type="button"
          class="rounded-lg border p-3 text-left shadow-sm transition focus:outline-none focus:ring-2 focus:ring-offset-1"
          :class="getCardClass('expiredLegacy', 'border-slate-200 bg-slate-50 focus:ring-slate-400')"
          @click="setStatusFilter('expiredLegacy')"
        >
          <p class="text-xs font-semibold uppercase tracking-wide text-slate-700">Expired 365+ Days</p>
          <p class="mt-1 text-xs text-slate-700">Legacy backlog for cleanup or reactivation.</p>
          <p class="mt-1 text-xl font-bold text-slate-900">{{ expiredOver365Count }}</p>
        </button>
      </div>
    </div>

    <div class="rounded-lg border border-gray-200 bg-white shadow-sm">
      <div class="border-b border-gray-200 px-4 py-3">
        <div class="flex items-center justify-between gap-3">
          <h2 class="text-sm font-semibold text-gray-900">Priority Licence List</h2>
          <button
            @click="refetch()"
            class="rounded-md border border-gray-300 px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-50"
          >
            Refresh
          </button>
        </div>
      </div>

      <div v-if="isLoading" class="px-4 py-10 text-center text-sm text-gray-500">
        Loading customer records...
      </div>

      <div v-else-if="isError" class="px-4 py-10 text-center">
        <p class="text-sm font-medium text-red-700">Failed to load customer records.</p>
        <p class="mt-1 text-xs text-red-600">{{ errorMessage }}</p>
      </div>

      <div v-else-if="filteredRows.length === 0" class="px-4 py-10 text-center text-sm text-gray-500">
        No customer records match the selected filter.
      </div>

      <div v-else>
        <div class="hidden overflow-x-auto md:block">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-600">Customer</th>
                <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-600">Client ID</th>
                <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-600">Licence Key</th>
                <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-600">Issued</th>
                <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-600">Expiry</th>
                <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-600">Days Left</th>
                <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-600">Status</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 bg-white">
              <tr v-for="row in filteredRows" :key="row.idKey" class="hover:bg-gray-50">
                <td class="px-4 py-3 text-sm">
                  <p class="font-medium text-gray-900">{{ row.name }}</p>
                  <p class="text-xs text-gray-500">{{ row.category || 'Uncategorised' }}</p>
                </td>
                <td class="px-4 py-3 text-sm text-gray-700">{{ row.clientId }}</td>
                <td class="px-4 py-3 text-sm text-gray-700">
                  <span
                    class="inline-block max-w-[220px] truncate align-bottom"
                    :title="row.licenceKey || 'N/A'"
                  >
                    {{ row.licenceKey || 'N/A' }}
                  </span>
                </td>
                <td class="px-4 py-3 text-sm text-gray-700">{{ formatDate(row.issuedOn) }}</td>
                <td class="px-4 py-3 text-sm text-gray-700">{{ formatDate(row.expiresOn) }}</td>
                <td class="px-4 py-3 text-sm text-gray-700">{{ formatDays(row.daysToExpiry) }}</td>
                <td class="px-4 py-3 text-sm">
                  <span
                    class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium"
                    :class="getStatusClass(row.status)"
                  >
                    {{ row.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="space-y-3 p-3 md:hidden">
          <article
            v-for="row in filteredRows"
            :key="row.idKey"
            class="rounded-md border border-gray-200 bg-white p-3"
          >
            <div class="flex items-start justify-between gap-3">
              <div>
                <h3 class="text-sm font-semibold text-gray-900">{{ row.name }}</h3>
                <p class="text-xs text-gray-500">{{ row.clientId }} • {{ row.category || 'Uncategorised' }}</p>
              </div>
              <span
                class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium"
                :class="getStatusClass(row.status)"
              >
                {{ row.status }}
              </span>
            </div>

            <div class="mt-3 grid grid-cols-2 gap-2 text-xs text-gray-600">
              <div>
                <p class="font-medium text-gray-500">Issued</p>
                <p>{{ formatDate(row.issuedOn) }}</p>
              </div>
              <div>
                <p class="font-medium text-gray-500">Expiry</p>
                <p>{{ formatDate(row.expiresOn) }}</p>
              </div>
              <div>
                <p class="font-medium text-gray-500">Days Left</p>
                <p>{{ formatDays(row.daysToExpiry) }}</p>
              </div>
              <div>
                <p class="font-medium text-gray-500">Rep</p>
                <p>{{ row.rep || 'N/A' }}</p>
              </div>
            </div>
          </article>
        </div>
      </div>

      <div v-if="isFetching && !isLoading" class="border-t border-gray-100 px-4 py-2 text-right text-xs text-gray-500">
        Updating data...
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useAllCompanies } from '@/composables/useCustomers'
import type { CompanyAnalyticsCustomer } from '@/types/field'

type LicenceHealthStatus =
  | 'Expired'
  | 'Due in 30 Days'
  | 'Due in 31-60 Days'
  | 'Active'
  | 'Missing Date'
  | 'Invalid Date'

type StatusFilter =
  | 'risk'
  | 'all'
  | 'expired'
  | 'expired30'
  | 'expired90'
  | 'expired365'
  | 'expiredLegacy'
  | 'due30'
  | 'due60'
  | 'dataIssues'
  | 'missing'
  | 'invalid'
  | 'active'

interface CompanyAnalyticsRow {
  idKey: string
  recordId: number | null
  name: string
  clientId: string
  licenceKey: string | null
  category: string | null
  rep: string | null
  issuedOn: string | null
  expiresOn: string | null
  daysToExpiry: number | null
  status: LicenceHealthStatus
}

const searchQuery = ref('')
const statusFilter = ref<StatusFilter>('due30')
const showExpiredBreakdown = ref(false)

const {
  data: companies,
  isLoading,
  isError,
  isFetching,
  error,
  refetch,
} = useAllCompanies()

const safeCompanies = computed(() => companies.value ?? [])

const rows = computed<CompanyAnalyticsRow[]>(() => {
  return safeCompanies.value.map((company: CompanyAnalyticsCustomer, index: number) => {
    const issuedOn = normaliseDateValue(company.systemdate)
    const expiresOn = normaliseDateValue(company.expiry)

    const issuedDate = parseDbDate(issuedOn)
    const expiryDate = parseDbDate(expiresOn)

    const hasMissingDate = !issuedOn || !expiresOn
    const hasInvalidDate = (issuedOn && !issuedDate) || (expiresOn && !expiryDate)
    const daysToExpiry = getDaysFromToday(expiryDate)

    let status: LicenceHealthStatus = 'Active'

    if (hasMissingDate) {
      status = 'Missing Date'
    } else if (hasInvalidDate) {
      status = 'Invalid Date'
    } else if (typeof daysToExpiry === 'number' && daysToExpiry < 0) {
      status = 'Expired'
    } else if (typeof daysToExpiry === 'number' && daysToExpiry <= 30) {
      status = 'Due in 30 Days'
    } else if (typeof daysToExpiry === 'number' && daysToExpiry <= 60) {
      status = 'Due in 31-60 Days'
    }

    const recordId = parseNumericId(company.id)

    return {
      idKey: `${String(company.id)}-${index}`,
      recordId,
      name: normaliseText(company.name) || 'Unknown Customer',
      clientId: normaliseText(company.clientid) || 'N/A',
      licenceKey: normaliseText(company.licensekey),
      category: normaliseText(company.category),
      rep: normaliseText(company.rep),
      issuedOn,
      expiresOn,
      daysToExpiry,
      status,
    }
  })
})

const sortedRows = computed(() => {
  return [...rows.value].sort((a, b) => {
    if (a.recordId !== null && b.recordId !== null) {
      return b.recordId - a.recordId
    }

    if (a.recordId === null && b.recordId !== null) {
      return 1
    }

    if (a.recordId !== null && b.recordId === null) {
      return -1
    }

    return b.idKey.localeCompare(a.idKey)
  })
})

const filteredRows = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()

  return sortedRows.value.filter((row) => {
    const statusMatch = doesRowMatchFilter(row, statusFilter.value)

    if (!statusMatch) {
      return false
    }

    if (!query) {
      return true
    }

    return [row.name, row.clientId, row.category, row.rep]
      .filter(Boolean)
      .some((value) => String(value).toLowerCase().includes(query))
  })
})

const totalRecords = computed(() => rows.value.length)
const expiredCount = computed(() => countByStatus('Expired'))
const dueIn30Count = computed(() => countByStatus('Due in 30 Days'))
const dueIn60Count = computed(() => countByStatus('Due in 31-60 Days'))
const activeCount = computed(() => countByStatus('Active'))
const dataIssueCount = computed(() => countByStatus('Missing Date') + countByStatus('Invalid Date'))
const expired0To30Count = computed(() => countExpiredByAge(0, 30))
const expired31To90Count = computed(() => countExpiredByAge(31, 90))
const expired91To365Count = computed(() => countExpiredByAge(91, 365))
const expiredOver365Count = computed(() => countExpiredByAge(366, Number.POSITIVE_INFINITY))

const errorMessage = computed(() => {
  if (!error.value) {
    return 'An unknown error occurred.'
  }

  return error.value instanceof Error ? error.value.message : 'Could not fetch customer records.'
})

function countByStatus(status: LicenceHealthStatus) {
  return rows.value.filter((row) => row.status === status).length
}

function countExpiredByAge(minDays: number, maxDays: number) {
  return rows.value.filter((row) => isExpiredInRange(row, minDays, maxDays)).length
}

function doesRowMatchFilter(row: CompanyAnalyticsRow, filter: StatusFilter) {
  const { status } = row

  if (filter === 'all') {
    return true
  }

  if (filter === 'risk') {
    return status !== 'Active'
  }

  if (filter === 'expired') {
    return status === 'Expired'
  }

  if (filter === 'expired30') {
    return isExpiredInRange(row, 0, 30)
  }

  if (filter === 'expired90') {
    return isExpiredInRange(row, 31, 90)
  }

  if (filter === 'expired365') {
    return isExpiredInRange(row, 91, 365)
  }

  if (filter === 'expiredLegacy') {
    return isExpiredInRange(row, 366, Number.POSITIVE_INFINITY)
  }

  if (filter === 'due30') {
    return status === 'Due in 30 Days'
  }

  if (filter === 'due60') {
    return status === 'Due in 31-60 Days'
  }

  if (filter === 'dataIssues') {
    return status === 'Missing Date' || status === 'Invalid Date'
  }

  if (filter === 'missing') {
    return status === 'Missing Date'
  }

  if (filter === 'invalid') {
    return status === 'Invalid Date'
  }

  return status === 'Active'
}

function isExpiredInRange(row: CompanyAnalyticsRow, minDays: number, maxDays: number) {
  if (row.status !== 'Expired' || row.daysToExpiry === null) {
    return false
  }

  const daysSinceExpiry = Math.abs(row.daysToExpiry)
  return daysSinceExpiry >= minDays && daysSinceExpiry <= maxDays
}

function setStatusFilter(filter: StatusFilter) {
  statusFilter.value = filter
}

function getCardClass(filter: StatusFilter, baseClass: string) {
  if (statusFilter.value === filter) {
    return `${baseClass} ring-2 ring-primary-500 scale-[1.01]`
  }

  return `${baseClass} hover:brightness-95`
}

function normaliseText(value: unknown) {
  if (value === null || value === undefined) {
    return null
  }

  const text = String(value).trim()
  return text ? text : null
}

function normaliseDateValue(value: unknown) {
  const raw = normaliseText(value)
  return raw || null
}

function parseNumericId(value: unknown) {
  if (value === null || value === undefined) {
    return null
  }

  const parsed = Number(String(value).trim())
  return Number.isFinite(parsed) ? parsed : null
}

function parseDbDate(value: string | null) {
  if (!value || !/^\d{4}-\d{2}-\d{2}$/.test(value)) {
    return null
  }

  const [year, month, day] = value.split('-').map(Number)
  const parsed = new Date(year, month - 1, day)

  if (Number.isNaN(parsed.getTime())) {
    return null
  }

  if (
    parsed.getFullYear() !== year ||
    parsed.getMonth() !== month - 1 ||
    parsed.getDate() !== day
  ) {
    return null
  }

  return parsed
}

function getDaysFromToday(date: Date | null) {
  if (!date) {
    return null
  }

  const today = new Date()
  const todayStart = new Date(today.getFullYear(), today.getMonth(), today.getDate())
  const targetStart = new Date(date.getFullYear(), date.getMonth(), date.getDate())
  const diffMs = targetStart.getTime() - todayStart.getTime()
  return Math.floor(diffMs / 86400000)
}

function formatDate(value: string | null) {
  const parsedDate = parseDbDate(value)
  if (!parsedDate) {
    return value ? 'Invalid date' : 'N/A'
  }

  return parsedDate.toLocaleDateString('en-GB', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

function formatDays(days: number | null) {
  if (days === null) {
    return 'N/A'
  }

  if (days === 0) {
    return 'Today'
  }

  if (days < 0) {
    return `${Math.abs(days)} days ago`
  }

  return `${days} days`
}

function getStatusClass(status: LicenceHealthStatus) {
  if (status === 'Expired') {
    return 'bg-red-100 text-red-800'
  }

  if (status === 'Due in 30 Days') {
    return 'bg-amber-100 text-amber-800'
  }

  if (status === 'Due in 31-60 Days') {
    return 'bg-orange-100 text-orange-800'
  }

  if (status === 'Missing Date') {
    return 'bg-slate-200 text-slate-800'
  }

  if (status === 'Invalid Date') {
    return 'bg-rose-100 text-rose-800'
  }

  return 'bg-green-100 text-green-800'
}
</script>
