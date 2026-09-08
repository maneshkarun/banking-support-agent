import { useState } from "react";
import Dashboard from "./pages/Dashboard";
import { askBankingAgent } from "./services/api";
import "./App.css";

type ChatMessage = { role: "user" | "agent"; text: string };

export default function App() {
  const [customerId, setCustomerId] = useState(1);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [draft, setDraft] = useState("");
  const [sending, setSending] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([{ role: "agent", text: "Hi! I’m the banking assistant. Ask me to check a balance, find an account, or explain recent activity." }]);
  async function sendMessage(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault(); const message = draft.trim(); if (!message || sending) return;
    setMessages((current) => [...current, { role: "user", text: message }]); setDraft(""); setSending(true);
    try { const response = await askBankingAgent(message); setMessages((current) => [...current, { role: "agent", text: response }]); }
    catch (error) { setMessages((current) => [...current, { role: "agent", text: `I couldn’t reach the banking agent. ${error instanceof Error ? error.message : "Please try again."}` }]); }
    finally { setSending(false); }
  }
  return <>
    <header className="topbar"><a className="brand" href="/"><span className="brand-mark">B</span>banking<span>./agent</span></a><div className="topbar__right"><span className="secure-label">● Secure demo environment</span><button className="avatar" type="button" aria-label="Customer profile">{customerId}</button></div></header>
    <Dashboard customerId={customerId} onCustomerIdChange={setCustomerId} />
    <button aria-expanded={isChatOpen} className="chat-toggle" onClick={() => setIsChatOpen((open) => !open)} type="button">{isChatOpen ? "×" : "✦"}<span>{isChatOpen ? "Close" : "Ask agent"}</span></button>
    {isChatOpen ? <aside className="chat-panel" aria-label="Banking agent chat"><header><div><span className="agent-dot">✦</span><div><strong>Banking assistant</strong><small>Agent tools enabled</small></div></div><button aria-label="Close chat" onClick={() => setIsChatOpen(false)} type="button">×</button></header><div className="messages">{messages.map((item, index) => <p className={`message message--${item.role}`} key={index}>{item.text}</p>)}{sending ? <p className="message message--agent">Thinking…</p> : null}</div><form onSubmit={sendMessage}><input aria-label="Message the banking assistant" onChange={(event) => setDraft(event.target.value)} placeholder="Ask about your banking…" value={draft} /><button disabled={!draft.trim() || sending} type="submit">↑</button></form></aside> : null}
  </>;
}
