import { useState } from "react";
import "@/App.css";
import axios from "axios";
import {
  AlertCircle, ArrowUpRight, Check, Globe2, Loader2,
  ScanLine, ShieldCheck, X,
} from "lucide-react";

const API = `${process.env.REACT_APP_BACKEND_URL}/api/scan`;

function App() {
  const [url, setUrl] = useState("https://example.com");
  const [scan, setScan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleScan = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    setScan(null);
    try {
      const response = await axios.post(API, { url });
      setScan(response.data);
    } catch (err) {
      const status = err.response?.status;
      const gatewayMessage = status === 504 ? "Request timed out." : status === 502 ? "Unable to reach this website." : "";
      setError(err.response?.data?.error || gatewayMessage || "Unable to reach this website.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="app-shell">
      <nav className="topbar" data-testid="top-navigation">
        <div className="brand" data-testid="brand-name">
          <span className="brand-mark"><ShieldCheck size={19} /></span> WebGuard
        </div>
        <div className="header-status" data-testid="scanner-status"><span className="status-dot" /> Live scanner</div>
      </nav>

      <section className="hero" data-testid="scanner-intro">
        <p className="eyebrow"><ScanLine size={15} /> Security header intelligence</p>
        <h1>Check your website<br /><span>security posture.</span></h1>
        <p className="hero-copy">A focused, real-time check of the headers that protect your visitors from common web attacks.</p>
      </section>

      <section className="scan-panel" data-testid="scan-panel">
        <div className="panel-label"><span>01</span> Target website</div>
        <form onSubmit={handleScan} className="scan-form" data-testid="scan-form">
          <div className="url-field">
            <Globe2 size={20} />
            <input data-testid="url-input" aria-label="Website URL" value={url} onChange={(e) => setUrl(e.target.value)} placeholder="https://yourwebsite.com" />
          </div>
          <button data-testid="scan-button" type="submit" disabled={loading}>
            {loading ? <><Loader2 className="spin" size={18} /> Scanning</> : <>Scan website <ArrowUpRight size={18} /></>}
          </button>
        </form>
        {error && <div className="error-message" role="alert" data-testid="scan-error"><AlertCircle size={18} /> {error}</div>}
      </section>

      {scan && <section className="results" data-testid="scan-results">
        <div className="results-heading">
          <div><p className="eyebrow">02 / Scan complete</p><h2>Security headers</h2></div>
          <div className="scanned-url" data-testid="scanned-url">{scan.final_url || scan.url}</div>
        </div>
        {scan.ssl_warning && <div className="ssl-warning" data-testid="ssl-warning"><AlertCircle size={18} /> {scan.ssl_warning}</div>}
        <div className="header-list">
          {scan.headers.map((header) => <div className={`header-row ${header.present ? "is-present" : "is-missing"}`} key={header.name} data-testid={`header-result-${header.name.toLowerCase()}`}>
            <div className="result-icon">{header.present ? <Check size={17} /> : <X size={17} />}</div>
            <div><strong>{header.name}</strong><p>{header.present ? "Present" : "Missing"}</p></div>
            <span className="result-state">{header.present ? "Protected" : "Review needed"}</span>
          </div>)}
        </div>
        <div className="summary" data-testid="issues-summary">
          <div><span className="summary-kicker">Security issues found</span><strong>{scan.issues_found}</strong></div>
          <span className="summary-note">of {scan.headers.length} recommended headers missing</span>
        </div>
      </section>}
      <footer data-testid="page-footer">WebGuard <span>·</span> Built for clearer security decisions</footer>
    </main>
  );
}

export default App;
