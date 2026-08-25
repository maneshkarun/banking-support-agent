import type { Account } from "../types/banking";

interface AccountCardProps {
  account: Account;
}

export default function AccountCard({
  account,
}: AccountCardProps) {
  return (
    <div>
      <h3>{account.account_type}</h3>

      <p>
        {account.currency} {account.balance}
      </p>

      <p>
        ****{account.account_number.slice(-4)}
      </p>

      <p>{account.status}</p>
    </div>
  );
}