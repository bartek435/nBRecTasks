import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Car, Service } from '../car'
import { CarService } from '../car.service';

@Component({
  selector: 'app-car-details',
  templateUrl: './car-details.component.html',
  styleUrls: ['./car-details.component.css']
})
export class CarDetailsComponent implements OnInit {
  @Input() car?: Car;
  @Output("updateCars") updateCars: EventEmitter<any> = new EventEmitter();
  constructor(private carService: CarService) { }

  addNewService(car:Car){
    let service: Service = {
      name: '',
      parts: '',
      cost: 0
    }
    car.services.push(service)
  };
  updateCar(){
    this.updateCars.emit();
  }
  deleteService(car:Car, index:number){
    car.services.splice(index,1)
    this.updateCars.emit()
  }
  ngOnInit(): void {
  }

}
