import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { DevicesTableComponent } from '../../components/devices-table/devices-table.component';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterLink, DevicesTableComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit {

  peopleCount: number = 0;

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.loadPeople();
  }

  loadPeople() {
    this.http.get<any>('http://localhost:5000/people')
      .subscribe({
        next: (res) => {
          this.peopleCount = res.people;
        },
        error: (err) => {
          console.error('Error loading people:', err);
        }
      });
  }
}
