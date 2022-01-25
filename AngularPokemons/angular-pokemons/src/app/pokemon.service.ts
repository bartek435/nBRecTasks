import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError, of } from 'rxjs';
import { catchError, retry, map } from 'rxjs/operators';
import { pokemon, pokemonList, pokemon_details } from './pokemon';

@Injectable({
  providedIn: 'root'
})
export class PokemonService {
  private pokemonList;

  getPokemonList(offset:number, limit:number): Observable<pokemonList>{
    return this.http.get<pokemonList>(
      `https://pokeapi.co/api/v2/pokemon?limit=${limit}&offset=${offset}`,
      {responseType: 'json', observe: "body"}
    )
  }
  getPokemonDetails(poke:pokemon){
    return this.http.get<pokemon_details>(
      poke.url,
      {responseType: 'json', observe: "body"}
    )
  }
  constructor(private http: HttpClient) { 
    this.pokemonList = 1;
  }
}
