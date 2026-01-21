import React, { useState, useRef, useEffect } from "react";
import {
  Upload,
  FileText,
  Image as ImageIcon,
  File,
  X,
  CheckCircle2,
  AlertCircle,
  ShieldCheck,
  Search,
  Lock,
  Clock,
  ArrowRight,
  Database,
  Brain as BrainIcon,
} from "lucide-react";

interface UploadInterfaceProps {
  onUploadComplete: (result: any, file: File) => void;
  onBack: () => void;
  isDarkMode: boolean;
}

const API_BASE = import.meta.env.VITE_API_URL as string;

export default function UploadInterface({
  onUploadComplete,
  onBack,
  isDarkMode,
}: UploadInterfaceProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [estimatedTime, setEstimatedTime] = useState(8);
  const [error, setError] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [apiStatus, setApiStatus] = useState<"online" | "offline">("offline");

  const fileInputRef = useRef<HTMLInputElement>(null);
  const uploadTimerRef = useRef<number | null>(null);

  // Cleanup preview URL
  useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
      if (uploadTimerRef.current) clearInterval(uploadTimerRef.current);
    };
  }, [previewUrl]);

  // ----------------------------
  // 🔌 BACKEND HEALTH MONITOR
  // ----------------------------
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch(`${API_BASE}/health`);
        setApiStatus(res.ok ? "online" : "offline");
      } catch {
        setApiStatus("offline");
      }
    };

    checkHealth();
    const timer = setInterval(checkHealth, 5000);
    return () => clearInterval(timer);
  }, []);

  const handleFileSelect = (file: File) => {
    const validTypes = [
      "application/pdf",
      "image/jpeg",
      "image/png",
      "image/jpg",
      "text/csv",
    ];
    const maxSize = 10 * 1024 * 1024;

    setError(null);

    if (!validTypes.includes(file.type)) {
      setError("Unsupported format. Upload PDF, JPG, PNG or CSV only.");
      return;
    }

    if (file.size > maxSize) {
      setError("File too large. Maximum allowed size is 10MB.");
      return;
    }

    setSelectedFile(file);

    if (previewUrl) URL.revokeObjectURL(previewUrl);

    if (file.type.startsWith("image/")) {
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
    } else {
      setPreviewUrl(null);
    }
  };

  // 🚀 REAL API UPLOAD
  const handleSubmit = async () => {
    if (!selectedFile || isUploading || apiStatus === "offline") return;

    setUploadProgress(0);
    setEstimatedTime(8);
    setIsUploading(true);
    setError(null);

    uploadTimerRef.current = window.setInterval(() => {
      setUploadProgress((prev) => {
        const next = Math.min(prev + 2, 90);
        setEstimatedTime(Math.max(1, Math.ceil((100 - next) / 12)));
        return next;
      });
    }, 80);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Upload failed.");
      }

      const result = await response.json();

      clearInterval(uploadTimerRef.current!);
      setUploadProgress(100);
      setEstimatedTime(0);

      setTimeout(() => {
        onUploadComplete(result, selectedFile);
      }, 600);
    } catch (err) {
      clearInterval(uploadTimerRef.current!);
      setIsUploading(false);
      setUploadProgress(0);
      setError("Backend connection failed. Make sure Flask is running.");
    }
  };

  const getFileIcon = (type: string) => {
    if (type.includes("pdf"))
      return <FileText className="w-12 h-12 text-rose-500 animate-pulse" />;
    if (type.includes("image"))
      return <ImageIcon className="w-12 h-12 text-indigo-500 animate-pulse" />;
    return <File className="w-12 h-12 text-emerald-500 animate-pulse" />;
  };

  return (
    <div
      className={`min-h-screen flex flex-col font-sans transition-colors ${
        isDarkMode ? "bg-[#0F172A] text-white" : "bg-[#F1F5F9] text-slate-900"
      }`}
    >
      {/* NAVBAR */}
      <nav
        className={`backdrop-blur-xl border-b sticky top-0 z-50 ${
          isDarkMode
            ? "bg-slate-900/80 border-slate-800"
            : "bg-white/80 border-slate-200"
        }`}
      >
        <div className="max-w-5xl mx-auto px-6 py-4 flex justify-between">
          <button
            onClick={onBack}
            className={`group flex items-center gap-2 font-bold transition-all text-sm uppercase tracking-widest ${
              isDarkMode
                ? "text-slate-300 hover:text-blue-400"
                : "text-slate-500 hover:text-blue-600"
            }`}
          >
            <span className="group-hover:-translate-x-1 transition-transform inline-block">
              ←
            </span>
            Back
          </button>

          {/* API STATUS */}
          <div
            className={`flex items-center gap-2 px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest ${
              apiStatus === "online"
                ? "bg-emerald-500/10 text-emerald-400"
                : "bg-rose-500/10 text-rose-400"
            }`}
          >
            <span className="w-2 h-2 rounded-full bg-current animate-pulse" />
            API {apiStatus === "online" ? "Online" : "Offline"}
          </div>
        </div>
      </nav>

      <main className="flex-1 max-w-4xl mx-auto w-full px-6 py-12 flex flex-col items-center">
        {/* HEADER */}
        <div className="text-center mb-12">
          <div
            className={`inline-flex items-center gap-2 px-4 py-1.5 rounded-full border text-[10px] font-black uppercase tracking-[0.2em] mb-3 ${
              isDarkMode
                ? "bg-blue-500/10 border-blue-500/20 text-blue-400"
                : "bg-blue-600/10 border-blue-200 text-blue-700"
            }`}
          >
            <ShieldCheck className="w-3 h-3" />
            Secure AI Infrastructure
          </div>

          <h1 className="text-5xl font-black mb-4 tracking-tighter">
            Upload Your Report
          </h1>
          <p
            className={`text-lg max-w-lg mx-auto font-medium ${
              isDarkMode ? "text-slate-400" : "text-slate-500"
            }`}
          >
            AI-powered extraction of biomarkers with medical-grade precision.
          </p>
        </div>

        {/* UPLOAD BOX */}
        <div
          className={`w-full rounded-[3rem] p-3 md:p-10 border relative overflow-hidden transition-colors ${
            isDarkMode
              ? "bg-slate-900 border-slate-800"
              : "bg-white border-slate-100 shadow-[0_32px_64px_-16px_rgba(0,0,0,0.08)]"
          }`}
        >
          <div
            className={`relative border-2 border-dashed rounded-[2.5rem] p-12 text-center transition-all duration-500
            ${
              isDragging
                ? "border-blue-500 bg-blue-500/10 scale-[0.98]"
                : isDarkMode
                ? "border-slate-700 hover:border-blue-500"
                : "border-slate-200 hover:border-blue-400 hover:bg-slate-50/30"
            }
            ${uploadProgress > 0 ? "pointer-events-none" : "cursor-pointer"}`}
            onDragOver={(e) => {
              e.preventDefault();
              setIsDragging(true);
            }}
            onDragLeave={() => setIsDragging(false)}
            onDrop={(e) => {
              e.preventDefault();
              setIsDragging(false);
              const file = e.dataTransfer.files?.[0];
              if (file) handleFileSelect(file);
            }}
            onClick={() =>
              !selectedFile && fileInputRef.current?.click()
            }
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.jpg,.jpeg,.png,.csv"
              onChange={(e) =>
                e.target.files?.[0] &&
                handleFileSelect(e.target.files[0])
              }
              className="hidden"
            />

            {!selectedFile ? (
              <div className="py-12 group">
                <div className="w-24 h-24 bg-gradient-to-tr from-blue-600 to-indigo-700 rounded-3xl flex items-center justify-center mx-auto mb-8 shadow-2xl shadow-blue-500/30 group-hover:rotate-6 transition-transform duration-300">
                  <Upload className="w-10 h-10 text-white" />
                </div>
                <h3 className="text-3xl font-black mb-3">
                  Drop your file here
                </h3>
                <p className="text-slate-400 mb-10 font-bold uppercase text-[10px] tracking-[0.2em]">
                  PDF, Image, or CSV • Max 10MB
                </p>
                <span className="px-10 py-4 bg-slate-900 text-white rounded-2xl font-black text-sm hover:bg-blue-600 transition-all shadow-xl hover:-translate-y-1 active:scale-95">
                  Browse Files
                </span>
              </div>
            ) : (
              <div className="space-y-8">
                <div
                  className={`flex flex-col md:flex-row items-center gap-8 p-8 rounded-[2rem] border ${
                    isDarkMode
                      ? "bg-slate-800 border-slate-700"
                      : "bg-slate-50 border-slate-200/50"
                  }`}
                >
                  <div className="w-28 h-28 rounded-2xl bg-white border overflow-hidden flex items-center justify-center shrink-0 shadow-inner">
                    {previewUrl ? (
                      <img
                        src={previewUrl}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      getFileIcon(selectedFile.type)
                    )}
                  </div>

                  <div className="flex-1 min-w-0">
                    <h4 className="font-black text-xl truncate mb-1">
                      {selectedFile.name}
                    </h4>
                    <span className="text-xs font-black text-slate-400 uppercase tracking-widest">
                      {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                    </span>
                  </div>

                  {uploadProgress === 0 && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        setSelectedFile(null);
                        setUploadProgress(0);
                      }}
                      className="p-3 hover:bg-rose-500/10 text-slate-400 hover:text-rose-400 rounded-2xl transition-all"
                    >
                      <X className="w-6 h-6" />
                    </button>
                  )}
                </div>

                {uploadProgress > 0 && (
                  <div className="space-y-4 px-4">
                    <div className="flex justify-between text-[11px] font-black uppercase tracking-widest text-slate-400">
                      <span className="flex items-center gap-2">
                        {uploadProgress < 100 ? (
                          <>
                            <Clock className="w-4 h-4 animate-spin" />
                            Est. {estimatedTime}s remaining
                          </>
                        ) : (
                          <>
                            <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                            Completed
                          </>
                        )}
                      </span>
                      <span className="text-blue-500">
                        {uploadProgress}%
                      </span>
                    </div>

                    <div className="h-3 bg-slate-800/30 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full transition-all duration-300"
                        style={{ width: `${uploadProgress}%` }}
                      />
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          <div className="mt-8 flex flex-col md:flex-row justify-between items-center px-4 gap-6">
            <div className="flex items-center gap-6 opacity-40 hover:opacity-100 transition-opacity text-[10px] font-black uppercase">
              <div className="flex items-center gap-1.5">
                <Database className="w-3 h-3" /> No Storage
              </div>
              <div className="flex items-center gap-1.5">
                <Lock className="w-3 h-3" /> Encrypted
              </div>
              <div className="flex items-center gap-1.5">
                <ShieldCheck className="w-3 h-3" /> Secure
              </div>
            </div>

            {selectedFile && uploadProgress === 0 && (
              <button
                onClick={handleSubmit}
                disabled={isUploading || apiStatus === "offline"}
                className={`w-full md:w-auto px-10 py-5 rounded-[1.5rem] font-black text-sm transition-all shadow-xl flex items-center justify-center gap-3 active:scale-[0.98] ${
                  apiStatus === "offline"
                    ? "bg-slate-600 text-slate-300 cursor-not-allowed"
                    : "bg-blue-600 text-white hover:bg-blue-700 shadow-blue-500/30"
                }`}
              >
                Start Analysis
                <ArrowRight className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>

        {error && (
          <div className="mt-8 p-5 bg-rose-500/10 border border-rose-500/20 rounded-[1.5rem] flex items-center gap-4 text-rose-400 text-sm font-black">
            <AlertCircle className="w-6 h-6 shrink-0" />
            {error}
          </div>
        )}

        {/* INFO CARDS */}
        <div className="grid md:grid-cols-3 gap-6 mt-16 w-full">
          <InfoCard
            isDark={isDarkMode}
            icon={<Search className="w-5 h-5" />}
            step="01"
            title="OCR Scanning"
            desc="Digitizing every cell with high-fidelity vision models."
          />
          <InfoCard
            isDark={isDarkMode}
            icon={<BrainIcon className="w-5 h-5" />}
            step="02"
            title="AI Inference"
            desc="Comparing values against clinical reference standards."
          />
          <InfoCard
            isDark={isDarkMode}
            icon={<FileText className="w-5 h-5" />}
            step="03"
            title="Health Mapping"
            desc="Building your personalized metabolic dashboard."
          />
        </div>
      </main>
    </div>
  );
}

function InfoCard({
  step,
  title,
  desc,
  icon,
  isDark,
}: {
  step: string;
  title: string;
  desc: string;
  icon: React.ReactNode;
  isDark: boolean;
}) {
  return (
    <div
      className={`border p-8 rounded-[2rem] hover:shadow-xl hover:-translate-y-1 transition-all duration-300 text-left ${
        isDark
          ? "bg-slate-900 border-slate-800"
          : "bg-white/60 border-white"
      }`}
    >
      <div className="flex items-center justify-between mb-4">
        <span className="text-blue-500 font-black text-[10px] tracking-[0.2em]">
          {step}
        </span>
        <div className="text-slate-400">{icon}</div>
      </div>
      <h3 className="font-black mb-2 uppercase text-xs">
        {title}
      </h3>
      <p className="text-sm text-slate-500 leading-relaxed font-medium">
        {desc}
      </p>
    </div>
  );
}