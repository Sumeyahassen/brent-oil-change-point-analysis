const CATEGORY_COLORS = {
  Conflict: "#f43f5e",
  Economic: "#f59e0b",
  "OPEC Policy": "#3b82f6",
  Sanctions: "#8b5cf6",
  Geopolitical: "#10b981",
};

function Row({ label, value, valueStyle }) {
  return (
    <div className="flex items-start justify-between py-2 border-b border-white/5">
      <span className="text-xs text-slate-500">{label}</span>
      <span className="text-sm text-slate-200 font-medium text-right" style={valueStyle}>{value}</span>
    </div>
  );
}

function EventDetailModal({ event, onClose }) {
  if (!event) return null;

  const accentColor = CATEGORY_COLORS[event.category] || "#94a3b8";

  return (
    <div
      className="fixed inset-0 flex items-center justify-center p-4 z-50"
      style={{ background: "rgba(0,0,0,0.7)", backdropFilter: "blur(4px)" }}
      onClick={onClose}
    >
      <div
        className="rounded-2xl border w-full max-w-md"
        style={{ background: "#0f172a", borderColor: "rgba(255,255,255,0.1)" }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal header accent bar */}
        <div className="h-1 rounded-t-2xl" style={{ background: `linear-gradient(90deg, ${accentColor}, transparent)` }} />

        <div className="p-6">
          <div className="flex items-start justify-between mb-4">
            <div>
              <span
                className="text-xs px-2 py-0.5 rounded-full font-medium border mb-2 inline-block"
                style={{ color: accentColor, borderColor: accentColor + "40", background: accentColor + "15" }}
              >
                {event.category}
              </span>
              <h3 className="text-base font-bold text-white leading-snug">{event.event_name}</h3>
            </div>
            <button
              onClick={onClose}
              className="text-slate-500 hover:text-white text-xl leading-none ml-4 mt-1 transition-colors"
            >
              &times;
            </button>
          </div>

          <div className="space-y-0">
            <Row label="Date" value={event.event_date} />
            {event.description && <Row label="Description" value={event.description} />}
            {event.avg_price_before != null && (
              <>
                <Row label="Avg Price Before" value={`$${event.avg_price_before}`} />
                <Row label="Avg Price After" value={`$${event.avg_price_after}`} />
                <Row
                  label="Price Change"
                  value={`${event.percent_change > 0 ? "+" : ""}${event.percent_change}%`}
                  valueStyle={{ color: event.percent_change > 0 ? "#10b981" : "#f43f5e" }}
                />
                <Row label="Volatility After" value={event.avg_volatility_after} />
              </>
            )}
          </div>

          <button
            onClick={onClose}
            className="mt-5 w-full py-2 rounded-lg text-sm font-medium text-slate-400 border border-white/10 hover:border-white/20 hover:text-slate-200 transition-colors"
            style={{ background: "rgba(255,255,255,0.04)" }}
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

export default EventDetailModal;
