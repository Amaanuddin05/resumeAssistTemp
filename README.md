# ResumeAssist

**AI‑powered Resume Analysis and Optimization**

ResumeAssist helps job seekers instantly analyze their resumes against a target job description using NLP and machine learning. It scores resumes for ATS‑compatibility, skill matches, and readability, and provides AI‑driven suggestions to optimize summary and experience sections.

---

## 🚀 Features

* **Resume Text Extraction**: Parses PDF or text resumes with `PyMuPDF` & custom parser.
* **Skill Matching**: Extracts skills from resume and job description via a hybrid approach:

  * SpaCy PhraseMatcher with a curated JSON skill list.
  * Fallback noun‑chunk extraction & junk‑phrase filtering.
* **Scoring Metrics**:

  * **ATS Score**: Evaluates keyword coverage & formatting.
  * **Skill Match Score**: Percentage overlap of target skills.
  * **Readability & TF‑IDF**: (WIP) AI‑driven readability/TF‑IDF scoring.
* **AI Suggestions**: Tailored improvement tips for summary and experience.
* **Scan History**: Saves last scan and history in browser `localStorage`.
* **Responsive UI**: Angular + Tailwind CSS frontend with modern, animated design.
* **One‑click Deployment**: Netlify configuration included for static hosting.

---

## 📦 Tech Stack

| Layer       | Technology                             |
| ----------- | -------------------------------------- |
| Frontend    | Angular 19, TypeScript, Tailwind CSS   |
| Backend API | Node.js, Express.js                    |
| ML & NLP    | Python 3, Scikit‑learn, SpaCy, PyMuPDF |
| Data store  | JSON files (`skills_all_merged.json`)  |
| Hosting     | Netlify                                |

---

## 📂 Repository Structure

```
amaanuddin05-resumeassist/
├── netlify.toml                  # Netlify build & redirect config
├── frontend/                     # Angular + Tailwind UI
│   ├── README.md                 # Frontend local dev instructions
│   ├── src/                      # Application source code
│   │   ├── app/                  # Components: navbar, home, upload, analyze, report
│   │   ├── styles.scss           # Global & Tailwind imports
│   │   └── index.html, main.ts   # Bootstrap & entry point
│   ├── angular.json              # Angular CLI config
│   ├── package.json              # Frontend dependencies & scripts
│   └── ...                       # TS configs, PostCSS, EditorConfig
└── server/                       # Backend & ML logic
    ├── index.js                  # Express server entrypoint
    ├── routes/analyze.js         # API route for resume/job analysis
    ├── utils/                    # Text extraction & parsing helpers
    │   ├── extract_resume_text.py# PDF/text extraction
    │   └── resumeParser.js       # Additional parsing logic
    ├── ml/                       # ML scoring module
    │   ├── score.py              # TF‑IDF, keyword/skill scoring
    │   └── skills_all_merged.json# ML skill list reference
    ├── requirements.txt          # Python dependencies
    └── package.json              # Node.js dependencies & server scripts
```

---

## 🔧 Prerequisites

* **Node.js** v18+ & **npm**
* **Python** 3.9+ with `pip`
* **Angular CLI** (optional, for global ng commands)

---

## 🛠 Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/amaanuddin05/amaanuddin05-resumeassist.git
   cd amaanuddin05-resumeassist
   ```

2. **Setup Backend**

   ```bash
   cd server
   npm install                # Install Node.js dependencies
   pip install -r requirements.txt  # Install Python packages
   ```

3. **Setup Frontend**

   ```bash
   cd ../frontend
   npm install                # Install Angular & Tailwind dependencies
   ```

---

## 🔄 Development

### Run Backend API

```bash
cd server
npm run dev       # Starts Express server (nodemon)
```

### Run Frontend App

```bash
cd frontend
npm start         # ng serve on http://localhost:4200
```

Browse to `http://localhost:4200`, upload a resume and job description to see analysis in action.

---

## 📦 Production Build & Deployment

### Frontend

```bash
cd frontend
npm run build -- --configuration production
```

Artifacts will be in `frontend/dist/frontend/browser` and served by Netlify or any static host.

### Backend

Use your preferred Node.js/Python hosting or containerize. Ensure the ML dependencies are installed.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Commit changes: `git commit -m "feat: add ..."`
4. Push to branch and open a PR

Please follow the existing code style and write unit tests for new features.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

*Happy job hunting!*
