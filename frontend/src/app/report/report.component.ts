import { Component } from '@angular/core';
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
export class ReportComponent {
  atsScore: number = 87;
  keywordMatch: number = 76;
  readability: string = 'Good';
  jobTitle: string = 'Frontend Developer';
  date: string = new Date().toLocaleDateString();
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

  printReport() {
    window.print();
  }
}
