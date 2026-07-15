function StatsCards({ stats }) {
  if (!stats) return null;

  const cards = [
    {
      label: "Average Price",
      value: `$${stats.avg_price}`,
      icon: "◈",
      gradient: "from-blue-500/20 to-blue-600/5",
      accent: "#3b82f6",
      border: "border-blue-500/20",
    },
    {
      label: "Min Price",
      value: `$${stats.min_price}`,
      icon: "↓",
      gradient: "from-emerald-500/20 to-emerald-600/5",
      accent: "#10b981",
      border: "border-emerald-500/20",
    },
    {
      label: "Max Price",
      value: `$${stats.max_price}`,
      icon: "↑",
      gradient: "from-rose-500/20 to-rose-600/5",
      accent: "#f43f5e",
      border: "border-rose-500/20",
    },
    {
      label: "Total Days",
      value: stats.total_days.toLocaleString(),
      icon: "◷",
      gradient: "from-slate-500/20 to-slate-600/5",
      accent: "#94a3b8",
      border: "border-slate-500/20",
    },
    {
      label: "Peak Volatility",
      value: `${stats.highest_volatility_period.volatility}`,
      sub: stats.highest_volatility_period.date,
      icon: "⚡",
      gradient: "from-amber-500/20 to-amber-600/5",
      accent: "#f59e0b",
      border: "border-amber-500/20",
    },
    {
      label: "Avg Volatility",
      value: stats.avg_daily_volatility,
      icon: "~",
      gradient: "from-violet-500/20 to-violet-600/5",
      accent: "#8b5cf6",
      border: "border-violet-500/20",
    },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
      {cards.map((card) => (
        <div
          key={card.label}
          className={`stat-card bg-gradient-to-br ${card.gradient} border ${card.border}`}
        >
          <div className="flex items-center justify-between mb-3">
            <p className="text-xs text-slate-400 font-medium">{card.label}</p>
            <span className="text-sm" style={{ color: card.accent }}>{card.icon}</span>
          </div>
          <p className="text-xl font-bold text-white">{card.value}</p>
          {card.sub && <p className="text-xs text-slate-500 mt-1">{card.sub}</p>}
        </div>
      ))}
    </div>
  );
}

export default StatsCards;
