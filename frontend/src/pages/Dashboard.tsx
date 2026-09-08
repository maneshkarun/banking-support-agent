import { useEffect, useState } from "react";
import type { Account, Customer } from "../types/banking";
import { getCustomer, getCustomerAccounts } from "../services/api";
import AccountCard from "../components/AccountCard";
import Transactions from "./Transactions";

interface DashboardProps { customerId: number; onCustomerIdChange: (id: number) => void; }

export default function Dashboard({ customerId, onCustomerIdChange }: DashboardProps) {
  const [customer, setCustomer] = useState<Customer | null>(null);
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [selectedAccount, setSelectedAccount] = useState<Account | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [customerInput, setCustomerInput] = useState(String(customerId));
  useEffect(() => {
    let ignore = false; setLoading(true); setError(null);
    Promise.all([getCustomer(customerId), getCustomerAccounts(customerId)]).then(([c, a]) => { if (!ignore) { setCustomer(c); setAccounts(a); setSelectedAccount(a[0] ?? null); } }).catch((reason: Error) => !ignore && setError(reason.message)).finally(() => !ignore && setLoading(false));
    return () => { ignore = true; };
  }, [customerId]);
  const totalBalance = accounts.reduce((total, account) => total + Number(account.balance), 0);
  function submitCustomer(event: React.FormEvent<HTMLFormElement>) { event.preventDefault(); const id = Number(customerInput); if (Number.isInteger(id) && id > 0) onCustomerIdChange(id); }
  return <main className="dashboard">
    <section className="welcome-row"><div><p className="eyebrow">YOUR FINANCIAL OVERVIEW</p><h1>{loading ? "Loading your accounts…" : `Good morning, ${customer?.full_name?.split(" ")[0] ?? "there"}.`}</h1><p className="intro">A clear view of your accounts and recent activity.</p></div><form className="customer-switcher" onSubmit={submitCustomer}><label htmlFor="customer-id">Demo customer ID</label><div><input id="customer-id" inputMode="numeric" min="1" onChange={(event) => setCustomerInput(event.target.value)} type="number" value={customerInput} /><button type="submit">Load</button></div></form></section>
    {error ? <section className="notice"><strong>Couldn’t load customer {customerId}.</strong><span>{error}. Try a customer ID that exists in the API database.</span></section> : null}
    {!loading && !error ? <><section className="summary-grid" aria-label="Account summary"><article className="balance-card balance-card--primary"><span>Total balance</span><strong>{new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR" }).format(totalBalance)}</strong><small>Across {accounts.length} account{accounts.length === 1 ? "" : "s"}</small></article><article className="balance-card"><span>Customer since</span><strong>{customer ? new Date(customer.created_at).toLocaleDateString("en-IN", { month: "short", year: "numeric" }) : "—"}</strong><small>{customer?.email}</small></article><article className="balance-card"><span>Agent status</span><strong className="agent-live"><i /> Ready</strong><small>Ask about balances, transfers, or transactions</small></article></section>
    <section className="content-grid"><div className="accounts-panel"><div className="section-heading"><div><p className="eyebrow">ACCOUNTS</p><h2>Choose an account</h2></div><span>{accounts.length} total</span></div><div className="account-grid">{accounts.map((account) => <AccountCard account={account} key={account.account_number} onSelect={() => setSelectedAccount(account)} selected={selectedAccount?.account_number === account.account_number} />)}</div>{!accounts.length ? <p className="panel-message">This customer does not have any accounts yet.</p> : null}</div><section className="activity-panel"><div className="section-heading"><div><p className="eyebrow">RECENT ACTIVITY</p><h2>{selectedAccount ? `•••• ${selectedAccount.account_number.slice(-4)}` : "Select an account"}</h2></div></div>{selectedAccount ? <Transactions accountNumber={selectedAccount.account_number} customerId={customerId} /> : <p className="panel-message">Select an account to see its activity.</p>}</section></section></> : null}
  </main>;
}
