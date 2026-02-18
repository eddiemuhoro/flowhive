<!-- Customer Billing Report Component -->
<!-- Shows billable vs non-billable hours breakdown per customer -->

<template>
  <div class="rounded-lg bg-white p-6 shadow-sm">
    <h2 class="text-lg font-semibold text-gray-900 mb-4">
      Customer Billing Summary
    </h2>

    <!-- Overall Billing Stats -->
    <div class="grid grid-cols-2 gap-6 md:grid-cols-4 mb-6 pb-6 border-b">
      <div>
        <p class="text-sm text-gray-600">Total Billable Hours</p>
        <p class="mt-1 text-2xl font-bold text-green-600">
          {{ billingSummary.billableHours.toFixed(1) }}h
        </p>
        <p class="text-xs text-gray-500">{{ billingSummary.billableVisits }} visits</p>
      </div>
      <div>
        <p class="text-sm text-gray-600">Non-Billable Hours</p>
        <p class="mt-1 text-2xl font-bold text-gray-600">
          {{ billingSummary.nonBillableHours.toFixed(1) }}h
        </p>
        <p class="text-xs text-gray-500">{{ billingSummary.officeActivities }} tasks</p>
      </div>
      <div>
        <p class="text-sm text-gray-600">Billing Rate</p>
        <p class="mt-1 text-2xl font-bold text-blue-600">
          {{ billingSummary.billingPercentage.toFixed(1) }}%
        </p>
        <p class="text-xs text-gray-500">of total hours</p>
      </div>
      <div>
        <p class="text-sm text-gray-600">Customers to Bill</p>
        <p class="mt-1 text-2xl font-bold text-gray-900">
          {{ billingSummary.billableCustomers }}
        </p>
        <p class="text-xs text-gray-500">with on-site visits</p>
      </div>
    </div>

    <!-- Customer Breakdown Table -->
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead>
          <tr class="bg-gray-50">
            <th class="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase">
              Customer Name
            </th>
            <th class="px-4 py-3 text-center text-xs font-semibold text-gray-700 uppercase">
              On-Site Visits
            </th>
            <th class="px-4 py-3 text-center text-xs font-semibold text-gray-700 uppercase">
              Office Tasks
            </th>
            <th class="px-4 py-3 text-right text-xs font-semibold text-gray-700 uppercase">
              Billable Hours
            </th>
            <th class="px-4 py-3 text-right text-xs font-semibold text-gray-700 uppercase">
              Non-Billable Hours
            </th>
            <th class="px-4 py-3 text-right text-xs font-semibold text-gray-700 uppercase">
              Total Hours
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 bg-white">
          <tr
            v-for="customer in customerBillingBreakdown"
            :key="customer.name"
            class="hover:bg-gray-50"
          >
            <td class="px-4 py-3 text-sm font-medium text-gray-900">
              {{ customer.name }}
            </td>
            <td class="px-4 py-3 text-sm text-center">
              <span
                v-if="customer.onSiteVisits > 0"
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"
              >
                {{ customer.onSiteVisits }}
              </span>
              <span v-else class="text-gray-400">-</span>
            </td>
            <td class="px-4 py-3 text-sm text-center">
              <span
                v-if="customer.officeActivities > 0"
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
              >
                {{ customer.officeActivities }}
              </span>
              <span v-else class="text-gray-400">-</span>
            </td>
            <td class="px-4 py-3 text-sm text-right font-semibold text-green-600">
              {{ customer.billableHours > 0 ? customer.billableHours.toFixed(1) + 'h' : '-' }}
            </td>
            <td class="px-4 py-3 text-sm text-right text-gray-600">
              {{ customer.nonBillableHours > 0 ? customer.nonBillableHours.toFixed(1) + 'h' : '-' }}
            </td>
            <td class="px-4 py-3 text-sm text-right font-semibold text-gray-900">
              {{ customer.totalHours.toFixed(1) }}h
            </td>
          </tr>
        </tbody>
        <tfoot class="bg-gray-50 border-t-2 border-gray-300">
          <tr>
            <td class="px-4 py-3 text-sm font-bold text-gray-900">
              TOTAL
            </td>
            <td class="px-4 py-3 text-sm text-center font-bold text-gray-900">
              {{ billingSummary.billableVisits }}
            </td>
            <td class="px-4 py-3 text-sm text-center font-bold text-gray-900">
              {{ billingSummary.officeActivities }}
            </td>
            <td class="px-4 py-3 text-sm text-right font-bold text-green-600">
              {{ billingSummary.billableHours.toFixed(1) }}h
            </td>
            <td class="px-4 py-3 text-sm text-right font-bold text-gray-900">
              {{ billingSummary.nonBillableHours.toFixed(1) }}h
            </td>
            <td class="px-4 py-3 text-sm text-right font-bold text-gray-900">
              {{ (billingSummary.billableHours + billingSummary.nonBillableHours).toFixed(1) }}h
            </td>
          </tr>
        </tfoot>
      </table>
    </div>

    <!-- Empty State -->
    <div
      v-if="customerBillingBreakdown.length === 0"
      class="text-center py-12"
    >
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
          d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
        />
      </svg>
      <p class="mt-2 text-sm text-gray-500">
        No activities found for the selected period
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { LocationType, type FieldActivity } from '@/types/field';

interface Props {
  activities: FieldActivity[];
}

const props = defineProps<Props>();

interface CustomerBilling {
  name: string;
  onSiteVisits: number;
  officeActivities: number;
  billableHours: number;
  nonBillableHours: number;
  totalHours: number;
}

// Calculate billing breakdown per customer
const customerBillingBreakdown = computed(() => {
  const customerMap = new Map<string, CustomerBilling>();

  props.activities.forEach(activity => {
    const key = activity.customer_name || 'Unknown Customer';

    if (!customerMap.has(key)) {
      customerMap.set(key, {
        name: key,
        onSiteVisits: 0,
        officeActivities: 0,
        billableHours: 0,
        nonBillableHours: 0,
        totalHours: 0,
      });
    }

    const customer = customerMap.get(key)!;
    const hours = activity.duration_hours || 0;

    if (activity.location_type === LocationType.ON_SITE) {
      customer.onSiteVisits++;
      customer.billableHours += hours;
    } else {
      customer.officeActivities++;
      customer.nonBillableHours += hours;
    }
    customer.totalHours += hours;
  });

  // Sort by billable hours (highest first)
  return Array.from(customerMap.values())
    .sort((a, b) => b.billableHours - a.billableHours);
});

// Calculate overall billing summary
const billingSummary = computed(() => {
  let billableHours = 0;
  let nonBillableHours = 0;
  let billableVisits = 0;
  let officeActivities = 0;
  const customersWithBillableVisits = new Set<string>();

  props.activities.forEach(activity => {
    const hours = activity.duration_hours || 0;

    if (activity.location_type === LocationType.ON_SITE) {
      billableHours += hours;
      billableVisits++;
      if (activity.customer_name) {
        customersWithBillableVisits.add(activity.customer_name);
      }
    } else {
      nonBillableHours += hours;
      officeActivities++;
    }
  });

  const totalHours = billableHours + nonBillableHours;
  const billingPercentage = totalHours > 0 ? (billableHours / totalHours) * 100 : 0;

  return {
    billableHours,
    nonBillableHours,
    billableVisits,
    officeActivities,
    billingPercentage,
    billableCustomers: customersWithBillableVisits.size,
  };
});
</script>
