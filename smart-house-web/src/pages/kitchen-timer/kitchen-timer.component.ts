import {Component} from '@angular/core';
import {HttpClient, HttpClientModule} from '@angular/common/http';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';

@Component({
  selector: 'app-kitchen-timer',
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './kitchen-timer.component.html',
  styleUrl: './kitchen-timer.component.css'
})
export class KitchenTimerComponent {
  seconds: number = 0;
  statusMessage: string = '';
  readonly MAX_SECONDS = 5999;

  constructor(private http: HttpClient) {}

  submitTimer() {
    // Validacija
    if (!this.seconds || this.seconds <= 0) {
      this.statusMessage = 'Unesite validan broj sekundi.';
      return;
    }

    if (this.seconds > this.MAX_SECONDS) {
      this.statusMessage = `Maksimalno ${this.MAX_SECONDS} sekundi (99:59).`;
      return;
    }

    // POST na server
    const url = 'http://localhost:5000/set_timer';
    this.http.post(url, { seconds: this.seconds }).subscribe({
      next: (res: any) => {
        if (res.status === 'success') {
          this.statusMessage = `Timer postavljen na ${this.seconds} sekundi. Kliknite dugme da startuje.`;
        } else {
          this.statusMessage = `Greška: ${res.message}`;
        }
      },
      error: (err) => {
        this.statusMessage = 'Greška u komunikaciji sa serverom.';
        console.error(err);
      }
    });
  }
}
