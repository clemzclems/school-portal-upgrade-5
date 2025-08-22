const express = require('express');
const router = express.Router();

router.get('/health', (req, res) => {
  res.json({ ok: true, service: 'jobs' });
});

router.get('/', (req, res) => {
  res.render('page', { title: 'Jobs', who: 'Jobs Board' });
});

module.exports = router;
