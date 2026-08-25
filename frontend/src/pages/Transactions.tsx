import { useEffect, useState } from "react";
import type { Transaction } from "../types/banking";
import { getTransactions } from "../services/api";

export default function Transactions() {
  const accountNumber = "YOUR_ACCOUNT_NUMBER";

  const [transactions, setTransactions] = useState<Transaction[]>([]);

  useEffect(() => {
    async function loadTransactions() {
      const data = await getTransactions(accountNumber);

      setTransactions(data);
    }

    loadTransactions();
  }, []);

  return (
    <div>
      <h1>Transactions</h1>

      {transactions.map((transaction) => (
        <div key={transaction.id}>
          <p>
            {transaction.transaction_type}
          </p>

          <p>
            {transaction.amount}
          </p>

          <p>
            {transaction.description}
          </p>

          <small>
            {transaction.created_at}
          </small>
        </div>
      ))}
    </div>
  );
}