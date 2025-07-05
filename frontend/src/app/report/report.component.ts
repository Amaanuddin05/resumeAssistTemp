import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { NavbarComponent } from '../navbar/navbar.component';

@Component({
  selector: 'app-report',
  standalone: true,
  imports: [CommonModule, RouterLink, NavbarComponent],
  templateUrl: './report.component.html',
  styleUrl: './report.component.scss'
})
export class ReportComponent implements OnInit {
  resumeScore!: number;
  skillsMatch!: number;
  aiAtsScore: string = 'WIP';
  jobTitle: string = 'Frontend Developer';
  date: string = '';
  resumeName: string = ''
  jobDescription: string = `We are seeking a skilled Frontend Developer to join our team. The ideal candidate will have experience with Angular, TypeScript, and modern CSS frameworks. Responsibilities include building responsive web applications, collaborating with designers, and optimizing performance.`;
  suggestions = {
    summary: [
      'Add a concise professional summary at the top.',
      'Mention years of experience and core technologies.'
    ],
    experience: [
      'Use more measurable results in your experience section.',
      'Highlight teamwork and leadership roles.',
      'Align your experience with the job requirements.'
    ]
  };
  finalRecommendation: string = 'Your resume is well-structured and matches the job requirements. Consider adding more quantifiable achievements and a summary section for even better results.';

  ngOnInit(){
    const storedData = localStorage.getItem('lastScan');
    if (storedData) {
      const data = JSON.parse(storedData);
      this.resumeScore = data.resume_score || 0;
      this.skillsMatch = data.skill_match_score || 0;
      // this.aiAtsScore = 85; // Static for now (adjust when actual readability metric added)
      // this.jobTitle = data.job_title || 'Not Provided';
      // this.jobDescription = data.job_description || '';
      this.resumeName = data.resumeName
      this.date = new Date(data.date).toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    }

  }

  printReport() {
    window.print();
  }
}
