import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, ReferenceLine,
} from "recharts";

const CATEGORY_COLORS = {
  Conflict: "#f43f5e",
  Economic: "#f59e0b",
  "OPEC Policy": "#3b82f6",
  Sanctions: "#8b5cf6",
  Geopolitical: "#10b981",
};

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="rounded-lg border border-white/10 px-3 py-2 text-sm" style={{ background: "#1e293b" }}>
      <p className="text-slate-400 text-xs mb-1">{label}</p>
      <p className="text-white font-semibold">${payload[0].value.toFixed(2)}</p>
    </div>
  );
}

function PriceChart({ prices, events, changepoints, onEventClick }) {
  const chartData = prices.map((p) => ({ date: p.Date, price: p.Price }));

  return (
    <div className="rounded-xl border border-white/10 p-5" style={{ background: "rgba(255,255,255,0.04)" }}>
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-sm font-semibold text-white">Brent Crude Oil Price</h2>
          <p className="text-xs text-slate-500 mt-0.5">With event markers and detected change points</p>
        </div>
      </div>

      <ResponsiveContainer width="100%" height={360}>
        <LineChart data={chartData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
          <defs>
            <linearGradient id="priceGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#3b82f6" stopOpacity={0.3} />
              <stop offset="100%" stopColor="#3b82f6" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 10, fill: "#64748b" }}
            axisLine={{ stroke: "rgba(255,255,255,0.08)" }}
            tickLine={false}
            minTickGap={40}
          />
          <YAxis
            tick={{ fontSize: 11, fill: "#64748b" }}
            axisLine={false}
            tickLine={false}
            width={45}
          />
          <Tooltip content={<CustomTooltip />} />
          <Line
            type="monotone"
            dataKey="price"
            stroke="#3b82f6"
            strokeWidth={1.5}
            dot={false}
            activeDot={{ r: 4, fill: "#3b82f6", strokeWidth: 0 }}
          />

          {events
            .filter((e) => e.event_date >= chartData[0]?.date && e.event_date <= chartData[chartData.length - 1]?.date)
            .map((event) => (
              <ReferenceLine
                key={event.event_name}
                x={event.event_date}
                stroke={CATEGORY_COLORS[event.category] || "#64748b"}
                strokeDasharray="4 2"
                strokeOpacity={0.7}
                onClick={() => onEventClick(event)}
                style={{ cursor: "pointer" }}
              />
            ))}

          {changepoints.map((cp) => (
            <ReferenceLine
              key={cp.change_point_date}
              x={cp.change_point_date}
              stroke="#facc15"
              strokeWidth={2}
              strokeOpacity={0.9}
              label={{ value: "CP", fontSize: 9, fill: "#facc15", position: "insideTopRight" }}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>

      <div className="flex flex-wrap gap-4 mt-4 pt-3 border-t border-white/5">
        {Object.entries(CATEGORY_COLORS).map(([cat, color]) => (
          <div key={cat} className="flex items-center gap-1.5">
            <span className="w-3 h-0.5 rounded-full" style={{ backgroundColor: color }} />
            <span className="text-xs text-slate-500">{cat}</span>
          </div>
        ))}
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-0.5 rounded-full bg-yellow-400" />
          <span className="text-xs text-slate-500">Change Point</span>
        </div>
      </div>
    </div>
  );
}

export default PriceChart;
