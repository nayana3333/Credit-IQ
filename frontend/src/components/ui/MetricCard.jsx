export function MetricCard({ label, value, sub, valueColor, accent }) {
  return (
    <div style={{ position: "relative", overflow: "hidden", background: "#FFFFFF", border: "1px solid #E5E5E5", borderRadius: 10, padding: "14px 16px", boxShadow: "0 1px 2px rgba(17,17,17,0.04)" }}>
      {accent && <span style={{ position: "absolute", top: 0, left: 0, right: 0, height: 3, background: accent }} />}
      <p style={{ fontSize: 10, fontWeight: 500, textTransform: "uppercase", letterSpacing: "0.07em", color: "#737373", margin: "0 0 6px" }}>{label}</p>
      <p style={{ fontSize: 24, fontWeight: 600, color: valueColor || "#111111", margin: 0, lineHeight: 1 }}>{value}</p>
      {sub && <p style={{ fontSize: 11, color: "#A3A3A3", marginTop: 5, marginBottom: 0 }}>{sub}</p>}
    </div>
  );
}

export default MetricCard;



