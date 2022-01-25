export interface pokemon{
    name: string;
    url: string
}
export interface pokemonList{
    count: number;
    next: string;
    previous?: string;
    results: Array<pokemon>

}
export interface pokemon_details{
    name: string;
    types: Array<types>;
    stats: Array<stat>;
    weight: number;
    height: number;
    abilities: Array<ability>;
    base_experience: number;
    is_default: boolean;
}
export interface types{
    type: api;
    slot: number;
}
export interface stat{
    stat: api;
    base_stat: number;
    effort: number;
}
export interface ability{
    ability: api;
    slot: number
}
export interface api{
    name: string;
    url: string;
}