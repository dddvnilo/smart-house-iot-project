import { Routes } from '@angular/router';
import {HomeComponent} from '../pages/home/home.component';
import {CameraComponent} from '../pages/camera/camera.component';
import {KitchenTimerComponent} from '../pages/kitchen-timer/kitchen-timer.component';
import {BedroomRgbLedComponent} from '../pages/bedroom-rgb-led/bedroom-rgb-led.component';

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
    path: 'bedroom-rgb-led',
    component: BedroomRgbLedComponent
  },
  {
    path: '**',
    redirectTo: 'home',
  }
];
