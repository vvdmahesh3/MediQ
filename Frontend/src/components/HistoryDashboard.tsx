import { useEffect, useState } from "react";
import { ArrowLeft, TrendingUp, TrendingDown, Minus } from "lucide-react";

interface HistoryDashboardProps {
  isDarkMode: boolean;
  onBack: () => void;
}

interface ReportSnapshot {
  report_id: string;
  filename: string;
  timestamp: string;
  health_score: number;
  overall_risk: string;
}

const API_BASE = "http://127.0.0.1:5000";

export default function HistoryDashboard({
  isDarkMode,
  onBack,
}: HistoryDashboardProps) {
  const [reports, setReports] = useState<ReportSnapshot[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/history`)
      .then((res) => res.json())
      .then((data) => {
        setReports(data.reports || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const cardStyle = isDarkMode
    ? "bg-slate-900 border-slate-800 text-white"
    : "bg-white border-slate-200 text-slate-900";

  const getTrendIcon = (index: number) => {
    if (index === 0 || reports.length < 2) return <Minus size={18} />;

    const prev = reports[index - 1].health_score;
    const curr = reports[index].health_score;

    if (curr > prev) return <TrendingUp size={18} className="text-emerald-400" />;
    if (curr < prev)
      return <TrendingDown size={18} className="text-red-400" />;

    return <Minus size={18} />;
  };

  return (
    <div
      className={`min-h-screen px-6 py-10 ${
        isDarkMode ? "bg-[#0F172A]" : "bg-slate-50"
      }`}
    >
      {/* HEADER */}
      <div className="flex items-center gap-4 mb-10">
        <button
          onClick={onBack}
          className="flex items-center gap-2 text-sm font-bold hover:opacity-80"
        >
          <ArrowLeft size={18} />
          Back
        </button>

        <h1 className="text-2xl font-black">Report History</h1>
      </div>

      {/* CONTENT */}
      {loading ? (
        <div className="text-center opacity-60">Loading history...</div>
      ) : reports.length === 0 ? (
        <div className="text-center opacity-60">
          No reports available yet.
        </div>
      ) : (
        <div className="grid gap-5 max-w-3xl">
          {reports.map((report, index) => (
            <div
              key={report.report_id}
              className={`border rounded-2xl p-5 flex justify-between items-center ${cardStyle}`}
            >
              <div>
                <div className="font-bold">{report.filename}</div>
                <div className="text-xs opacity-60">
                  {new Date(report.timestamp).toLocaleString()}
                </div>
                <div className="text-xs mt-1">
                  Risk:{" "}
                  <span className="font-semibold">
                    {report.overall_risk}
                  </span>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="text-xl font-black">
                  {report.health_score}
                </div>
                {getTrendIcon(index)}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}