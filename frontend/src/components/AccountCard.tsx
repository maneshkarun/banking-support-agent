import type { Account } from "../types/banking";

interface AccountCardProps {
  account: Account;
  selected: boolean;
  onSelect: () => void;
}

export default function AccountCard({
  account,
  selected,
  onSelect,
}: AccountCardProps) {
  const accountType =
    account.account_type === "savings"
      ? "Savings Account"
      : "Checking Account";

  return (
    <button className={`account-card ${selected ? "account-card--selected" : ""}`} onClick={onSelect} type="button" aria-pressed={selected}>
      <span className="account-card__topline">
        <span className="account-card__icon">{accountType.charAt(0)}</span>
        <span className={`status status--${account.status}`}>{account.status}</span>
      </span>
      <span className="account-card__type">{accountType}</span>
      <strong>{formatMoney(account.balance, account.currency)}</strong>
      <span className="account-card__number">•••• {account.account_number.slice(-4)}</span>
    </button>
  );
}

function formatMoney(amount: string, currency: string) {
  return new Intl.NumberFormat("en-IN", { style: "currency", currency }).format(Number(amount));
}
