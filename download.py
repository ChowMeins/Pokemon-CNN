import requests
import os

dataset_path = "./PokemonGen4/dataset/"
request_url = "https://pokeapi.co/api/v2/pokemon/?offset=0&limit=493"
response = requests.get(request_url)
data = response.json()
version_shorthands = {
    "diamond-pearl": "dp",
    "platinum": "pt",
    "heartgold-soulsilver": "hgss"
}
print(data)
'''
for pokemon in data['results']:
    pokemon_name = pokemon["name"]
    pokemon_directory = dataset_path + "/" + pokemon["name"]
    os.makedirs(pokemon_directory, exist_ok=True)
    os.makedirs(pokemon_directory + "_shiny", exist_ok=True)

    pokemon_response = requests.get(pokemon["url"])
    pokemon_data = pokemon_response.json()
    for version in pokemon_data["sprites"]["versions"]["generation-iv"]: # For each version that exists in Gen 4 (DP, Pt, HGSS)
        # Store URLs of each shiny sprite
        version_shorthands = {
            "diamond-pearl": "dp",
            "platinum": "pt",
            "heartgold-soulsilver": "hgss"
        }
        version_shorthand = version_shorthands[version]
        keys = ["front_default", "front_female", "front_shiny", "front_shiny_female"]
        sprite_urls = []
        for key in keys:
            sprite_urls.append(pokemon_data["sprites"]["versions"]["generation-iv"][version][key])   
        # Download each sprite if it exists
        for i, sprite in enumerate(sprite_urls):
            if sprite is not None:
                image_response = requests.get(sprite)
                image_name = sprite.split("/")[-1].strip('.png')
                if i > 1: # Shiny sprites
                    with open(f"{pokemon_directory}_shiny/{image_name}_{version_shorthand}_{keys[i]}.png", "wb") as f:
                        f.write(image_response.content)
                else:
                    with open(f"{pokemon_directory}/{image_name}_{version_shorthand}_{keys[i]}.png", "wb") as f:
                        f.write(image_response.content)
'''