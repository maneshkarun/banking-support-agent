import type {
  Customer,
  Account,
  Balance,
  Transaction,
} from "../types/banking";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, options);
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail ?? "The request could not be completed.");
  }
  return response.json() as Promise<T>;
}

export async function getCustomer(
  customerId: number
): Promise<Customer> {
  return request(`/customers/${customerId}`);
}

export async function getCustomerAccounts(
  customerId: number
): Promise<Account[]> {
  return request(`/customers/${customerId}/accounts`);
}

export async function getBalance(
  customerId: number,
  accountNumber: string
): Promise<Balance> {
  return request(`/customers/${customerId}/accounts/${accountNumber}/balance`);
}

export async function getTransactions(
  customerId: number,
  accountNumber: string,
  limit = 20,
  offset = 0
): Promise<Transaction[]> {
  return request(`/customers/${customerId}/accounts/${accountNumber}/transactions?limit=${limit}&offset=${offset}`);
}

export async function askBankingAgent(message: string): Promise<string> {
  const result = await request<{ response: string }>("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  return result.response;
}
