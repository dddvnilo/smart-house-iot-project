import { Injectable } from '@angular/core';
import { io, Socket } from 'socket.io-client';
import { BehaviorSubject } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AlarmSocketService {

  private socket: Socket;
  private alarmSubject = new BehaviorSubject<boolean>(false);

  alarm$ = this.alarmSubject.asObservable();

  constructor() {
    this.socket = io('http://localhost:5000');

    this.socket.on('alarm', (data: boolean) => {
      console.log('Alarm received:', data);
      this.alarmSubject.next(data);
    });
  }

  disableAlarm(password: string) {
    this.socket.emit('disable_alarm', { password });
  }
}
