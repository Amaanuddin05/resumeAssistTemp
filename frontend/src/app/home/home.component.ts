import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { NavbarComponent } from '../navbar/navbar.component';

interface ResumeData {
  resumeTitle: string;
  atsScore: number;
  uploadedDate: string;
  thumbnailURL?: string;
}

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterLink, NavbarComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent implements OnInit {
  lastScannedResume: ResumeData | null = null;

  ngOnInit() {
    this.loadLastScannedResume();
    // For demo purposes, set sample data if none exists
    if (!this.lastScannedResume) {
      this.setSampleData();
    }
  }

  private loadLastScannedResume() {
    const resumeData = localStorage.getItem('lastScannedResume');
    if (resumeData) {
      try {
        this.lastScannedResume = JSON.parse(resumeData);
      } catch (error) {
        console.error('Error parsing last scanned resume data:', error);
        this.lastScannedResume = null;
      }
    }
  }

  private setSampleData() {
    const sampleData: ResumeData = {
      resumeTitle: 'Software Engineer Resume.pdf',
      atsScore: 85,
      uploadedDate: '2024-01-15',
      thumbnailURL: undefined
    };
    localStorage.setItem('lastScannedResume', JSON.stringify(sampleData));
    this.lastScannedResume = sampleData;
  }
}
