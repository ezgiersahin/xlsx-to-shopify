import React, { useState } from 'react';

function App() {
  const [file, setFile] = useState(null);
  const [csvUrl, setCsvUrl] = useState(null);

  const handleChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("/api/convert", {
      method: "POST",
      body: formData,
    });

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    setCsvUrl(url);
  };

  return (
    <div style={{ padding: 40, fontFamily: 'Arial' }}>
      <h1>Excel'den Shopify CSV Dönüştürücü</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept=".xlsx" onChange={handleChange} />
        <button type="submit">Dönüştür</button>
      </form>
      {csvUrl && (
        <div style={{ marginTop: 20 }}>
          <a href={csvUrl} download="shopify.csv">CSV Dosyasını İndir</a>
        </div>
      )}
    </div>
  );
}

export default App;
