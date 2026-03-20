import { apiClient } from "./api";
import type { Customer, Licence } from "@/types/field";

export const customerService = {
  /**
   * Get all companies from external API
   */
  async getCompanies(): Promise<Customer[]> {
    const response = await apiClient.get<Customer[]>("/customers/companies");
    return response.data;
  },

  /**
   * Get all customer licences from internal API
   */
  async getLicences(): Promise<Licence[]> {
    const response = await apiClient.get<Licence[]>("/customers/licences");
    return response.data;
  },
};
