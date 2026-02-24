import { Routes } from '@angular/router';
import {HomeComponent} from '../pages/home/home.component';
import {CameraComponent} from '../pages/camera/camera.component';
import {KitchenTimerComponent} from '../pages/kitchen-timer/kitchen-timer.component';
import {BedroomRgbLedComponent} from '../pages/bedroom-rgb-led/bedroom-rgb-led.component';
import {AlarmComponent} from '../pages/alarm/alarm.component';
import {AlarmGuard} from '../guards/alarm.guard';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
  {
    canActivate: [AlarmGuard],
    path: 'home',
    component: HomeComponent
  },
  {
    canActivate: [AlarmGuard],
    path: 'camera',
    component: CameraComponent
  },
  {
    canActivate: [AlarmGuard],
    path: 'kitchen-timer',
    component: KitchenTimerComponent
  },
  {
    canActivate: [AlarmGuard],
    path: 'bedroom-rgb-led',
    component: BedroomRgbLedComponent
  },
  {
    path: 'alarm',
    component: AlarmComponent
  },
  {
    path: '**',
    redirectTo: 'home',
  }
];
