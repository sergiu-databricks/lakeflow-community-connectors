# PokeAPI Community Connector

This connector enables ingestion of Pokemon data from the [PokeAPI](https://pokeapi.co/) into Databricks.

## Overview

PokeAPI is a free, public RESTful API that provides comprehensive data about Pokemon, including their abilities, stats, types, moves, and more. This connector allows you to ingest this data into your Databricks lakehouse for analysis.

## Authentication

**No authentication is required** for this connector. PokeAPI is a public API that does not require API keys or credentials.

## Configuration

### Connection Parameters

Since PokeAPI is a public API, no connection parameters are required.

**Example configuration:**
```python
options = {}
```

### Supported Tables

The connector currently supports the following table:

| Table Name | Description | Ingestion Type | Primary Key |
|-----------|-------------|----------------|-------------|
| `pokemon` | Complete Pokemon data including stats, abilities, types, moves, and sprites | Snapshot | `id` |

## Schema

### pokemon

The `pokemon` table contains comprehensive information about each Pokemon:

| Column Name | Type | Description |
|------------|------|-------------|
| `id` | integer | Unique identifier for the Pokemon |
| `name` | string | Name of the Pokemon |
| `base_experience` | integer | Base experience gained for defeating this Pokemon |
| `height` | integer | Height in decimetres |
| `is_default` | boolean | Whether this is the default form |
| `order` | integer | Sort order (almost national order, families grouped) |
| `weight` | integer | Weight in hectograms |
| `abilities` | array | List of abilities (nested structure) |
| `forms` | array | List of forms this Pokemon can take |
| `game_indices` | array | Game indices by version |
| `held_items` | array | Items this Pokemon may hold when encountered |
| `location_area_encounters` | string | Link to location areas where Pokemon can be found |
| `moves` | array | Moves this Pokemon can learn (nested structure) |
| `sprites` | struct | URLs to sprite images |
| `cries` | struct | URLs to Pokemon cries/sounds |
| `species` | struct | Reference to Pokemon species |
| `stats` | array | Base stat values (HP, Attack, Defense, etc.) |
| `types` | array | Pokemon types (e.g., Fire, Water, Grass) |

## Usage Example

### Using Python

```python
from databricks.labs.community_connector.sources.PokeAPI.PokeAPI import PokeAPILakeflowConnect

# Initialize connector (no options needed)
connector = PokeAPILakeflowConnect(options={})

# List available tables
tables = connector.list_tables()
print(tables)  # Output: ['pokemon']

# Get schema
schema = connector.get_table_schema("pokemon", {})

# Read Pokemon data
records, offset = connector.read_table("pokemon", start_offset={}, table_options={})

# Process records
for pokemon in records:
    print(f"Pokemon: {pokemon['name']} (ID: {pokemon['id']})")
```

### Using in Databricks

```python
# Create a Spark DataFrame
df = spark.read \
    .format("lakeflowtConnect") \
    .option("source", "PokeAPI") \
    .option("table", "pokemon") \
    .load()

# Display the data
display(df)

# Example queries
df.select("id", "name", "height", "weight").show()

# Find all fire-type Pokemon
df.filter("array_contains(types.type.name, 'fire')").select("name").show()

# Get Pokemon with highest base stats
df.select("name", "stats.base_stat").orderBy("stats.base_stat", ascending=False).show(10)
```

## Data Notes

1. **Data Coverage**: The connector fetches Pokemon with IDs from 1 to 1025, covering all Pokemon available in the PokeAPI.

2. **Ingestion Type**: The `pokemon` table uses snapshot ingestion, meaning it fetches the complete dataset on each run.

3. **Nested Structures**: The schema preserves nested structures (abilities, moves, stats, etc.) rather than flattening them, allowing for richer analysis.

4. **Rate Limiting**: PokeAPI is a public API. The connector fetches data in batches of 50 Pokemon to be respectful of the API.

5. **Data Freshness**: Pokemon data is relatively static. New Pokemon are only added with new game releases.

## Limitations

- Currently only supports the `pokemon` table. Future enhancements could add support for other PokeAPI endpoints (abilities, moves, types, etc.)
- Uses snapshot ingestion only (no incremental updates)
- No support for filtering specific Pokemon during ingestion

## Troubleshooting

### Connection Issues

If you experience connection issues:
- Verify internet connectivity
- Check if https://pokeapi.co/ is accessible
- The API may occasionally be slow; retry if timeouts occur

### Data Quality

- Some Pokemon may have null values for certain fields (e.g., not all Pokemon have gender differences)
- Sprite URLs may return null for some older Pokemon forms

## Support

For issues specific to this connector, please file an issue in the [community-connectors repository](https://github.com/databricks/lakeflow-community-connectors).

For questions about the PokeAPI itself, visit the [PokeAPI documentation](https://pokeapi.co/docs/v2).

## License

This connector is provided as-is under the project's license. PokeAPI data is provided under the PokeAPI terms of use.
