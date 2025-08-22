const express = require('express');
const router = express.Router();

router.get('/health', (req, res) => {
  res.json({ ok: true, service: 'admin' });
});

router.get('/', (req, res) => {
  res.render('page', { title: 'Admin Home', who: 'Admin' });
});

module.exports = router;
