import { useMemo } from "react";
import type { AvailabilityBlock } from "../types";

function inBlock(iso: string, blocks: AvailabilityBlock[]) {
  return blocks.some((b) => iso >= b.date_from && iso <= b.date_to);
}

export default function AvailabilityCalendar({ blocks }: { blocks: AvailabilityBlock[] }) {
  const days = useMemo(() => {
    const start = new Date();
    start.setDate(1);
    const list: { iso: string; day: number; past: boolean; blocked: boolean }[] = [];
    const year = start.getFullYear();
    const month = start.getMonth();
    const count = new Date(year, month + 1, 0).getDate();
    const today = new Date().toISOString().slice(0, 10);
    for (let d = 1; d <= count; d++) {
      const iso = `${year}-${String(month + 1).padStart(2, "0")}-${String(d).padStart(2, "0")}`;
      list.push({ iso, day: d, past: iso < today, blocked: inBlock(iso, blocks) });
    }
    return list;
  }, [blocks]);

  return (
    <div>
      <div className="calendar">
        {["P", "U", "S", "Č", "P", "S", "N"].map((d) => (
          <div key={d} className="day head">
            {d}
          </div>
        ))}
        {days.map((d) => (
          <div key={d.iso} className={`day ${d.past ? "past" : d.blocked ? "blocked" : ""}`} title={d.iso}>
            {d.day}
          </div>
        ))}
      </div>
      <p className="meta" style={{ marginTop: 10 }}>
        Zeleno = potencijalno dostupno · Crveno = blokirano · Sivo = prošlo
      </p>
    </div>
  );
}
