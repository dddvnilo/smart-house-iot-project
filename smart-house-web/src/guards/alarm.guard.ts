import {CanActivate, CanActivateFn, Router} from '@angular/router';
import {Injectable} from '@angular/core';
import {AlarmService} from '../services/alarm.service';

@Injectable({ providedIn: 'root' })
export class AlarmGuard implements CanActivate {

  constructor(private alarmService: AlarmService,
              private router: Router) {}

  canActivate(): boolean {

    if (this.alarmService.isAlarmActive()) {
      this.router.navigate(['/alarm']);
      return false;
    }

    return true;
  }
}
