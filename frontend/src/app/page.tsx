import Link from "next/link";
import { ArrowRight, CheckCircle2, ShieldCheck, Sparkles } from "lucide-react";

const capabilities = [
  "OWASP Top 10 for LLM Applications coverage",
  "NIST AI RMF-aligned governance signals",
  "Actionable findings with deterministic remediation guidance",
];

export default function HomePage() {
  return (
    <main className="min-h-screen overflow-hidden px-6 py-8 sm:px-10 lg:px-16">
      <nav className="mx-auto flex max-w-7xl items-center justify-between">
        <Link href="/" className="flex items-center gap-3 text-lg font-semibold tracking-tight text-white">
          <span className="flex h-10 w-10 items-center justify-center rounded-xl border border-cyan-300/30 bg-cyan-300/10 text-cyan-200">
            <ShieldCheck size={23} />
          </span>
          Aegis AI Auditor
        </Link>
        <Link
          href="/dashboard"
          className="rounded-lg border border-slate-700 bg-slate-900/80 px-4 py-2 text-sm font-medium text-slate-200 transition hover:border-cyan-400/50 hover:text-cyan-200"
        >
          Open dashboard
        </Link>
      </nav>

      <section className="mx-auto grid max-w-7xl gap-14 pb-20 pt-20 lg:grid-cols-[1.1fr_0.9fr] lg:items-center lg:pt-28">
        <div>
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-cyan-300/20 bg-cyan-300/10 px-3 py-1.5 text-sm text-cyan-100">
            <Sparkles size={15} />
            Security governance for the agentic AI era
          </div>
          <h1 className="max-w-4xl text-5xl font-semibold leading-[1.02] tracking-tight text-white sm:text-6xl lg:text-7xl">
            Secure your LLM workflows against the OWASP Top 10.
          </h1>
          <p className="mt-7 max-w-2xl text-lg leading-8 text-slate-300 sm:text-xl">
            Aegis AI Auditor exposes prompt injection, unsafe tool execution, embedded secrets, system-prompt leakage, and risky retrieval patterns before they become production incidents.
          </p>
          <div className="mt-9 flex flex-col gap-4 sm:flex-row sm:items-center">
            <Link
              href="/dashboard"
              className="inline-flex items-center justify-center gap-2 rounded-xl bg-cyan-300 px-5 py-3.5 font-semibold text-slate-950 transition hover:bg-cyan-200"
            >
              Run a free audit <ArrowRight size={18} />
            </Link>
            <span className="text-sm text-slate-400">No deployment required for your first scan.</span>
          </div>
          <ul className="mt-10 space-y-3">
            {capabilities.map((capability) => (
              <li key={capability} className="flex items-center gap-3 text-sm text-slate-300">
                <CheckCircle2 size={18} className="shrink-0 text-emerald-400" />
                {capability}
              </li>
            ))}
          </ul>
        </div>

        <div className="relative rounded-3xl border border-slate-700/80 bg-slate-950/70 p-6 shadow-2xl shadow-cyan-950/30 backdrop-blur sm:p-8">
          <div className="absolute -inset-px -z-10 rounded-3xl bg-gradient-to-br from-cyan-400/25 via-transparent to-indigo-500/20 blur-xl" />
          <div className="flex items-center justify-between border-b border-slate-800 pb-5">
            <div>
              <p className="text-sm font-medium text-slate-100">Audit snapshot</p>
              <p className="mt-1 text-xs text-slate-500">agent-orchestrator.ts</p>
            </div>
            <span className="rounded-full bg-rose-400/10 px-3 py-1 text-xs font-semibold text-rose-300">HIGH RISK</span>
          </div>
          <div className="space-y-4 py-6">
            <div className="rounded-xl border border-rose-400/20 bg-rose-400/5 p-4">
              <p className="text-sm font-semibold text-rose-200">Critical · Hardcoded credential</p>
              <p className="mt-2 text-sm leading-6 text-slate-400">Rotate the exposed key and replace it with a managed secret reference.</p>
            </div>
            <div className="rounded-xl border border-amber-400/20 bg-amber-400/5 p-4">
              <p className="text-sm font-semibold text-amber-200">High · Prompt injection indicator</p>
              <p className="mt-2 text-sm leading-6 text-slate-400">Isolate untrusted context and require structured tool-call validation.</p>
            </div>
          </div>
          <div className="grid grid-cols-3 gap-3 border-t border-slate-800 pt-5 text-center">
            <div><p className="text-2xl font-semibold text-white">62</p><p className="text-xs text-slate-500">Risk score</p></div>
            <div><p className="text-2xl font-semibold text-white">4</p><p className="text-xs text-slate-500">Findings</p></div>
            <div><p className="text-2xl font-semibold text-white">2</p><p className="text-xs text-slate-500">Frameworks</p></div>
          </div>
        </div>
      </section>
    </main>
  );
}
