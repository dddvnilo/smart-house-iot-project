import {Component, OnInit} from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

interface DeviceMeasurement {
  measurement: string;
  latestValue: string;
}

interface Device {
  code: string;
  name: string;
  measurements: DeviceMeasurement[];
}

interface PiGroup {
  name: string;
  color: string;
  devices: Device[];
}

@Component({
  selector: 'app-devices-table',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './devices-table.component.html',
  styleUrls: ['./devices-table.component.css']
})
export class DevicesTableComponent implements OnInit {

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loadLatest();
    setInterval(() => this.loadLatest(), 10000);
  }

  loadLatest() {
    this.http.get<any>('http://localhost:5000/api/latest')
      .subscribe(data => {
        this.applyServerData(data);
      });
  }

  applyServerData(data: any) {
    console.log(data);
    Object.keys(data).forEach(piName => {

      const piGroup = this.piGroups.find(g => g.name === piName);
      if (!piGroup) return;

      const devicesFromServer = data[piName];

      Object.keys(devicesFromServer).forEach(bucketName => {
        if (bucketName === 'dht' && piName === 'PI3') {

          const dhtData = devicesFromServer[bucketName];
          console.log(dhtData)
          Object.keys(dhtData).forEach(fullKey => {

            const value = dhtData[fullKey];

            // Example fullKey:
            // "Bedroom DHT_Temperature"
            // "Master Bedroom DHT_Humidity"

            const [deviceNamePart, measurementPart] = fullKey.split('_');

            const device = piGroup.devices.find(d =>
              d.name.toLowerCase() === deviceNamePart.toLowerCase()
            );

            if (!device) return;

            const measurement = device.measurements.find(m =>
              m.measurement.toLowerCase() === measurementPart.toLowerCase()
            );

            if (!measurement) return;

            if (measurementPart.toLowerCase() === 'temperature') {
              measurement.latestValue = value + ' °C';
            }
            else if (measurementPart.toLowerCase() === 'humidity') {
              measurement.latestValue = value + ' %';
            }
            else {
              measurement.latestValue = value.toString();
            }

          });

          return; // VERY IMPORTANT: skip normal logic
        }

        const deviceName = this.bucketToDeviceName[bucketName];
        console.log(deviceName);

        if (!deviceName) return;
        // ===== SPECIAL CASE: PI3 DHT GROUPED BUCKET =====


        const device = piGroup.devices.find(d => d.name === deviceName);
        if (!device) return;

        const measurements = devicesFromServer[bucketName];

        Object.keys(measurements).forEach(serverMeasurementName => {

          const mappedName =
            this.measurementMap[serverMeasurementName] ??
            serverMeasurementName.toLowerCase();

          const measurement = device.measurements
            .find(m => m.measurement.toLowerCase() === mappedName.toLowerCase());

          if (!measurement) return;

          let value = measurements[serverMeasurementName];

          // format booleans nicely
          if (typeof value === 'boolean') {
            measurement.latestValue = value ? 'TRUE' : 'FALSE';
          }
          else if (typeof value === 'number') {

            if (serverMeasurementName.toLowerCase().includes('distance')) {
              measurement.latestValue = value + ' cm';
            }
            else if (serverMeasurementName.toLowerCase().includes('temperature')) {
              measurement.latestValue = value + ' °C';
            }
            else if (serverMeasurementName.toLowerCase().includes('humidity')) {
              measurement.latestValue = value + ' %';
            }
            else {
              measurement.latestValue = value.toString();
            }
          }
          else {
            measurement.latestValue = value;
          }

        });

      });

    });

  }

  getTotalRows(group: PiGroup): number {
    return group.devices
      .map(d => d.measurements.length)
      .reduce((a, b) => a + b, 0);
  }

  private bucketToDeviceName: Record<string, string> = {
  door_sensor: 'Door Sensor (Button)',
  door_light: 'Door Light (LED diode)',
  door_ultrasonic_sensor: 'Door Ultrasonic Sensor',
  door_buzzer: 'Door Buzzer',
  door_motion_sensor: 'Door Motion Sensor',
  door_membrane_switch: 'Door Membrane Switch',
    
  display: 'Kitchen 4 Digit 7 Segment Display Timer',
  kitchen_button: 'Kitchen Button',
  dht: 'Kitchen DHT',
  gyroscope: 'Gyroscope',

  bedroom_dht1: 'Bedroom DHT',
  bedroom_dht2: 'Master Bedroom DHT',
  infrared_receiver: 'Bedroom Infrared',
  rgb_led: 'Bedroom RGB',
  lcd: 'Living room Display',
  living_motion: 'Living Room Motion Sensor'
};
  private measurementMap: Record<string, string> = {
    Distance: 'distance',
    MotionDetected: 'motion',
    IsUnlocked: 'pressed',
    IsLightOn: 'status',
    BuzzerActivated: 'status',
    KeyPressed: 'key',
    ButtonPressed: 'key',
    Temperature: 'temperature',
    Humidity: 'humidity',
    Color: 'color',
    ShownOnLCD: 'value',
    ShownOnDisplay: 'value'
  };
  piGroups: PiGroup[] = [

    // ===================== PI1 =====================
    {
      name: 'PI1',
      color: '#d8b4b4',
      devices: [
        {
          code: 'DS1',
          name: 'Door Sensor (Button)',
          measurements: [
            { measurement: 'pressed', latestValue: '?' }
          ]
        },
        {
          code: 'DL',
          name: 'Door Light (LED diode)',
          measurements: [
            { measurement: 'status', latestValue: '?' }
          ]
        },
        {
          code: 'DUS1',
          name: 'Door Ultrasonic Sensor',
          measurements: [
            { measurement: 'distance', latestValue: '?' }
          ]
        },
        {
          code: 'DB',
          name: 'Door Buzzer',
          measurements: [
            { measurement: 'status', latestValue: '?' }
          ]
        },
        {
          code: 'DPIR1',
          name: 'Door Motion Sensor',
          measurements: [
            { measurement: 'motion', latestValue: '?' }
          ]
        },
        {
          code: 'DMS',
          name: 'Door Membrane Switch',
          measurements: [
            { measurement: 'key', latestValue: '?' }
          ]
        }
      ]
    },

    // ===================== PI2 =====================
    {
      name: 'PI2',
      color: '#b7c7b0',
      devices: [
        {
          code: 'DS2',
          name: 'Door sensor (Button)',
          measurements: [
            { measurement: 'pressed', latestValue: '?' }
          ]
        },
        {
          code: 'DUS2',
          name: 'Door Ultrasonic Sensor',
          measurements: [
            { measurement: 'distance', latestValue: '?' }
          ]
        },
        {
          code: 'DPIR2',
          name: 'Door Motion Sensor',
          measurements: [
            { measurement: 'motion', latestValue: '?' }
          ]
        },
        {
          code: '4SD',
          name: 'Kitchen 4 Digit 7 Segment Display Timer',
          measurements: [
            { measurement: 'value', latestValue: '?' }
          ]
        },
        {
          code: 'BTN',
          name: 'Kitchen Button',
          measurements: [
            { measurement: 'pressed', latestValue: '?' }
          ]
        },
        {
          code: 'DHT3',
          name: 'Kitchen DHT',
          measurements: [
            { measurement: 'temperature', latestValue: '?' },
            { measurement: 'humidity', latestValue: '?' }
          ]
        },
        {
          code: 'GSG',
          name: 'Gyroscope',
          measurements: [
            { measurement: 'accelerometer', latestValue: '?' },
            { measurement: 'gyroscope', latestValue: '?' },
          ]
        }
      ]
    },

    // ===================== PI3 =====================
    {
      name: 'PI3',
      color: '#b7c7d9',
      devices: [
        {
          code: 'DHT1',
          name: 'Bedroom DHT',
          measurements: [
            { measurement: 'temperature', latestValue: '?' },
            { measurement: 'humidity', latestValue: '?' }
          ]
        },
        {
          code: 'DHT2',
          name: 'Master Bedroom DHT',
          measurements: [
            { measurement: 'temperature', latestValue: '?' },
            { measurement: 'humidity', latestValue: '?' }
          ]
        },
        {
          code: 'IR',
          name: 'Bedroom Infrared',
          measurements: [
            { measurement: 'key', latestValue: '?' }
          ]
        },
        {
          code: 'BRGB',
          name: 'Bedroom RGB',
          measurements: [
            { measurement: 'color', latestValue: '?' },
          ]
        },
        {
          code: 'LCD',
          name: 'Living room Display',
          measurements: [
            { measurement: 'value', latestValue: '?' }
          ]
        },
        {
          code: 'DPIR3',
          name: 'Door Motion Sensor',
          measurements: [
            { measurement: 'motion', latestValue: '?' }
          ]
        }
      ]
    }
  ];
}
