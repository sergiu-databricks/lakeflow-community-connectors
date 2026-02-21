import requests
from typing import Dict, List, Iterator
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    StringType,
    BooleanType,
    ArrayType,
)
from databricks.labs.community_connector.interface import LakeflowConnect


class PokeAPILakeflowConnect(LakeflowConnect):
    """
    LakeflowConnect implementation for PokeAPI.

    PokeAPI is a public API that provides comprehensive Pokemon data.
    No authentication is required.
    """

    def __init__(self, options: Dict[str, str]) -> None:
        """
        Initialize PokeAPI connector.

        Args:
            options: Dictionary of connection parameters (none required for PokeAPI)
        """
        self.base_url = "https://pokeapi.co/api/v2"
        self.max_pokemon_id = 1025  # Total Pokemon available in the API
        self.batch_size = 50  # Number of Pokemon to fetch per batch

    def list_tables(self) -> List[str]:
        """Return the list of available PokeAPI tables."""
        return ["pokemon"]

    def get_table_schema(
        self, table_name: str, table_options: Dict[str, str]
    ) -> StructType:
        """
        Fetch the schema of a table.

        Args:
            table_name: The name of the table
            table_options: Additional options for the table

        Returns:
            StructType representing the schema
        """
        if table_name != "pokemon":
            raise ValueError(f"Unknown table: {table_name}")

        # Define nested structures
        named_api_resource_schema = StructType(
            [
                StructField("name", StringType(), True),
                StructField("url", StringType(), True),
            ]
        )

        pokemon_ability_schema = StructType(
            [
                StructField("is_hidden", BooleanType(), True),
                StructField("slot", IntegerType(), True),
                StructField("ability", named_api_resource_schema, True),
            ]
        )

        pokemon_type_schema = StructType(
            [
                StructField("slot", IntegerType(), True),
                StructField("type", named_api_resource_schema, True),
            ]
        )

        pokemon_stat_schema = StructType(
            [
                StructField("stat", named_api_resource_schema, True),
                StructField("effort", IntegerType(), True),
                StructField("base_stat", IntegerType(), True),
            ]
        )

        pokemon_move_version_schema = StructType(
            [
                StructField("move_learn_method", named_api_resource_schema, True),
                StructField("version_group", named_api_resource_schema, True),
                StructField("level_learned_at", IntegerType(), True),
            ]
        )

        pokemon_move_schema = StructType(
            [
                StructField("move", named_api_resource_schema, True),
                StructField(
                    "version_group_details",
                    ArrayType(pokemon_move_version_schema),
                    True,
                ),
            ]
        )

        pokemon_held_item_version_schema = StructType(
            [
                StructField("version", named_api_resource_schema, True),
                StructField("rarity", IntegerType(), True),
            ]
        )

        pokemon_held_item_schema = StructType(
            [
                StructField("item", named_api_resource_schema, True),
                StructField(
                    "version_details",
                    ArrayType(pokemon_held_item_version_schema),
                    True,
                ),
            ]
        )

        version_game_index_schema = StructType(
            [
                StructField("game_index", IntegerType(), True),
                StructField("version", named_api_resource_schema, True),
            ]
        )

        pokemon_sprites_schema = StructType(
            [
                StructField("front_default", StringType(), True),
                StructField("front_shiny", StringType(), True),
                StructField("front_female", StringType(), True),
                StructField("front_shiny_female", StringType(), True),
                StructField("back_default", StringType(), True),
                StructField("back_shiny", StringType(), True),
                StructField("back_female", StringType(), True),
                StructField("back_shiny_female", StringType(), True),
            ]
        )

        pokemon_cries_schema = StructType(
            [
                StructField("latest", StringType(), True),
                StructField("legacy", StringType(), True),
            ]
        )

        # Main Pokemon schema
        schema = StructType(
            [
                StructField("id", IntegerType(), False),
                StructField("name", StringType(), True),
                StructField("base_experience", IntegerType(), True),
                StructField("height", IntegerType(), True),
                StructField("is_default", BooleanType(), True),
                StructField("order", IntegerType(), True),
                StructField("weight", IntegerType(), True),
                StructField("abilities", ArrayType(pokemon_ability_schema), True),
                StructField("forms", ArrayType(named_api_resource_schema), True),
                StructField("game_indices", ArrayType(version_game_index_schema), True),
                StructField("held_items", ArrayType(pokemon_held_item_schema), True),
                StructField("location_area_encounters", StringType(), True),
                StructField("moves", ArrayType(pokemon_move_schema), True),
                StructField("sprites", pokemon_sprites_schema, True),
                StructField("cries", pokemon_cries_schema, True),
                StructField("species", named_api_resource_schema, True),
                StructField("stats", ArrayType(pokemon_stat_schema), True),
                StructField("types", ArrayType(pokemon_type_schema), True),
            ]
        )

        return schema

    def read_table_metadata(
        self, table_name: str, table_options: Dict[str, str]
    ) -> Dict[str, str]:
        """
        Fetch the metadata of a table.

        Args:
            table_name: The name of the table
            table_options: Additional options for the table

        Returns:
            Dictionary containing metadata
        """
        if table_name != "pokemon":
            raise ValueError(f"Unknown table: {table_name}")

        return {
            "primary_keys": ["id"],
            "ingestion_type": "snapshot",
        }

    def read_table(
        self, table_name: str, start_offset: dict, table_options: Dict[str, str]
    ) -> (Iterator[dict], dict):
        """
        Read data from a table and return an iterator of records along with the next offset.

        Args:
            table_name: The name of the table
            start_offset: The offset to start reading from
            table_options: Additional options for the table

        Returns:
            Tuple of (iterator of records, next offset)
        """
        if table_name != "pokemon":
            raise ValueError(f"Unknown table: {table_name}")

        # Determine starting ID
        current_id = start_offset.get("last_id", 0) if start_offset else 0
        current_id += 1  # Start from the next ID

        # If we've already processed all Pokemon, return empty iterator with same offset
        if current_id > self.max_pokemon_id:
            return iter([]), start_offset

        # Calculate end ID for this batch
        end_id = min(current_id + self.batch_size - 1, self.max_pokemon_id)

        # Fetch Pokemon data
        data_iterator = self._fetch_pokemon_batch(current_id, end_id)

        # Return iterator and next offset
        next_offset = {"last_id": end_id}

        return data_iterator, next_offset

    def _fetch_pokemon_batch(
        self, start_id: int, end_id: int
    ) -> Iterator[dict]:
        """
        Fetch a batch of Pokemon data.

        Args:
            start_id: Starting Pokemon ID
            end_id: Ending Pokemon ID

        Yields:
            Pokemon records as dictionaries
        """
        for pokemon_id in range(start_id, end_id + 1):
            try:
                url = f"{self.base_url}/pokemon/{pokemon_id}/"
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                pokemon_data = response.json()

                # Yield the Pokemon data
                yield pokemon_data

            except requests.exceptions.RequestException as e:
                # Log error but continue with next Pokemon
                print(f"Error fetching Pokemon ID {pokemon_id}: {e}")
                continue
