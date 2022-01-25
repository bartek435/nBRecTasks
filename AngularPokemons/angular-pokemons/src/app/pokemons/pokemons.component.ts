import { Component, OnInit } from '@angular/core';
import { PokemonService } from '../pokemon.service';
import { pokemonList, pokemon, pokemon_details } from '../pokemon';
import { isNgTemplate } from '@angular/compiler';

@Component({
  selector: 'app-pokemons',
  templateUrl: './pokemons.component.html',
  styleUrls: ['./pokemons.component.css']
})

export class PokemonsComponent implements OnInit {
  offset = 0;
  pokemons: pokemon[] = [];
  selectedPokemon: pokemon_details = Object({});
  icons: any = {};

  constructor(private pokemonService: PokemonService) {
    this.getPokemons()
    this.icons = {
      "hp": "fas fa-heart",
      "attack": "fas fa-gavel",
      "defense": "fas fa-shield-alt",
      "special-attack": "fas fa-magic",
      "special-defense": "fas fa-shield-virus",
      "speed": "fas fa-running",
      "normal": "fas fa-circle",
      "fighting": "fas fa-fist-raised",
      "flying": "fas fa-wind",
      "poison": "fas fa-skull-crossbones",
      "ground": "fas fa-globe-europe",
      "rock": "fas fa-hard-hat",
      "bug": "fas fa-bug",
      "ghost": "fas fa-ghost",
      "steel": "fas fa-map",
      "fire": "fas fa-fire",
      "water": "fas fa-water",
      "grass": "fas fa-leaf",
      "electric": "fas fa-bolt",
      "psychic": "fas fa-500px",
      "ice": "fas fa-icicles",
      "dragon": "fas fa-dragon",
      "dark": "fas fa-moon",
      "fairy": "fas fa-magic",
      "unknown": "fas fa-question",
      "shadow": "fas fa-adjust",
    };
  }
  
    

  changeOffset(change:number){
    this.offset += change;
    this.getPokemons()
  }
  displayPokemon(index:number){
    let data = this.pokemonService.getPokemonDetails(this.pokemons[index]);
    data.subscribe(
      item => {
        this.selectedPokemon = <pokemon_details>item;
      }
    )
  }
  getPokemons(){
    let data = this.pokemonService.getPokemonList(this.offset,10);
    data.subscribe(
      item => {
        this.pokemons = []
        item.results.forEach(element => {
          let poke:pokemon = <pokemon>element;
          this.pokemons.push(poke)
        });
      }
    )
  }
  ngOnInit(): void {
  }

}
