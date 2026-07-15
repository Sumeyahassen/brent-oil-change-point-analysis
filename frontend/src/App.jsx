import { useEffect, useState } from "react";
import { getPrices, getEvents, getChangepoints, getEventCorrelation, getStats } from "./services/api";
import StatsCards from "./components/StatsCards";
import DateRangeFilter from "./components/DateRangeFilter";
import PriceChart from "./components/PriceChart";
import EventsPanel from "./components/EventsPanel";
import EventDetailModal from "./components/EventDetailModal";
import ChangePointsPanel from "./components/ChangePointsPanel";

function App() {
  const [prices, setPrices] = useState([]);
  const [events, setEvents] = useState([]);
  const [correlation, setCorrelation] = useState([]);
  const [changepoints, setChangepoints] = useState([]);
  const [stats, setStats] = useState(null);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadAll = async (startDate = null, endDate = null) => {
    setLoading(true);
    setError(null);
    try {
      const [pricesData, eventsData, cpData, corrData, statsData] = await Promise.all([
        getPrices(startDate, endDate),
        getEvents(),
        getChangepoints(),
        getEventCorrelation(),
        getStats(),
      ]);
      setPrices(pricesData);
      setEvents(eventsData);
      setChangepoints(cpData);
      setCorrelation(corrData);
      setStats(statsData);
    } catch (err) {
      setError("Could not connect to backend. Is Flask running on port 5000?");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadAll(); }, []);

  return (
    <div className="min-h-screen" style={{ background: "linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%)" }}>
      {/* Header */}
      <header className="border-b border-white/10 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ background: "linear-gradient(135deg, #3b82f6, #8b5cf6)" }}>
                <span className="text-white text-sm font-bold">B</span>
              </div>
              <h1 className="text-xl font-bold text-white tracking-tight">Brent Oil Dashboard</h1>
            </div>
            <p className="text-slate-400 text-xs ml-11">Birhan Energies — Bayesian structural break analysis</p>
          </div>
          <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full border border-white/10" style={{ background: "rgba(255,255,255,0.05)" }}>
            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-xs text-slate-300">Live Data</span>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 md:px-6 py-6 flex flex-col gap-5">
        {error && (
          <div className="flex items-center gap-3 rounded-xl px-4 py-3 border border-red-500/30 text-red-300 text-sm" style={{ background: "rgba(239,68,68,0.1)" }}>
            <span className="text-red-400">⚠</span>
            {error}
          </div>
        )}

        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="flex flex-col items-center gap-4">
              <div className="w-10 h-10 border-2 border-blue-500/30 border-t-blue-500 rounded-full animate-spin" />
              <p className="text-slate-400 text-sm">Loading dashboard data...</p>
            </div>
          </div>
        ) : (
          <>
            <StatsCards stats={stats} />
            <DateRangeFilter
              onFilterChange={loadAll}
              minDate={stats?.date_range_start}
              maxDate={stats?.date_range_end}
            />
            <PriceChart
              prices={prices}
              events={events}
              changepoints={changepoints}
              onEventClick={setSelectedEvent}
            />
            <ChangePointsPanel changepoints={changepoints} />
            <EventsPanel correlation={correlation} onSelectEvent={setSelectedEvent} />
          </>
        )}
      </main>

      <EventDetailModal event={selectedEvent} onClose={() => setSelectedEvent(null)} />
    </div>
  );
}

export default App;
