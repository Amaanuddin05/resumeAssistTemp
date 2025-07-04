const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const extractTextFromPDF = require('../utils/resumeParser');
const { spawn } = require('child_process');

const router = express.Router();

// Multer setup
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, path.join(__dirname, '../uploads'));
  },
  filename: function (req, file, cb) {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, uniqueSuffix + '-' + file.originalname);
  }
});
const upload = multer({
  storage,
  fileFilter: (req, file, cb) => {
    if (file.mimetype === 'application/pdf') {
      cb(null, true);
    } else {
      cb(new Error('Only PDF files are allowed!'));
    }
  }
});

function runScoringScript(resumeText, jdText) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python3', [path.join(__dirname, '../ml/score.py')]);

    let result = '';
    let error = '';

    pythonProcess.stdout.on('data', data => result += data.toString());
    pythonProcess.stderr.on('data', data => {
      error += data.toString();
      console.error('[PYTHON STDERR]:', data.toString()); // 🔥 Add this
    });

    pythonProcess.on('close', code => {
      if (code !== 0) {
        console.error('[PYTHON ERROR CODE]', code);
        reject(new Error(error || 'Python script failed'));
      } else {
        try {
          resolve(JSON.parse(result));
        } catch (e) {
          console.error('[PYTHON PARSE ERROR]', e);
          reject(new Error('Failed to parse Python output'));
        }
      }
    });

    // Debug input
    console.log('[RUNNING PYTHON] Resume length:', resumeText.length);
    console.log('[RUNNING PYTHON] JD length:', jdText.length);

    const payload = JSON.stringify({ resume: resumeText.trim(), jd: jdText.trim() });
    pythonProcess.stdin.write(payload);
    pythonProcess.stdin.end();
  });
}


// POST /analyze
router.post('/', upload.single('resume'), async (req, res) => {
  const { jobTitle, jobDescription } = req.body;
  const file = req.file;

  console.log('Job Title:', jobTitle);
  console.log('Job Description:', jobDescription);
  if (file) {
    console.log('Resume file received:', file.filename);
    try {
      const parsedText = await extractTextFromPDF(file.path);
      // fs.writeFileSync('extracted_resume.txt', parsedText);
      console.log('Resume text preview:', parsedText.slice(0, 300));
      if (!parsedText || parsedText.trim().split(/\s+/).length < 10) {
        return res.status(400).json({ error: 'Resume text too short or empty.' });
      }
      // Optional: delete file after parsing
      fs.unlinkSync(file.path);

      // ML scoring
      const scoringResult = await runScoringScript(parsedText, jobDescription);
      res.json(scoringResult);
    } catch (err) {
      console.error('Error:', err);
      res.status(500).json({ error: err.message || 'Failed to process resume.' });
    }
  } else {
    console.log('No file received');
    res.status(400).json({ error: 'No resume file received.' });
  }
});

module.exports = router;
