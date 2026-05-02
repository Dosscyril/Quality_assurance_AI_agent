import { PieChart, Pie, Cell, Text } from "recharts";

export default function ScoreChart({ score }) {
  const data = [
    { name: "Score", value: score },
    { name: "Remaining", value: 100 - score }
  ];

  const COLORS =
    score > 80
      ? ["#22c55e", "#374151"]
      : score > 50
      ? ["#facc15", "#374151"]
      : ["#ef4444", "#374151"];

  return (
    <PieChart width={200} height={200}>
      <Pie
        data={data}
        dataKey="value"
        innerRadius={50}
        outerRadius={80}
        isAnimationActive
      >
        {data.map((entry, index) => (
          <Cell key={index} fill={COLORS[index]} />
        ))}
      </Pie>

      <Text
        x={100}
        y={100}
        textAnchor="middle"
        dominantBaseline="middle"
        fill="#fff"
        fontSize={18}
      >
        {score}%
      </Text>
    </PieChart>
  );
}