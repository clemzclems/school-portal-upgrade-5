const express = require('express');
const router = express.Router();

router.get('/health', (req, res) => {
  res.json({ ok: true, service: 'student' });
});

router.get('/', (req, res) => {
  res.render('page', { title: 'Student Home', who: 'Student' });
});

module.exports = router;
