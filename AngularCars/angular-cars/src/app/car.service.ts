import { Injectable } from '@angular/core';
import { Car } from './car';

const defaultCars = `[
  { 
    "name": "BMW",
    "services": [
      {
        "name": "Engine Check",
        "parts": '',
        "cost": 300
      }
    ]
  },
  { 
    "name": "Audi",
    "services": [
      {
        "name": "Change tires",
        "parts": "tires",
        "cost": 200
      }
    ]
  },
  { 
    "name": "Mercedes",
    "services": [
      {
        "name": "Change bulb",
        "parts": "bulb",
        "cost": 10
      }
    ]
  }
]`;
@Injectable({
  providedIn: 'root'
})
export class CarService {
  private carList;

  getCars(){
    return this.carList
  }
  addCar(car:Car){
    this.carList.push(car)
    return this.update()
  }
  private update() {
    localStorage.setItem("cars", JSON.stringify(this.carList));
    return this.getCars();
  }
  private findCarIndex(car:Car) {
    return this.carList.indexOf(car);
  }
  updateCars(cars:Array<Car>) {
    this.carList = cars;
    return this.update();
  }
  destroyCar(car:Car) {
    this.carList.splice(this.findCarIndex(car), 1);
    return this.update();
  }
  constructor() { 
    this.carList = JSON.parse(localStorage.getItem('cars') || defaultCars);
  }
}
