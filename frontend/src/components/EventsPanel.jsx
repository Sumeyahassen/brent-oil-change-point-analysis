import { useState } from "react";

const CATEGORY_COLORS = {
  Conflict: { bg: "rgba(244,63,94,0.1)", text: "#f43f5e", border: "rgba(244,63,94,0.3)" },
  Economic: { bg: "rgba(245,158,11,0.1)", text: "#f59e0b", border: "rgba(245,158,11,0.3)" },
  "OPEC Policy": { bg: "rgba(59,130,246,0.1)", text: "#3b82f6", border: "rgba(59,130,246,0.3)" },
  Sanctions: { bg: "rgba(139,92,246,0.1)", text: "#8b5cf6", border: "rgba(139,92,246,0.3)" },
  Geopolitical: { bg: "rgba(16,185,129,0.1)", text: "#10b981", border: "rgba(16,185,129,0.3)" },
};

function CategoryBadge({ category }) {
  const c = CATEGORY_COLORS[category] || { bg: "rgba(148,163,184,0.1)", text: "#94a3b8", border: "rgba(148,163,184,0.3)" };
  return (
    <span
      className="text-xs px-2 py-0.5 rounded-full font-medium border"
      style={{ background: c.bg, color: c.text, borderColor: c.border }}
    >
      {category}
    </span>
  );
}

function EventsPanel({ correlation, onSelectEvent }) {
  const [sortKey, setSortKey] = useState("event_date");
  const [sortAsc, setSortAsc] = useState(true);

  const sorted = [...correlation].sort((a, b) => {
    const valA = a[sortKey], valB = b[sortKey];
    if (valA === null) return 1;
    if (valB === null) return -1;
    if (typeof valA === "string") return sortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
    return sortAsc ? valA - valB : valB - valA;
  });

  const toggleSort = (key) => {
    if (sortKey === key) setSortAsc(!sortAsc);
    else { setSortKey(key); setSortAsc(true); }
  };

  const columns = [
    { key: "event_date", label: "Date" },
    { key: "event_name", label: "Event" },
    { key: "category", label: "Category" },
    { key: "percent_change", label: "% Change" },
    { key: "avg_volatility_after", label: "Volatility" },
  ];

  return (
    <div className="rounded-xl border border-white/10 p-5" style={{ background: "rgba(255,255,255,0.04)" }}>
      <div className="mb-4">
        <h2 className="text-sm font-semibold text-white">Event Correlation</h2>
        <p className="text-xs text-slate-500 mt-0.5">Click a row to see event details</p>
      </div>

      <div className="overflow-x-auto rounded-lg border border-white/5">
        <table className="w-full text-sm min-w-[600px]">
          <thead>
            <tr style={{ background: "rgba(255,255,255,0.04)" }}>
              {columns.map((col) => (
                <th
                  key={col.key}
                  onClick={() => toggleSort(col.key)}
                  className="py-2.5 px-4 text-xs font-semibold text-slate-400 cursor-pointer hover:text-white whitespace-nowrap text-left transition-colors select-none"
                >
                  {col.label}{" "}
                  {sortKey === col.key && (
                    <span className="text-blue-400">{sortAsc ? "↑" : "↓"}</span>
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sorted.map((row, i) => (
              <tr
                key={row.event_name}
                onClick={() => onSelectEvent(row)}
                className="border-t border-white/5 cursor-pointer transition-colors"
                style={{ background: i % 2 === 0 ? "transparent" : "rgba(255,255,255,0.01)" }}
                onMouseEnter={(e) => e.currentTarget.style.background = "rgba(59,130,246,0.06)"}
                onMouseLeave={(e) => e.currentTarget.style.background = i % 2 === 0 ? "transparent" : "rgba(255,255,255,0.01)"}
              >
                <td className="py-2.5 px-4 text-slate-400 whitespace-nowrap text-xs">{row.event_date}</td>
                <td className="py-2.5 px-4 text-slate-200 font-medium">{row.event_name}</td>
                <td className="py-2.5 px-4"><CategoryBadge category={row.category} /></td>
                <td className="py-2.5 px-4 font-semibold">
                  <span style={{ color: row.percent_change > 0 ? "#10b981" : "#f43f5e" }}>
                    {row.percent_change !== null ? `${row.percent_change > 0 ? "+" : ""}${row.percent_change}%` : "—"}
                  </span>
                </td>
                <td className="py-2.5 px-4 text-slate-400 text-xs">{row.avg_volatility_after ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default EventsPanel;
