import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { NavbarComponent } from '../navbar/navbar.component';

@Component({
  selector: 'app-analyze',
  standalone: true,
  imports: [CommonModule, RouterLink, NavbarComponent],
  templateUrl: './analyze.component.html',
  styleUrl: './analyze.component.scss'
})
export class AnalyzeComponent {
  atsScore: number = 85;
  keywordMatch: number = 78;
  readability: string = 'Good';
  suggestions = {
    summary: [
      'Add a professional summary at the top of your resume.',
      'Highlight your years of experience and key skills.'
    ],
    experience: [
      'Use more action verbs to describe your achievements.',
      'Quantify your impact with numbers where possible.',
      'Tailor your experience to match the job description.'
    ]
  };
}
