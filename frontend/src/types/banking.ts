export interface Customer {
  id: number;
  full_name: string;
  email: string;
  phone: string | null;
  created_at: string;
}

export interface Account {
  account_number: string;
  customer_id: number;
  account_type: string;
  status: string;
  currency: string;
  balance: number;
  created_at: string;
}

export interface Balance {
  account_number: string;
  currency: string;
  balance: number;
}

export interface Transaction {
  id: number;
  account_id: number;
  transaction_type: string;
  amount: number;
  description: string | null;
  reference: string;
  created_at: string;
}