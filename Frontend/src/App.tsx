import { useState, useEffect } from "react";
import LandingPage from "./components/LandingPage";
import UploadInterface from "./components/UploadInterface";
import ProcessingScreen from "./components/ProcessingScreen";
import ResultsDashboard from "./components/ResultsDashboard";
import HistoryDashboard from "./components/HistoryDashboard";

type Screen = "landing" | "upload" | "processing" | "results" | "history";

function App() {
  const [currentScreen, setCurrentScreen] = useState<Screen>("landing");
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [analysisResult, setAnalysisResult] = useState<any>(null);

  // 🌗 GLOBAL THEME STATE
  const [isDarkMode, setIsDarkMode] = useState<boolean>(() => {
    const saved = localStorage.getItem("theme");
    return saved === "dark";
  });

  useEffect(() => {
    localStorage.setItem("theme", isDarkMode ? "dark" : "light");
    document.documentElement.classList.toggle("dark", isDarkMode);
  }, [isDarkMode]);

  // -------------------------------
  // Navigation
  // -------------------------------

  const goToLanding = () => setCurrentScreen("landing");
  const goToUpload = () => setCurrentScreen("upload");
  const goToResults = () => setCurrentScreen("results");
  const goToHistory = () => setCurrentScreen("history");

  const handleUploadComplete = (result: any, file: File) => {
    setUploadedFile(file);
    setAnalysisResult(result);
    setCurrentScreen("processing");
  };

  const resetFlow = () => {
    setUploadedFile(null);
    setAnalysisResult(null);
    setCurrentScreen("landing");
  };

  // -------------------------------
  // Render Controller
  // -------------------------------

  const renderScreen = () => {
    switch (currentScreen) {
      case "landing":
        return (
          <LandingPage
            onGetStarted={goToUpload}
            isDarkMode={isDarkMode}
            setIsDarkMode={setIsDarkMode}
          />
        );

      case "upload":
        return (
          <UploadInterface
            onUploadComplete={handleUploadComplete}
            onBack={goToLanding}
            isDarkMode={isDarkMode}
          />
        );

      case "processing":
        return (
          <ProcessingScreen
            onComplete={goToResults}
            isDarkMode={isDarkMode}
          />
        );

      case "results":
        return (
          <ResultsDashboard
            uploadedFile={uploadedFile}
            result={analysisResult}
            onStartNew={resetFlow}
            isDarkMode={isDarkMode}
            onViewHistory={goToHistory}
          />
        );

      case "history":
        return (
          <HistoryDashboard
            isDarkMode={isDarkMode}
            onBack={goToResults}
          />
        );

      default:
        return null;
    }
  };

  return (
    <div
      className={`min-h-screen w-full overflow-hidden transition-colors duration-500 ${
        isDarkMode ? "bg-[#0F172A]" : "bg-slate-50"
      }`}
    >
      {renderScreen()}
    </div>
  );
}

export default App;