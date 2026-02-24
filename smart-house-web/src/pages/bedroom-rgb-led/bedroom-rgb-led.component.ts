import { Component } from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Component({
  selector: 'app-bedroom-rgb-led',
  imports: [],
  templateUrl: './bedroom-rgb-led.component.html',
  styleUrl: './bedroom-rgb-led.component.css'
})
export class BedroomRgbLedComponent {
  constructor(private http: HttpClient) {}

  send(button: string) {
    const payload = { rgb_led_input: button };

    this.http.post('http://localhost:5000/rgb_led_input', payload)
      .subscribe({
        next: () => console.log("Poslato:", button),
        error: err => console.error("Greska:", err)
      });
  }
}
