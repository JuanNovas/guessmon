import random
import requests
    

def get_generation(pokemon_guessed : str) -> int:
    """Checks the pokemon generation with the request library and the poke api 
    from the name of the pokemon

    Args:
        pokemon_gussed (str): Pokemons name

    Returns:
        int: Generation of the pokemon given as an argument
    """
    
    pokemon = pokemon_guessed.lower()[:(pokemon_guessed.lower().find("-"))]
    
    url =f"https://pokeapi.co/api/v2/pokemon-species/{pokemon}"
    re  = requests.get(url)
    
    if re.status_code == 200:
    
        data = re.json()
        
        numero_generacion = data['generation']['url'].split('/')[-2] 
        return int(numero_generacion)
    
    else:
        pokemon = pokemon_guessed.lower()
    
        url =f"https://pokeapi.co/api/v2/pokemon-species/{pokemon}"
        re  = requests.get(url)
        
        if re.status_code == 200:
        
            data = re.json()
            
            numero_generacion = data['generation']['url'].split('/')[-2] 
            return int(numero_generacion)
        
        else:
            return False

  
    
    
def check_accuracy(pokemon_guessed : dict, answer : dict) -> tuple:
    """Compare the user guess with the actual answer and returns the 
    background that will be displayed in each div in the website

    Args:
        pomkemon_guessed (dict): Pokemon the user guess in the form of a dict
        answer (dict): Answer in the form of a dict with all the values

    Returns:
        tuple: Tuple of the URL that will be displayed in the back of every container
        in the following order:
            - Pokemon
            - Generation
            - HP
            - Attack
            - Defense
            - Sp. atack
            - Sp. defense 
            - Speed
            - Types
    """
    
    green = "#27CB58"
    yellow = "#FFFF00"
    red = "#FF0000"
    green_image = "../static/green_background.png"
    arrow_up = "../static/arrow_up.png"
    arrow_down = "../static/arrow_down.png"
    
    
    # Cheking the pokemon, if it is right returns all green
    if pokemon_guessed["name"] == answer["name"]:
        return green, green_image, green_image, green_image, green_image, green_image, green_image, green_image, green
    else:
        sprite_b = red
    
    # Checking the generation
    if pokemon_guessed["generation"] == answer["generation"]:
        generation_b = green_image
    elif pokemon_guessed["generation"] > answer["generation"]:
        generation_b = arrow_down
    else:
        generation_b = arrow_up
        
    # Cheking the HP
    if pokemon_guessed["hp"] == answer["hp"]:
        hp_b = green_image
    elif pokemon_guessed["hp"] > answer["hp"]:
        hp_b = arrow_down
    else:
        hp_b = arrow_up
        
    # Cheking the attack
    if pokemon_guessed["attack"] == answer["attack"]:
        attack_b = green_image
    elif pokemon_guessed["attack"] > answer["attack"]:
        attack_b = arrow_down
    else:
        attack_b = arrow_up
        
    # Cheking the defense
    if pokemon_guessed["defense"] == answer["defense"]:
        defense_b = green_image
    elif pokemon_guessed["defense"] > answer["defense"]:
        defense_b = arrow_down
    else:
        defense_b = arrow_up
        
    # Cheking the sp. attack
    if pokemon_guessed["sp. attack"] == answer["sp. attack"]:
        sp_attack_b = green_image
    elif pokemon_guessed["sp. attack"] > answer["sp. attack"]:
        sp_attack_b = arrow_down
    else:
        sp_attack_b = arrow_up
        
    # Cheking the sp. defense
    if pokemon_guessed["sp. defense"] == answer["sp. defense"]:
        sp_defense_b = green_image
    elif pokemon_guessed["sp. defense"] > answer["sp. defense"]:
        sp_defense_b = arrow_down
    else:
        sp_defense_b = arrow_up
        
    # Cheking the speed
    if pokemon_guessed["speed"] == answer["speed"]:
        speed_b = green_image
    elif pokemon_guessed["speed"] > answer["speed"]:
        speed_b = arrow_down
    else:
        speed_b = arrow_up
        
    # Cheking the types
    if pokemon_guessed["types"] == answer["types"]:
        types_b  = green
    elif len(pokemon_guessed["types"]) == 2:
        if pokemon_guessed["types"][0] in answer["types"] or pokemon_guessed["types"][1] in answer["types"]:
            types_b = yellow
        else:
            types_b = red
    else:
        if pokemon_guessed["types"][0] in answer["types"]:
            types_b = yellow
        else:
            types_b = red
            
    return sprite_b, generation_b, hp_b, attack_b, defense_b, sp_attack_b, sp_defense_b, speed_b, types_b
    
    
def generate_correct_pokemon() -> dict:
    
    
    """Returns a random pokemon 

    Returns:
        dict: A random pokemon in a dict format with all the information needed
    """
    
    pokemon_data = (requests.get("https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0")).json()
    
    
    # Getting the dex_number of the pokemon
    pokemon_random = random.choice(pokemon_data["results"])
    
    # Guetting the pokemon
    pokemon = (requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_random['name']}")).json()
        
    # Generating the pokemon dict
    pokemon_dict = {
        "name" : pokemon["name"],
        "generation" : get_generation(pokemon["name"]),
        "hp" : pokemon["stats"][0]["base_stat"],
        "attack" : pokemon["stats"][1]["base_stat"],
        "defense" : pokemon["stats"][2]["base_stat"],
        "sp. attack" : pokemon["stats"][3]["base_stat"],
        "sp. defense" : pokemon["stats"][4]["base_stat"],
        "speed" : pokemon["stats"][5]["base_stat"],
        "types" : [tipo["type"]["name"] for tipo in pokemon["types"]]
    }
    
    # Returning the dict
    return pokemon_dict


def update_progress(previous_progress : dict, correct_pokemon : dict, guess : dict) -> dict:
    """Update the progress dictionary by comparing the correct pokemon with the guess and returning 
    an updated progress dictionary

    Args:
        previous_progress (dict): Dictionary containing the ranges and the correct information the user has
        correct_pokemon (dict): Dictionary containing the information of the correct pokemon
        guess (dict): Dictionary containing the information of the pokemon guessed

    Returns:
        dict: Progress dctionary with the ranges and the correct answers the user have
    """
    
    # Defining the background colors
    green = "#27CB58"
    yellow = "#FFFF00"
    red = "#FF0000"
    
    
    
    # Checking the generation
    if type(previous_progress["generation"]) == list:
        if correct_pokemon["generation"] == guess["generation"]:
            previous_progress["generation"] = correct_pokemon["generation"]
            previous_progress["generation b"] = green
            
        elif correct_pokemon["generation"] > guess["generation"] and previous_progress["generation"][0] <= guess["generation"]:
            previous_progress["generation"][0] = guess["generation"] + 1
            if previous_progress["generation"][0] == previous_progress["generation"][1]:
                previous_progress["generation"] = previous_progress["generation"][0]
                previous_progress["generation b"] = green
            elif previous_progress["generation"][1] - previous_progress["generation"][0] <= 2:
                previous_progress["generation b"] = yellow
            else:
                previous_progress["generation b"] = red
                
        elif correct_pokemon["generation"] < guess["generation"] and previous_progress["generation"][1] >= guess["generation"]:
            previous_progress["generation"][1] = guess["generation"] - 1
            if previous_progress["generation"][0] == previous_progress["generation"][1]:
                previous_progress["generation"] = previous_progress["generation"][0]
                previous_progress["generation b"] = green
            elif previous_progress["generation"][1] - previous_progress["generation"][0] <= 2:
                previous_progress["generation b"] = yellow
            else:
                previous_progress["generation b"] = red
            
    
    # Checking the hp
    if type(previous_progress["hp"]) == list:
        if correct_pokemon["hp"] == guess["hp"]:
            previous_progress["hp"] = correct_pokemon["hp"]
            previous_progress["hp b"] = green
            
        elif correct_pokemon["hp"] > guess["hp"] and previous_progress["hp"][0] <= guess["hp"]:
            previous_progress["hp"][0] = guess["hp"] + 1
            if previous_progress["hp"][1] - previous_progress["hp"][0] <= 30:
                previous_progress["hp b"] = yellow
            else:
                previous_progress["hp b"] = red
                
        elif correct_pokemon["hp"] < guess["hp"]  and previous_progress["hp"][1] >= guess["hp"]:
            previous_progress["hp"][1] = guess["hp"] - 1
            if previous_progress["hp"][1] - previous_progress["hp"][0] <= 30:
                previous_progress["hp b"] = yellow
            else:
                previous_progress["hp b"] = red

    
    
    # Checking the attack
    if type(previous_progress["attack"]) == list:
        if correct_pokemon["attack"] == guess["attack"]:
            previous_progress["attack"] = correct_pokemon["attack"]
            previous_progress["attack b"] = green
            
        elif correct_pokemon["attack"] > guess["attack"] and previous_progress["attack"][0] <= guess["attack"]:
            previous_progress["attack"][0] = guess["attack"] + 1
            if previous_progress["attack"][1] - previous_progress["attack"][0] <= 30:
                previous_progress["attack b"] = yellow
            else:
                previous_progress["attack b"] = red
                
        elif correct_pokemon["attack"] < guess["attack"] and previous_progress["attack"][1] >= guess["attack"]:
            previous_progress["attack"][1] = guess["attack"] - 1
            if previous_progress["attack"][1] - previous_progress["attack"][0] <= 30:
                previous_progress["attack b"] = yellow
            else:
                previous_progress["attack b"] = red
    
    
    # Checking the defense
    if type(previous_progress["defense"]) == list:
        if correct_pokemon["defense"] == guess["defense"]:
            previous_progress["defense"] = correct_pokemon["defense"]
            previous_progress["defense b"] = green
            
        elif correct_pokemon["defense"] > guess["defense"] and previous_progress["defense"][0] <= guess["defense"]:
            previous_progress["defense"][0] = guess["defense"] + 1
            if previous_progress["defense"][1] - previous_progress["defense"][0] <= 30:
                previous_progress["defense b"] = yellow
            else:
                previous_progress["defense b"] = red
                
        elif correct_pokemon["defense"] < guess["defense"] and previous_progress["defense"][1] >= guess["defense"]:
            previous_progress["defense"][1] = guess["defense"] - 1
            if previous_progress["defense"][1] - previous_progress["defense"][0] <= 30:
                previous_progress["defense b"] = yellow
            else:
                previous_progress["defense b"] = red
    
    
    # Checking the sp. attack
    if type(previous_progress["sp. attack"]) == list:
        if correct_pokemon["sp. attack"] == guess["sp. attack"]:
            previous_progress["sp. attack"] = correct_pokemon["sp. attack"]
            previous_progress["sp. attack b"] = green
            
        elif correct_pokemon["sp. attack"] > guess["sp. attack"] and previous_progress["sp. attack"][0] <= guess["sp. attack"]:
            previous_progress["sp. attack"][0] = guess["sp. attack"] + 1
            if previous_progress["sp. attack"][1] - previous_progress["sp. attack"][0] <= 30:
                previous_progress["sp. attack b"] = yellow
            else:
                previous_progress["sp. attack b"] = red
                
        elif correct_pokemon["sp. attack"] < guess["sp. attack"] and previous_progress["sp. attack"][1] >= guess["sp. attack"]:
            previous_progress["sp. attack"][1] = guess["sp. attack"] - 1
            if previous_progress["sp. attack"][1] - previous_progress["sp. attack"][0] <= 30:
                previous_progress["sp. attack b"] = yellow
            else:
                previous_progress["sp. attack b"] = red
                
    
    # Checking the sp. defense
    if type(previous_progress["sp. defense"]) == list:
        if correct_pokemon["sp. defense"] == guess["sp. defense"]:
            previous_progress["sp. defense"] = correct_pokemon["sp. defense"]
            previous_progress["sp. defense b"] = green
            
        elif correct_pokemon["sp. defense"] > guess["sp. defense"] and previous_progress["sp. defense"][0] <= guess["sp. defense"]:
            previous_progress["sp. defense"][0] = guess["sp. defense"] + 1
            if previous_progress["sp. defense"][1] - previous_progress["sp. defense"][0] <= 30:
                previous_progress["sp. defense b"] = yellow
            else:
                previous_progress["sp. defense b"] = red
                
        elif correct_pokemon["sp. defense"] < guess["sp. defense"] and previous_progress["sp. defense"][1] >= guess["sp. defense"]:
            previous_progress["sp. defense"][1] = guess["sp. defense"] - 1
            if previous_progress["sp. defense"][1] - previous_progress["sp. defense"][0] <= 30:
                previous_progress["sp. defense b"] = yellow
            else:
                previous_progress["sp. defense b"] = red
                
                
    # Checking the speed
    if type(previous_progress["speed"]) == list:
        if correct_pokemon["speed"] == guess["speed"]:
            previous_progress["speed"] = correct_pokemon["speed"]
            previous_progress["speed b"] = green
            
        elif correct_pokemon["speed"] > guess["speed"] and previous_progress["speed"][0] <= guess["speed"]:
            previous_progress["speed"][0] = guess["speed"] + 1
            if previous_progress["speed"][1] - previous_progress["speed"][0] <= 30:
                previous_progress["speed b"] = yellow
            else:
                previous_progress["speed b"] = red
                
        elif correct_pokemon["speed"] < guess["speed"] and previous_progress["speed"][1] >= guess["speed"]:
            previous_progress["speed"][1] = guess["speed"] - 1
            if previous_progress["speed"][1] - previous_progress["speed"][0] <= 30:
                previous_progress["speed b"] = yellow
            else:
                previous_progress["speed b"] = red
                
                
    # Checking the types
    if previous_progress["types"] != correct_pokemon["types"]:
        if guess["types"] == correct_pokemon["types"]:
            previous_progress["types"] = guess["types"]
            previous_progress["types b"] = green
        elif len(guess["types"]) == 1 and guess["types"] in correct_pokemon["types"]:
            previous_progress["types"] = guess["types"]
            previous_progress["types b"] = yellow
    
    
    
    return previous_progress


def create_progress_dict() -> dict:
    """Generates a dictionary with the default information needed

    Returns:
        dict: Dict full with the base information
    """ 
    
    progress_default = {
    "generation" : [1,9],
    "generation b" : "#FF0000",
    "hp" : [1,255],
    "hp b" : "#FF0000",
    "attack" : [5,190],
    "attack b" : "#FF0000",
    "defense" : [5,250],
    "defense b" : "#FF0000",
    "sp. attack" : [10,194],
    "sp. attack b" : "#FF0000",
    "sp. defense" : [20,250],
    "sp. defense b" : "#FF0000",
    "speed" : [5,180],
    "speed b" : "#FF0000",
    "types" : [],
    "types b" : "#FF0000"
    }
    
    
    return progress_default



def format(value) -> str:
    """ Depending on the datatype converts the value given into a str with a "-" in the 
    middle or if the value is an int it returns the same number as an str

    Args:
        value (list/int): A list with 2 ints representing a range or a single int

    Returns:
        str: The value given with the format wanted to be displayed
    """
    
    if type(value) == list:
        new_value = []
        for item in value:
            new_value.append(str(item))
        return " - ".join(new_value)
    elif type(value) == int:
        return str(value)
    else:
        return value
    
    
def guessed(guess : str, attemps : list) -> bool:
    """Checks if the pokemon was already guessed

    Args:
        guess (str): A pokemon guess
        attemps (list) : A list with all the past guesses

    Returns:
        bool: True if the pokemon was already guessed
              False if not 
    """
    
    for guessed in attemps:
        if guessed["name"] == guess:
            return True
    
    return False