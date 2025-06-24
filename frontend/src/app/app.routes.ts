import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { UploadComponent } from './upload/upload.component';
import { AnalyzeComponent } from './analyze/analyze.component';
import { ReportComponent } from './report/report.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'upload', component: UploadComponent },
  { path: 'analyze', component: AnalyzeComponent },
  { path: 'report', component: ReportComponent },
  { path: 'results', component: HomeComponent }, // Placeholder - will be replaced with ResultsComponent
  { path: '**', redirectTo: '' }
];
