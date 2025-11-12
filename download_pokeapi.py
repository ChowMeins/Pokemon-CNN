import json
import requests
import os

version_shorthands = {
    "diamond-pearl": "dp",
    "platinum": "pt",
    "heartgold-soulsilver": "hgss"
}
variation_shorthands = {
    "front_default": "d",
    "front_female": "f",
    "front_shiny": "s",
    "front_shiny_female": "sf"
}
sprite_variations = ['front_default', 'front_female', 'front_shiny', 'front_shiny_female']

dataset_path = "./PokemonGen4/dataset/sprites"
request_url = "https://pokeapi.co/api/v2/pokemon/?offset=0&limit=493"
response = requests.get(request_url)
data = response.json()
json_data = data['results']

for i in range(len(json_data)):
    pokemon_name = json_data[i]["name"]
    pokemon_directory = f"{dataset_path}/{i + 1}"

    pokemon_response = requests.get(json_data[i]["url"])
    pokemon_data = pokemon_response.json()
    pokemon_forms = (pokemon_data["forms"])
    # Handle multiple forms
    if len(pokemon_forms) > 1:
        print(f"{pokemon_forms[0]['name']} has multiple forms.")
        for form in pokemon_forms:
            form_response = requests.get(form["url"])
            form_data = form_response.json()
            form_name, sprite_urls = form_data["form_name"], form_data["sprites"]
            if form_name == '': # If default form, skip current iteration, handled in next block
                continue
            else:
                output_path = f"{pokemon_directory}-{form_name}"
                for variation in sprite_variations:
                    sprite_url = sprite_urls[variation]
                    if sprite_url is not None:
                        if not os.path.exists(output_path):
                            os.makedirs(output_path)
                        with open(f"{output_path}/{variation}.png", "wb") as f:
                            image_response = requests.get(sprite_url)            
                            f.write(image_response.content)
    else:
        print(f"{pokemon_forms[0]['name']} has 1 form.")
    
    # Handle default form / Pokemon with only 1 form
    version_data = pokemon_data["sprites"]["versions"]["generation-iv"] # For each version that exists in Gen 4 (DP, Pt, HGSS)
    os.makedirs(pokemon_directory, exist_ok=True)
    for key in version_data.keys():
        for variation in sprite_variations:
            sprite_url = version_data[key][variation]
            if sprite_url is not None:
                 with open(f"{pokemon_directory}/{version_shorthands[key]}-{variation_shorthands[variation]}.png", "wb") as f:
                     image_response = requests.get(sprite_url)            
                     f.write(image_response.content)
