import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, Router } from '@angular/router';
import { NavbarComponent } from '../navbar/navbar.component';

@Component({
  selector: 'app-analyze',
  standalone: true,
  imports: [CommonModule, RouterLink, NavbarComponent],
  templateUrl: './analyze.component.html',
  styleUrl: './analyze.component.scss'
})
export class AnalyzeComponent implements OnInit {
  resumeScore!: number;
  skillsMatch!: number;
  aiATSScore: string = "WIP";
  resumeName!: string;
  date!: string;
  suggestions = {
    summary: [
      'Work in progress',
      'Add a professional summary at the top of your resume.',
      'Highlight your years of experience and key skills.'
    ],
    experience: [
      'Work in progress',
      'Use more action verbs to describe your achievements.',
      'Quantify your impact with numbers where possible.',
      'Tailor your experience to match the job description.'
    ]
  };

  constructor(
    private router: Router
  ){}

  ngOnInit(){
     const data = localStorage.getItem('lastScan');
    if (data) {
      const result = JSON.parse(data);

      this.resumeScore = result.resume_score ?? 0;
      this.skillsMatch = result.skill_match_score ?? 0;
      // this.aiATSScore = result.tfidf_score ?? 85; // or use another metric

      this.resumeName = result.resumeName ?? 'Resume.pdf'
      this.date = result.date ? new Date(result.date).toLocaleDateString() : ''

      // this.suggestions.summary = result.education_suggestions ?? [];
      // this.suggestions.experience = result.experience_suggestions ?? [];

      // Save to history if not already there
      const history = JSON.parse(localStorage.getItem('scanHistory') || '[]');
      const alreadyExists = history.some((entry: any) => entry.timestamp === result.timestamp);
      if (!alreadyExists) {
        result.timestamp = Date.now();
        history.push(result);
        localStorage.setItem('scanHistory', JSON.stringify(history));
      }
    } else {
      // fallback if no scan exists
      alert('No analysis data found. Please upload your resume first.');
      this.router.navigate(['/upload']);
    }
  }


}
