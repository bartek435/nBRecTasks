import { Component, OnInit } from '@angular/core';
import { Car } from '../car';
import { CarService } from '../car.service'

@Component({
  selector: 'app-cars',
  templateUrl: './cars.component.html',
  styleUrls: ['./cars.component.css']
})
export class CarsComponent implements OnInit {
  selectedCar?: Car;
  cars: Car[] = [];

  constructor(private carService: CarService,) {}

  onSelect(car: Car): void {
    this.selectedCar = car;
  }
  addNewCar(){
    let newCar: Car = {
      name: '',
      services: []
    };
    this.carService.addCar(newCar);
  }
  getCars(): void {
    this.cars = this.carService.getCars()
  }
  deleteCar(index:number){
    this.cars.splice(index,1)
    this.updateCars()
  }
  updateCars(){
    this.carService.updateCars(this.cars)
    this.getCars()
  }
  ngOnInit(): void {
    this.getCars()
  }
  
}
