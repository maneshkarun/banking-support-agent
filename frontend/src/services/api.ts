import type {
  Customer,
  Account,
  Balance,
  Transaction,
} from "../types/banking";

const API_URL = "http://localhost:8000/api/v1";

export async function getCustomer(
  customerId: number
): Promise<Customer> {
  const response = await fetch(
    `${API_URL}/customers/${customerId}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch customer");
  }

  return response.json();
}

export async function getCustomerAccounts(
  customerId: number
): Promise<Account[]> {
  const response = await fetch(
    `${API_URL}/customers/${customerId}/accounts`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch accounts");
  }

  return response.json();
}

export async function getBalance(
  customerId: number,
  accountNumber: string
): Promise<Balance> {
  const response = await fetch(
    `${API_URL}/customers/${customerId}/accounts/${accountNumber}/balance`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch balance");
  }

  return response.json();
}

export async function getTransactions(
  accountNumber: string,
  limit = 20,
  offset = 0
): Promise<Transaction[]> {
  const response = await fetch(
    `${API_URL}/accounts/${accountNumber}/transactions?limit=${limit}&offset=${offset}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch transactions");
  }

  return response.json();
}