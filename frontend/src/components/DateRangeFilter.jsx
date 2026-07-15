import { useState } from "react";

function DateRangeFilter({ onFilterChange, minDate, maxDate }) {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const applyFilter = () => onFilterChange(startDate || null, endDate || null);

  const resetFilter = () => {
    setStartDate("");
    setEndDate("");
    onFilterChange(null, null);
  };

  const presets = [
    { label: "COVID-19", sub: "2019–2021", start: "2019-06-01", end: "2021-01-01" },
    { label: "OPEC Decision", sub: "2014–2015", start: "2014-08-01", end: "2015-03-31" },
    { label: "Financial Crisis", sub: "2008–2009", start: "2008-01-01", end: "2009-06-30" },
    { label: "Full History", sub: "All time", start: minDate, end: maxDate },
  ];

  const applyPreset = (p) => {
    setStartDate(p.start);
    setEndDate(p.end);
    onFilterChange(p.start, p.end);
  };

  return (
    <div className="rounded-xl border border-white/10 p-4" style={{ background: "rgba(255,255,255,0.04)" }}>
      <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">Date Range Filter</p>

      <div className="flex flex-col sm:flex-row gap-3 items-start sm:items-end mb-3">
        <div className="flex flex-col gap-1">
          <label className="text-xs text-slate-500">Start Date</label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="rounded-lg px-3 py-1.5 text-sm text-slate-200 border border-white/10 focus:outline-none focus:border-blue-500/50"
            style={{ background: "rgba(255,255,255,0.06)" }}
          />
        </div>
        <div className="flex flex-col gap-1">
          <label className="text-xs text-slate-500">End Date</label>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="rounded-lg px-3 py-1.5 text-sm text-slate-200 border border-white/10 focus:outline-none focus:border-blue-500/50"
            style={{ background: "rgba(255,255,255,0.06)" }}
          />
        </div>
        <button
          onClick={applyFilter}
          className="px-5 py-1.5 rounded-lg text-sm font-semibold text-white transition-opacity hover:opacity-90"
          style={{ background: "linear-gradient(135deg, #3b82f6, #6366f1)" }}
        >
          Apply
        </button>
        <button
          onClick={resetFilter}
          className="px-5 py-1.5 rounded-lg text-sm font-medium text-slate-300 border border-white/10 hover:border-white/20 transition-colors"
          style={{ background: "rgba(255,255,255,0.05)" }}
        >
          Reset
        </button>
      </div>

      <div className="flex flex-wrap gap-2">
        {presets.map((p) => (
          <button
            key={p.label}
            onClick={() => applyPreset(p)}
            className="flex flex-col items-start px-3 py-1.5 rounded-lg border border-white/10 hover:border-blue-500/40 hover:bg-blue-500/10 transition-all"
            style={{ background: "rgba(255,255,255,0.03)" }}
          >
            <span className="text-xs font-medium text-slate-300">{p.label}</span>
            <span className="text-xs text-slate-500">{p.sub}</span>
          </button>
        ))}
      </div>
    </div>
  );
}

export default DateRangeFilter;
