import { Injectable } from '@angular/core';
import {AlarmSocketService} from './alarm-socket.service';
import {Router} from '@angular/router';

@Injectable({ providedIn: 'root' })
export class AlarmService {

  alarmActive = false;
  isAlarmActive(): boolean {
    return this.alarmActive;
  }
  constructor(private socketService: AlarmSocketService, private router: Router) {
    this.socketService.alarm$.subscribe(state => {
      const wasActive = this.alarmActive;
      this.alarmActive = state;

      // 🔥 Redirect only when alarm just turned ON
      if (state && !wasActive) {
        console.log('Alarm triggered!');
        // Prevent redirect loop if already on alarm page
        if (!this.router.url.startsWith('/alarm')) {
          this.router.navigate(['/alarm']);
        }
      }
      if (!state && wasActive) {
        console.log('Alarm off!');
        // Prevent redirect loop if already on alarm page
        if (this.router.url.startsWith('/alarm')) {
          this.router.navigate(['/home']);
        }
      }
    });

  }
}
