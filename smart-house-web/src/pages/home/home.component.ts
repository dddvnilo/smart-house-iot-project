import { Component } from '@angular/core';
import {RouterLink} from '@angular/router';
import {DevicesTableComponent} from '../../components/devices-table/devices-table.component';

@Component({
  selector: 'app-home',
  imports: [RouterLink, DevicesTableComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {

}
