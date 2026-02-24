import { Routes } from '@angular/router';
import {HomeComponent} from '../pages/home/home.component';
import {CameraComponent} from '../pages/camera/camera.component';
import {KitchenTimerComponent} from '../pages/kitchen-timer/kitchen-timer.component';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
  {
    path: 'home',
    component: HomeComponent
  },
  {
    path: 'camera',
    component: CameraComponent
  },
  {
    path: 'kitchen-timer',
    component: KitchenTimerComponent
  },
  {
    path: '**',
    redirectTo: 'home',
  }
];
