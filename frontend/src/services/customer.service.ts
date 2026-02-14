import { apiClient } from "./api";
import type { Customer } from "@/types/field";

export const customerService = {
  /**
   * Get all companies from external API
   */
  async getCompanies(): Promise<Customer[]> {
    const response = await apiClient.get<Customer[]>("/customers/companies");
    return response.data;
  },
};
