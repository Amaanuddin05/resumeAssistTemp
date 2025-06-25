const { execFile } = require('child_process');
const path = require('path');

module.exports = function extractTextFromPDF(pdfPath) {
  return new Promise((resolve, reject) => {
    const scriptPath = path.join(__dirname, 'extract_resume_text.py');

    execFile('python3', [scriptPath, pdfPath], (err, stdout, stderr) => {
      if (err) {
        console.error('PyMuPDF extraction error:', stderr);
        return reject(err);
      }
      resolve(stdout.trim());
    });
  });
};
