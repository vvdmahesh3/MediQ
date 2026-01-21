import React, { useEffect } from "react";
import {
  Activity,
  Brain,
  Shield,
  FileText,
  UploadCloud,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Lock,
  Globe,
  Moon,
  Sun,
} from "lucide-react";

interface LandingPageProps {
  onGetStarted: () => void;
  isDarkMode: boolean;
  setIsDarkMode: (value: boolean) => void;
}

export default function LandingPage({
  onGetStarted,
  isDarkMode,
  setIsDarkMode,
}: LandingPageProps) {
  // Smooth scroll to top on mount
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <div
      className={`min-h-screen transition-colors duration-500 ${
        isDarkMode ? "bg-[#0F172A] text-white" : "bg-slate-50 text-slate-900"
      }`}
    >
      {/* ================= NAVBAR ================= */}
      <nav
        className={`fixed top-0 w-full z-50 border-b transition-all duration-300 backdrop-blur-xl ${
          isDarkMode
            ? "bg-slate-900/80 border-slate-800"
            : "bg-white/70 border-slate-200"
        }`}
      >
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2 group cursor-pointer">
            <div className="w-10 h-10 bg-gradient-to-tr from-blue-600 to-emerald-500 rounded-xl flex items-center justify-center shadow-lg group-hover:rotate-6 transition-transform">
              <Activity className="w-6 h-6 text-white" />
            </div>
            <span
              className={`text-xl font-black tracking-tight ${
                isDarkMode ? "text-white" : "text-slate-800"
              }`}
            >
              Medi<span className="text-blue-600">Q</span>
            </span>
          </div>

          <div className="flex items-center gap-4">
            {/* 🌗 Theme Toggle */}
            <button
              onClick={() => setIsDarkMode(!isDarkMode)}
              className={`p-2 rounded-full transition-colors ${
                isDarkMode
                  ? "hover:bg-slate-800 text-yellow-400"
                  : "hover:bg-slate-100 text-slate-600"
              }`}
            >
              {isDarkMode ? <Sun size={20} /> : <Moon size={20} />}
            </button>

            <button
              onClick={onGetStarted}
              className="px-6 py-2.5 bg-slate-900 dark:bg-blue-600 text-white rounded-xl font-bold text-sm hover:scale-105 active:scale-95 transition-all shadow-xl shadow-blue-500/10"
            >
              Get Started
            </button>
          </div>
        </div>
      </nav>

      {/* ================= HERO SECTION ================= */}
      <main className="max-w-7xl mx-auto px-6 pt-32 pb-20">
        <div className="text-center mb-24 animate-in fade-in slide-in-from-bottom-10 duration-1000">
          <div
            className={`inline-flex items-center gap-2 px-4 py-2 rounded-full text-xs font-black uppercase tracking-[0.2em] mb-8 border animate-bounce-slow ${
              isDarkMode
                ? "bg-blue-500/10 border-blue-500/20 text-blue-400"
                : "bg-blue-50 border-blue-100 text-blue-700"
            }`}
          >
            <Sparkles className="w-3.5 h-3.5" />
            Next-Gen Medical Analysis
          </div>

          <h1 className="text-5xl md:text-7xl font-black mb-8 leading-[1.1] tracking-tight">
            Intelligent Health Analysis <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-emerald-500 to-blue-600 bg-[length:200%_auto] animate-gradient-x">
              At Your Fingertips
            </span>
          </h1>

          <p
            className={`text-lg md:text-xl mb-12 max-w-2xl mx-auto leading-relaxed ${
              isDarkMode ? "text-slate-400" : "text-slate-500"
            }`}
          >
            Upload your medical reports and receive instant AI-powered analysis,
            early risk detection, and personalized recommendations with 99%
            accuracy.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-6">
            <button
              onClick={onGetStarted}
              className="group px-10 py-5 bg-blue-600 text-white rounded-2xl font-black text-lg hover:bg-blue-700 transition-all hover:scale-[1.02] active:scale-95 flex items-center gap-3 shadow-2xl shadow-blue-500/40"
            >
              <UploadCloud size={24} />
              Analyze Report Now
              <ArrowRight className="group-hover:translate-x-1 transition-transform" />
            </button>
          </div>

          {/* Trust Row */}
          <div className="mt-16 flex flex-wrap justify-center gap-8 opacity-60">
            <div className="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest">
              <ShieldCheck className="w-4 h-4 text-emerald-500" /> HIPAA Compliant
            </div>
            <div className="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest">
              <Lock className="w-4 h-4 text-blue-500" /> Encrypted Data
            </div>
            <div className="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest">
              <Globe className="w-4 h-4 text-indigo-500" /> Local Processing
            </div>
          </div>
        </div>

        {/* ================= FEATURE GRID ================= */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-32">
          <FeatureCard
            isDark={isDarkMode}
            icon={<Brain className="w-10 h-10 text-blue-600" />}
            title="Automated Analysis"
            description="Our neural networks extract biomarkers with medical-grade precision instantly."
            delay="delay-0"
          />
          <FeatureCard
            isDark={isDarkMode}
            icon={<Activity className="w-10 h-10 text-emerald-600" />}
            title="Trend Intelligence"
            description="Identify long-term patterns in your bloodwork that manual reviews might miss."
            delay="delay-100"
          />
          <FeatureCard
            isDark={isDarkMode}
            icon={<Shield className="w-10 h-10 text-blue-600" />}
            title="Risk Detection"
            description="Proactive scanning for anomalies and potential future health complications."
            delay="delay-200"
          />
          <FeatureCard
            isDark={isDarkMode}
            icon={<FileText className="w-10 h-10 text-emerald-600" />}
            title="Actionable Plans"
            description="Get dynamic dietary and lifestyle advice based on your specific results."
            delay="delay-300"
          />
        </div>

        {/* ================= STATS SECTION ================= */}
        <div
          className={`rounded-[3rem] p-12 md:p-20 relative overflow-hidden shadow-inner ${
            isDarkMode
              ? "bg-slate-900/50 border border-slate-800"
              : "bg-white border border-slate-100"
          }`}
        >
          <div className="grid md:grid-cols-3 gap-12 text-center relative z-10">
            <Metric value="98.5%" label="Analysis Accuracy" isDark={isDarkMode} />
            <Metric value="<30s" label="Response Time" isDark={isDarkMode} />
            <Metric value="50K+" label="Global Users" isDark={isDarkMode} />
          </div>

          {/* Subtle Background Blobs */}
          <div className="absolute -top-24 -left-24 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl animate-pulse" />
          <div className="absolute -bottom-24 -right-24 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl animate-pulse delay-700" />
        </div>
      </main>
    </div>
  );
}

/* ---------------- Sub-Components ---------------- */

function FeatureCard({ icon, title, description, isDark, delay }: any) {
  return (
    <div
      className={`group p-8 rounded-3xl border transition-all duration-500 hover:-translate-y-3 hover:shadow-2xl animate-in fade-in slide-in-from-bottom-5 ${delay} ${
        isDark
          ? "bg-slate-800/40 border-slate-700 hover:bg-slate-800"
          : "bg-white border-slate-100 hover:border-blue-100"
      }`}
    >
      <div className="mb-6 transform group-hover:scale-110 transition-transform duration-500">
        {icon}
      </div>
      <h3 className="text-xl font-bold mb-3">{title}</h3>
      <p
        className={`text-sm leading-relaxed ${
          isDark ? "text-slate-400" : "text-slate-500"
        }`}
      >
        {description}
      </p>
    </div>
  );
}

function Metric({ value, label, isDark }: any) {
  return (
    <div className="group">
      <div className="text-5xl md:text-6xl font-black text-blue-600 mb-4 group-hover:scale-110 transition-transform tracking-tighter">
        {value}
      </div>
      <div
        className={`text-xs font-black uppercase tracking-[0.2em] ${
          isDark ? "text-slate-500" : "text-slate-400"
        }`}
      >
        {label}
      </div>
    </div>
  );
}