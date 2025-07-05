import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { NavbarComponent } from '../navbar/navbar.component';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [CommonModule, FormsModule, NavbarComponent],
  templateUrl: './upload.component.html',
  styleUrl: './upload.component.scss'
})
export class UploadComponent {
  jobTitle: string = '';
  jobDescription: string = '';
  resumeFile: File | null = null;
  isDragOver: boolean = false;

  constructor(
    private router: Router,
    private http: HttpClient
  ) {}

  handleFileInput(event: any) {
    const file = event.target.files[0];
    if (file && this.isValidFileType(file)) {
      this.resumeFile = file;
    } else if (file) {
      alert('Please select a valid file type (PDF, DOC, or DOCX).');
    }
  }

  onDragOver(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    this.isDragOver = true;
  }

  onDragLeave(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    this.isDragOver = false;
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    this.isDragOver = false;

    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      const file = files[0];
      if (this.isValidFileType(file)) {
        this.resumeFile = file;
      } else {
        alert('Please select a valid file type (PDF, DOC, or DOCX).');
      }
    }
  }

  removeFile() {
    this.resumeFile = null;
  }

  isValidFileType(file: File): boolean {
    const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    return validTypes.includes(file.type);
  }

  isFormValid(): boolean {
    return !!(this.jobTitle.trim() && this.jobDescription.trim() && this.resumeFile);
  }

  analyzeResume() {
    if (!this.isFormValid()) {
      alert('Please complete all fields and upload a resume.');
      return;
    }

    const formData = new FormData();
    formData.append('resume', this.resumeFile as Blob);
    formData.append('jobTitle', this.jobTitle);
    formData.append('jobDescription', this.jobDescription);

    this.http.post('http://localhost:5000/analyze', formData).subscribe({
      next: (response: any) => {
        const scanData = {
          ...response,
          job_title: this.jobTitle,
          job_description: this.jobDescription,
          resumeName: this.resumeFile?.name,
          date: new Date().toISOString()
        };

        // Store as last scan
        localStorage.setItem('lastScan', JSON.stringify(scanData));

        // Store in history
        const history = JSON.parse(localStorage.getItem('scanHistory') || '[]');
        history.push(scanData);
        localStorage.setItem('scanHistory', JSON.stringify(history));

        this.router.navigate(['/analyze']);
      },
      error: (error) => {
        console.error('Upload failed:', error);
        alert('Something went wrong. Please try again.');
      },
    });
  }
}
