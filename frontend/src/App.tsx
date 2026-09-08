import { useState } from "react";
import Dashboard from "./pages/Dashboard";
import { askBankingAgent } from "./services/api";
import type { Account } from "./types/banking";
import "./App.css";

type ChatMessage = {
  role: "user" | "agent";
  text: string;
  accountOptions?: Account[];
};

export default function App() {
  const [customerId, setCustomerId] = useState(1);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [draft, setDraft] = useState("");
  const [sending, setSending] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: "agent", text: "Hi! I'm the banking assistant. Ask me to find a customer's accounts or check a balance." },
  ]);

  async function submitAgentMessage(message: string) {
    if (!message || sending) return;
    setMessages((current) => [...current, { role: "user", text: message }]);
    setSending(true);
    try {
      const result = await askBankingAgent(message);
      setMessages((current) => [...current, {
        role: "agent",
        text: result.response,
        accountOptions: result.account_options,
      }]);
    } catch (error) {
      const detail = error instanceof Error ? error.message : "Please try again.";
      setMessages((current) => [...current, { role: "agent", text: `I couldn't reach the banking agent. ${detail}` }]);
    } finally { setSending(false); }
  }

  function sendMessage(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const message = draft.trim();
    setDraft("");
    void submitAgentMessage(message);
  }

  function selectAccount(account: Account) {
    void submitAgentMessage(`Show complete account details for account number ${account.account_number}.`);
  }

  return <>
    <header className="topbar"><a className="brand" href="/"><span className="brand-mark">B</span>banking<span>./agent</span></a><div className="topbar__right"><span className="secure-label">Secure demo environment</span><button className="avatar" type="button" aria-label="Customer profile">{customerId}</button></div></header>
    <Dashboard customerId={customerId} onCustomerIdChange={setCustomerId} />
    <button aria-expanded={isChatOpen} className="chat-toggle" onClick={() => setIsChatOpen((open) => !open)} type="button">{isChatOpen ? "x" : "*"}<span>{isChatOpen ? "Close" : "Ask agent"}</span></button>
    {isChatOpen ? <aside className="chat-panel" aria-label="Banking agent chat"><header><div><span className="agent-dot">*</span><div><strong>Banking assistant</strong><small>Agent tools enabled</small></div></div><button aria-label="Close chat" onClick={() => setIsChatOpen(false)} type="button">x</button></header><div className="messages">{messages.map((item, index) => <div className={`message message--${item.role}`} key={index}><p>{item.text}</p>{item.accountOptions?.length ? <div className="account-options" aria-label="Select an account">{item.accountOptions.map((account) => <button key={account.account_number} onClick={() => selectAccount(account)} type="button"><span><strong>{account.account_type} account</strong><small>{account.account_number}</small></span><span>{formatMoney(account.balance, account.currency)}</span></button>)}</div> : null}</div>)}{sending ? <div className="message message--agent"><p>Thinking...</p></div> : null}</div><form onSubmit={sendMessage}><input aria-label="Message the banking assistant" onChange={(event) => setDraft(event.target.value)} placeholder="Ask about your banking..." value={draft} /><button disabled={!draft.trim() || sending} type="submit">Send</button></form></aside> : null}
  </>;
}

function formatMoney(amount: string, currency: string) {
  return new Intl.NumberFormat("en-IN", { style: "currency", currency }).format(Number(amount));
}
