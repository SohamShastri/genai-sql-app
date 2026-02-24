function TableInfo({ tableInfo }) {
  if (!tableInfo) return null;

  return (
    <div>
      <p><b>Rows:</b> {tableInfo.rows}</p>
      <p><b>Columns:</b></p>
      <ul>
        {tableInfo.columns.map(col => (
          <li key={col}>{col}</li>
        ))}
      </ul>
    </div>
  );
}

export default TableInfo;
