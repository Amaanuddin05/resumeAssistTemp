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
  scanHistory: any[] = []

  ngOnInit() {
    const history = localStorage.getItem('scanHistory');
    this.scanHistory = history ? JSON.parse(history).reverse() : [];
  }

  viewScan(scan: any) {
    localStorage.setItem('lastScan', JSON.stringify(scan));
  }
}
