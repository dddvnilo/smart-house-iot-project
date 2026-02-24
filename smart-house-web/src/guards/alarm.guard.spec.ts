import { TestBed } from '@angular/core/testing';
import { CanActivateFn } from '@angular/router';

import { alarmGuard } from './alarm.guard';

describe('alarmGuard', () => {
  const executeGuard: CanActivateFn = (...guardParameters) => 
      TestBed.runInInjectionContext(() => alarmGuard(...guardParameters));

  beforeEach(() => {
    TestBed.configureTestingModule({});
  });

  it('should be created', () => {
    expect(executeGuard).toBeTruthy();
  });
});
