import { useState } from "react";

function LoadTable({ onLoaded }) {
  const [table, setTable] = useState("");

  const loadTable = async () => {
    const res = await fetch(`http://localhost:8000/load-table/${table}`);
    const data = await res.json();

    if (data.message) {
      onLoaded(data);
    } else {
      alert(data.error);
    }
  };

  return (
    <div>
      <input
        placeholder="Enter table name"
        value={table}
        onChange={(e) => setTable(e.target.value)}
      />
      <button onClick={loadTable}>Load Table</button>
    </div>
  );
}

export default LoadTable;
