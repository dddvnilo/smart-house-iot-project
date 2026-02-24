import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-alarm',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './alarm.component.html',
  styleUrl: './alarm.component.css'
})
export class AlarmComponent {

  pin: string = '';
  errorMessage: string = '';

  constructor(
    private http: HttpClient,
    private router: Router
  ) {}

  submitPin() {
    this.http.post<any>('http://localhost:5000/enter_pin', {
      pin: this.pin
    }).subscribe({
      next: (res) => {
        if (res.status === 'success') {
          this.errorMessage = '';
          this.router.navigate(['/']); // go back to app
        } else {
          this.errorMessage = 'Incorrect PIN';
        }
      },
      error: () => {
        this.errorMessage = 'Server error';
      }
    });
  }
}
