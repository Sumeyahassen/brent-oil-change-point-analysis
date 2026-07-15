function ChangePointsPanel({ changepoints }) {
  if (!changepoints || changepoints.length === 0) return null;

  return (
    <div className="rounded-xl border border-white/10 p-5" style={{ background: "rgba(255,255,255,0.04)" }}>
      <div className="mb-4">
        <h2 className="text-sm font-semibold text-white">Detected Change Points</h2>
        <p className="text-xs text-slate-500 mt-0.5">Bayesian structural breaks with quantified impact</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {changepoints.map((cp) => {
          const isIncrease = cp.percent_change > 0;
          return (
            <div
              key={cp.change_point_date}
              className="rounded-xl border p-4"
              style={{
                background: "rgba(255,255,255,0.03)",
                borderColor: isIncrease ? "rgba(16,185,129,0.2)" : "rgba(244,63,94,0.2)",
              }}
            >
              <div className="flex items-center justify-between mb-3">
                <div>
                  <p className="text-xs text-slate-500 mb-0.5">{cp.window_analyzed}</p>
                  <p className="text-base font-bold text-white">{cp.change_point_date}</p>
                </div>
                <span
                  className="text-sm font-bold px-2 py-0.5 rounded-lg"
                  style={{
                    color: isIncrease ? "#10b981" : "#f43f5e",
                    background: isIncrease ? "rgba(16,185,129,0.1)" : "rgba(244,63,94,0.1)",
                  }}
                >
                  {isIncrease ? "+" : ""}{cp.percent_change}%
                </span>
              </div>

              <p className="text-sm text-slate-400 leading-relaxed">
                Following <span className="text-slate-200 font-medium">{cp.likely_event}</span>{" "}
                around {cp.likely_event_date} ({cp.days_from_event} days prior), average daily price
                shifted from{" "}
                <span className="text-slate-200 font-semibold">${cp.avg_price_before}</span> to{" "}
                <span className="text-slate-200 font-semibold">${cp.avg_price_after}</span>.
              </p>

              <div className="mt-3 pt-3 border-t border-white/5 flex items-center gap-2">
                <div className="flex-1 h-1.5 rounded-full bg-white/5 overflow-hidden">
                  <div
                    className="h-full rounded-full"
                    style={{
                      width: `${(cp.probability_increase * 100).toFixed(0)}%`,
                      background: "linear-gradient(90deg, #3b82f6, #8b5cf6)",
                    }}
                  />
                </div>
                <span className="text-xs text-slate-500 whitespace-nowrap">
                  {(cp.probability_increase * 100).toFixed(1)}% prob. increase
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default ChangePointsPanel;
