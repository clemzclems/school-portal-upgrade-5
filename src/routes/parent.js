const express = require('express');
const router = express.Router();

router.get('/health', (req, res) => {
  res.json({ ok: true, service: 'parent' });
});

router.get('/', (req, res) => {
  res.render('page', { title: 'Parent Home', who: 'Parent' });
});

module.exports = router;
