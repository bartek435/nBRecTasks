export interface Car {
  name: string;
  services: Array<Service>;
};
export interface Service {
  name: string;
  parts: string;
  cost: number;
}