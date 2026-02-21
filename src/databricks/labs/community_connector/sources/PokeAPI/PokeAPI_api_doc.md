# **PokeAPI API Documentation**

## **Authorization**
- No Authorization required

## **Object List**

The object list is **static** (defined by the connector), representing pokemon and their abbilities, regions they can be captured and more.

**Total Supported Tables**: 1 (1 snapshot)

| Object Name | Description | Primary Endpoint | Ingestion Type |
|------------|-------------|------------------|----------------|
| `pokemon` | Pokemon | `GET /api/v2/pokemon/{id or name}/` | `snapshot` |


**Implementation Status**:
- One table is implemented

**Response Format**:
- JSON with JSON:API format

High-level notes on objects:
- **pokemon**: Data about Pokemon; treated as snapshot (JSON format)


## **Object Schema**

### General notes

- Table schemas are static
- Nested JSON objects are modeled as **nested structures** rather than being fully flattened


### `Pokemon` object (snapshot)

| Column Name | Type | Description |
|------------|------|-------------|
| `id ` | integer | Description |
| `name ` | string | The identifier for this resource. |
| `base_experience ` | integer | The name for this resource. |
| `height ` | integer | The base experience gained for defeating this Pokémon. |
| `is_default ` | boolean | The height of this Pokémon in decimetres. |
| `order ` | integer | Set for exactly one Pokémon used as the default for each species. |
| `weight ` | integer | Order for sorting. Almost national order, except families are grouped together. |
| `abilities ` | list PokemonAbility | The weight of this Pokémon in hectograms. |
| `forms ` | list NamedAPIResource (PokemonForm) | A list of abilities this Pokémon could potentially have. |
| `game_indices ` | list VersionGameIndex | A list of forms this Pokémon can take on. |
| `held_items ` | list PokemonHeldItem | A list of game indices relevent to Pokémon item by generation. |
| `location_area_encounters ` | string | A list of items this Pokémon may be holding when encountered. |
| `moves ` | list PokemonMove | A link to a list of location areas, as well as encounter details pertaining to specific versions. |
| `past_types ` | list PokemonTypePast | A list of moves along with learn methods and level details pertaining to specific version groups. |
| `past_abilities ` | list PokemonAbilityPast | A list of details showing types this pokémon had in previous generations |
| `past_stats ` | list PokemonStatPast | A list of details showing abilities this pokémon had in previous generations |
| `sprites ` | PokemonSprites | A list of details showing stats this pokémon had in previous generations |
| `cries ` | PokemonCries | A set of sprites used to depict this Pokémon in the game. A visual representation of the various sprites can be found at PokeAPI/sprites |
| `species ` | NamedAPIResource (PokemonSpecies) | A set of cries used to depict this Pokémon in the game. A visual representation of the various cries can be found at PokeAPI/cries |
| `stats ` | list PokemonStat | The species this Pokémon belongs to. |
| `types ` | list PokemonType | A list of base stat values for this Pokémon. |



### `PokemonAbility` type

| Column Name | Type | Description |
|------------|------|-------------|
| `is_hidden ` | boolean | Whether or not this is a hidden ability. |
| `slot ` | integer | The slot this ability occupies in this Pokémon species. |
| `ability ` | NamedAPIResource (Ability) | The ability the Pokémon may have. |


### `PokemonType` type

| Column Name | Type | Description |
|------------|------|-------------|
| `slot ` | integer | The order the Pokémon's types are listed in. |
| `type ` | NamedAPIResource (Type) | The type the referenced Pokémon has. |


### `PokemonFormType` type

| Column Name | Type | Description |
|------------|------|-------------|
| `slot ` | integer | The order the Pokémon's types are listed in. |
| `type ` | NamedAPIResource (Type) | The type the referenced Form has. |


### `PokemonTypePast` type

| Column Name | Type | Description |
|------------|------|-------------|
| `generation ` | NamedAPIResource (Generation) | The last generation in which the referenced pokémon had the listed types. |
| `types ` | list PokemonType | The types the referenced pokémon had up to and including the listed generation. |


### `PokemonAbilityPast` type

| Column Name | Type | Description |
|------------|------|-------------|
| `generation ` | NamedAPIResource (Generation) | The last generation in which the referenced pokémon had the listed abilities. |
| `abilities ` | list PokemonAbility | The abilities the referenced pokémon had up to and including the listed generation. If null, the slot was previously empty. |

### `PokemonStatPast` type

| Column Name | Type | Description |
|------------|------|-------------|
| `generation ` | NamedAPIResource (Generation) | The last generation in which the referenced pokémon had the listed stats. |
| `stats ` | list PokemonStat | The stat the Pokémon had up to and including the listed generation. |


### `PokemonHeldItem` type

| Column Name | Type | Description |
|------------|------|-------------|
| `item ` | NamedAPIResource (Item) | The item the referenced Pokémon holds. |
| `version_details ` | list PokemonHeldItemVersion | The details of the different versions in which the item is held. |


### `PokemonHeldItemVersion` type

| Column Name | Type | Description |
|------------|------|-------------|
| `move ` | NamedAPIResource (Move) | The move the Pokémon can learn. |
| `version_group_details ` | list PokemonMoveVersion | The details of the version in which the Pokémon can learn the move. |


### `PokemonMove` type

| Column Name | Type | Description |
|------------|------|-------------|
| `move ` | NamedAPIResource (Move) | Description |
| `version_group_details ` | list PokemonMoveVersion | The move the Pokémon can learn. |


### `PokemonMoveVersion` type

| Column Name | Type | Description |
|------------|------|-------------|
| `move_learn_method ` | NamedAPIResource (MoveLearnMethod) | The method by which the move is learned. |
| `version_group ` | NamedAPIResource (VersionGroup) | The version group in which the move is learned. |
| `level_learned_at ` | integer | The minimum level to learn the move. |
| `order ` | integer | Order by which the pokemon will learn the move. A newly learnt move will replace the move with lowest order. |


### `PokemonStat` type

| Column Name | Type | Description |
|------------|------|-------------|
| `stat ` | NamedAPIResource (Stat) | The stat the Pokémon has. |
| `effort ` | integer | The effort points (EV) the Pokémon has in the stat. |
| `base_stat ` | integer | The base value of the stat. |


### `PokemonSprites` type

| Column Name | Type | Description |
|------------|------|-------------|
| `front_default ` | string | The default depiction of this Pokémon from the front in battle. |
| `front_shiny ` | string | The shiny depiction of this Pokémon from the front in battle. |
| `front_female ` | string | The female depiction of this Pokémon from the front in battle. |
| `front_shiny_female ` | string | The shiny female depiction of this Pokémon from the front in battle. |
| `back_default ` | string | The default depiction of this Pokémon from the back in battle. |
| `back_shiny ` | string | The shiny depiction of this Pokémon from the back in battle. |
| `back_female ` | string | The female depiction of this Pokémon from the back in battle. |
| `back_shiny_female ` | string | The shiny female depiction of this Pokémon from the back in battle. |


### `PokemonCries` type

| Column Name | Type | Description |
|------------|------|-------------|
| `latest ` | string | The latest depiction of this Pokémon's cry. |
| `legacy ` | string | The legacy depiction of this Pokémon's cry. |


**Example request**:

```bash
curl -X GET \
  -H "accept: application/json" \
  "https://pokeapi.co/api/v2/pokemon/35/"
```

**Example response (truncated)**:

```json
[
  {
    "id": 35
    "name": "clefairy"
    "base_experience": 113
    "height": 6
    "is_default": true
    "order": 56
    "weight": 75
  }
]
```

## **Get Object Primary Keys**
- The Pokemon object has a static range of ids from 1 to 1025
