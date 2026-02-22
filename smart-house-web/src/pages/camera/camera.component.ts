import { Component } from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';
import {RouterLink} from '@angular/router';

@Component({
  selector: 'app-camera',
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './camera.component.html',
  styleUrl: './camera.component.css'
})
export class CameraComponent {
  cameraUrl: string = "http://localhost:5000/camera_stream";

  updateUrl(newUrl: string) {
    this.cameraUrl = newUrl;
  }
}
