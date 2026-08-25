import { useEffect, useState } from "react";
import type { Account, Customer } from "../types/banking";
import {
  getCustomer,
  getCustomerAccounts,
} from "../services/api";

export default function Dashboard() {
  const customerId = 1;

  const [customer, setCustomer] = useState<Customer | null>(null);
  const [accounts, setAccounts] = useState<Account[]>([]);

  useEffect(() => {
    async function loadDashboard() {
      const customerData = await getCustomer(customerId);
      const accountData = await getCustomerAccounts(customerId);

      setCustomer(customerData);
      setAccounts(accountData);
    }

    loadDashboard();
  }, []);

  return (
    <div>
      <h1>
        Welcome, {customer?.full_name}
      </h1>

      <h2>Your Accounts</h2>

      {accounts.map((account) => (
        <div key={account.account_number}>
          <h3>{account.account_type}</h3>

          <p>
            {account.currency} {account.balance}
          </p>

          <p>
            Account: {account.account_number}
          </p>
        </div>
      ))}
    </div>
  );
}