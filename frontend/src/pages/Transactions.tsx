import { useEffect, useState } from "react";
import type { Transaction } from "../types/banking";
import { getTransactions } from "../services/api";

interface TransactionsProps {
  customerId: number;
  accountNumber: string;
}

export default function Transactions({ customerId, accountNumber }: TransactionsProps) {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let ignore = false;
    setLoading(true);
    setError(null);
    getTransactions(customerId, accountNumber)
      .then((data) => !ignore && setTransactions(data))
      .catch((reason: Error) => !ignore && setError(reason.message))
      .finally(() => !ignore && setLoading(false));
    return () => { ignore = true; };
  }, [customerId, accountNumber]);

  if (loading) return <p className="panel-message">Loading activity…</p>;
  if (error) return <p className="panel-message panel-message--error">{error}</p>;
  if (!transactions.length) return <p className="panel-message">No transactions recorded for this account yet.</p>;

  return (
    <div className="transaction-list">
      {transactions.map((transaction) => {
        const isCredit = transaction.transaction_type === "credit";
        return (
          <article className="transaction" key={transaction.id}>
            <span className={`transaction__icon ${isCredit ? "transaction__icon--credit" : "transaction__icon--debit"}`}>{isCredit ? "↓" : "↑"}</span>
            <div className="transaction__description">
              <strong>{transaction.description || (isCredit ? "Money received" : "Payment")}</strong>
              <span>{new Date(transaction.created_at).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" })} · {transaction.reference}</span>
            </div>
            <strong className={isCredit ? "money money--positive" : "money"}>
              {isCredit ? "+" : "−"}{new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR" }).format(Number(transaction.amount))}
            </strong>
          </article>
        );
      })}
    </div>
  );
}
