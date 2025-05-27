const express = require('express');
const fetch = require('node-fetch');
const app = express();
const PORT = process.env.PORT || 3001;

app.use(express.json());

app.post('/v1/chat/completions', async (req, res) => {
  const apiKey = process.env.OPENAI_API_KEY || req.body.apiKey;
  if (!apiKey) {
    return res.status(400).json({ error: 'OpenAI APIキーがありません' });
  }
  try {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify(req.body)
    });
    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    res.status(500).json({ error: 'OpenAI APIへのリクエストに失敗しました', details: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`OpenAI Proxy running on http://localhost:${PORT}`);
});