const express = require('express');
const router = express.Router();

router.get('/health', (req, res) => {
  res.json({ ok: true, service: 'teacher' });
});

router.get('/', (req, res) => {
  res.render('page', { title: 'Teacher Home', who: 'Teacher' });
});

module.exports = router;
