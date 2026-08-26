import { useEffect, useState } from "react";

import type {
  Account,
  Customer,
} from "../types/banking";

import {
  getCustomer,
  getCustomerAccounts,
} from "../services/api";

import AccountCard from "../components/AccountCard";

export default function Dashboard() {
  const customerId = 1;

  const [customer, setCustomer] =
    useState<Customer | null>(null);

  const [accounts, setAccounts] =
    useState<Account[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  useEffect(() => {
    async function loadDashboard() {
      try {
        setLoading(true);

        const [customerData, accountData] =
          await Promise.all([
            getCustomer(customerId),
            getCustomerAccounts(customerId),
          ]);

        setCustomer(customerData);
        setAccounts(accountData);
      } catch (err) {
        setError("Unable to load dashboard");
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  if (loading) {
    return <p>Loading dashboard...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <main>
      <h1>
        Welcome, {customer?.full_name}
      </h1>

      <h2>Your Accounts</h2>

      {accounts.map((account) => (
        <AccountCard
          key={account.account_number}
          account={account}
        />
      ))}
    </main>
  );
}