<template>
    <div class="space-y-6 p-2 md:p-6">
        <div class="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
                <h1 class="text-3xl font-bold text-gray-900">Customer Licences</h1>
                <p class="mt-1 text-sm text-gray-600">
                    Track all customer licences, expiry status, and account notes.
                </p>
                <span class="mt-2 inline-flex items-center rounded-full border border-sky-200 bg-sky-50 px-2.5 py-0.5 text-xs font-medium text-sky-700">
                    Still in dev, close to completion
                </span>
            </div>

            <div class="w-full md:w-80">
                <label for="licence-search" class="mb-1 block text-sm font-medium text-gray-700">Search</label>
                <input
                    id="licence-search"
                    v-model="searchQuery"
                    type="text"
                    placeholder="Customer, ID, licence number"
                    class="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
            </div>
        </div>

        <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div class="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
                <p class="text-xs font-semibold uppercase tracking-wide text-gray-500">Total Licences</p>
                <p class="mt-2 text-2xl font-bold text-gray-900">{{ totalLicences }}</p>
            </div>

            <div class="rounded-lg border border-green-200 bg-green-50 p-4 shadow-sm">
                <p class="text-xs font-semibold uppercase tracking-wide text-green-700">Active</p>
                <p class="mt-2 text-2xl font-bold text-green-900">{{ activeLicences }}</p>
            </div>

            <div class="rounded-lg border border-amber-200 bg-amber-50 p-4 shadow-sm">
                <p class="text-xs font-semibold uppercase tracking-wide text-amber-700">Expiring in 30 Days</p>
                <p class="mt-2 text-2xl font-bold text-amber-900">{{ expiringSoonLicences }}</p>
            </div>
        </div>

        <div class="rounded-lg border border-gray-200 bg-white shadow-sm">
            <div class="border-b border-gray-200 px-4 py-3">
                <div class="flex items-center justify-between">
                    <h2 class="text-sm font-semibold text-gray-900">Licence Records</h2>
                    <button
                        @click="refetch()"
                        class="rounded-md border border-gray-300 px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-50"
                    >
                        Refresh
                    </button>
                </div>
            </div>

            <div v-if="isLoading" class="px-4 py-10 text-center text-sm text-gray-500">
                Loading licences...
            </div>

            <div v-else-if="isError" class="px-4 py-10 text-center">
                <p class="text-sm font-medium text-red-700">Failed to load licences.</p>
                <p class="mt-1 text-xs text-red-600">{{ errorMessage }}</p>
            </div>

            <div v-else-if="filteredLicences.length === 0" class="px-4 py-10 text-center text-sm text-gray-500">
                No licences found.
            </div>

            <div v-else>
                <div class="hidden overflow-x-auto md:block">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-600">Customer</th>
                                <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-600">Customer ID</th>
                                <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-600">Licence #</th>
                                <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-600">Issued</th>
                                <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-600">Expires</th>
                                <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-600">Status</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-100 bg-white">
                            <tr v-for="licence in filteredLicences" :key="licence.id" class="hover:bg-gray-50">
                                <td class="px-4 py-3 text-sm font-medium text-gray-900">{{ licence.customer_name || 'Unknown Customer' }}</td>
                                <td class="px-4 py-3 text-sm text-gray-700">{{ licence.customer_id }}</td>
                                <td class="px-4 py-3 text-sm text-gray-700">{{ licence.licence_number }}</td>
                                <td class="px-4 py-3 text-sm text-gray-700">{{ formatDate(licence.issued_on) }}</td>
                                <td class="px-4 py-3 text-sm text-gray-700">{{ formatDate(licence.expires_on) }}</td>
                                <td class="px-4 py-3 text-sm">
                                    <span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium" :class="getStatusClass(licence.expires_on)">
                                        {{ getStatusLabel(licence.expires_on) }}
                                    </span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="space-y-3 p-3 md:hidden">
                    <article
                        v-for="licence in filteredLicences"
                        :key="licence.id"
                        class="rounded-md border border-gray-200 bg-white p-3"
                    >
                        <div class="flex items-start justify-between gap-3">
                            <div>
                                <h3 class="text-sm font-semibold text-gray-900">{{ licence.customer_name || 'Unknown Customer' }}</h3>
                                <p class="text-xs text-gray-500">{{ licence.customer_id }} • {{ licence.licence_number }}</p>
                            </div>
                            <span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium" :class="getStatusClass(licence.expires_on)">
                                {{ getStatusLabel(licence.expires_on) }}
                            </span>
                        </div>

                        <div class="mt-3 grid grid-cols-2 gap-2 text-xs text-gray-600">
                            <div>
                                <p class="font-medium text-gray-500">Issued</p>
                                <p>{{ formatDate(licence.issued_on) }}</p>
                            </div>
                            <div>
                                <p class="font-medium text-gray-500">Expires</p>
                                <p>{{ formatDate(licence.expires_on) }}</p>
                            </div>
                        </div>

                        <p v-if="licence.notes" class="mt-2 text-xs text-gray-600">
                            {{ licence.notes }}
                        </p>
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
import { useLicences } from '@/composables/useCustomers'
import type { Licence } from '@/types/field'

const searchQuery = ref('')

const {
    data: licences,
    isLoading,
    isError,
    isFetching,
    error,
    refetch,
} = useLicences()

const safeLicences = computed(() => licences.value ?? [])

const filteredLicences = computed(() => {
    const query = searchQuery.value.trim().toLowerCase()

    if (!query) {
        return safeLicences.value
    }

    return safeLicences.value.filter((licence: Licence) => {
        return [
            licence.customer_name,
            licence.customer_id,
            licence.licence_number,
            licence.notes,
        ]
            .filter(Boolean)
            .some((value) => String(value).toLowerCase().includes(query))
    })
})

const totalLicences = computed(() => safeLicences.value.length)

const activeLicences = computed(() => {
    const now = new Date()
    return safeLicences.value.filter((licence) => {
        const expiryDate = new Date(licence.expires_on)
        return expiryDate >= now
    }).length
})

const expiringSoonLicences = computed(() => {
    const now = new Date()
    const inThirtyDays = new Date()
    inThirtyDays.setDate(inThirtyDays.getDate() + 30)

    return safeLicences.value.filter((licence) => {
        const expiryDate = new Date(licence.expires_on)
        return expiryDate >= now && expiryDate <= inThirtyDays
    }).length
})

const errorMessage = computed(() => {
    if (!error.value) {
        return 'An unknown error occurred.'
    }

    return error.value instanceof Error ? error.value.message : 'Could not fetch licence records.'
})

function formatDate(value: string) {
    const date = new Date(value)
    if (Number.isNaN(date.getTime())) {
        return 'N/A'
    }

    return date.toLocaleDateString('en-GB', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
    })
}

function getStatusClass(expiresOn: string) {
    const status = getStatusLabel(expiresOn)
    if (status === 'Expired') {
        return 'bg-red-100 text-red-800'
    }
    if (status === 'Expiring Soon') {
        return 'bg-amber-100 text-amber-800'
    }
    return 'bg-green-100 text-green-800'
}

function getStatusLabel(expiresOn: string) {
    const now = new Date()
    const expiryDate = new Date(expiresOn)

    if (Number.isNaN(expiryDate.getTime())) {
        return 'Unknown'
    }

    if (expiryDate < now) {
        return 'Expired'
    }

    const thirtyDaysFromNow = new Date()
    thirtyDaysFromNow.setDate(thirtyDaysFromNow.getDate() + 30)

    if (expiryDate <= thirtyDaysFromNow) {
        return 'Expiring Soon'
    }

    return 'Active'
}
</script>