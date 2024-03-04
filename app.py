import requests
from flask import Flask,redirect, render_template, request
from functions import *


# Configure application
app = Flask(__name__)

# Declarint the log variable
attemps = []

# Declaring the correct pokemon dictionary
correct_pokemon = dict()

# Creating the progress dictionary
progress = create_progress_dict()


@app.route("/", methods=["GET", "POST"])
def index():
    
    # Using the global variable so the log won't reset
    global attemps
    
    global correct_pokemon
    
    global progress

    
    # Cheking if it is a correct pokemon 
    if not correct_pokemon:
        correct_pokemon = generate_correct_pokemon()
        attemps = []
    
    
    
    # Analizing the user's guess
    if request.method == "POST":
        
        # Try to search the user input into the database, return exception if not
        try:
            # Getting the input
            guess = request.form.get("guess")
            
            # Checking if the user choose the random option
            if guess == "random":  
                while True:             
                    guess = generate_correct_pokemon()["name"]
                    if not guessed(guess, attemps):
                        break
            else:
                   
                # Checking if the pokemon was already guessed
                if guessed(guess, attemps):
                    return render_template("/index.html", attemps=attemps, progress=progress,format=format)
            
            # Getting the pokemon guessed information
            pokemon_data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{guess}")
            pokemon_guessed = pokemon_data.json()
                
            
            # Getting the pokemon guessed generation in numbers
            generation = get_generation(guess)
            if generation == False:
                generation = get_generation(guess)
                if generation == False:
                    print(correct_pokemon["name"])
                    raise("Error geting generation")
            
            # Getting the types in a list format
            types_list = [tipo["type"]["name"] for tipo in pokemon_guessed["types"]]

            # Asigning all the information to a dictionary to pass it to a function
            pokemon_guessed_dict = {
                "name" : pokemon_guessed["name"],
                "generation" : generation,
                "hp" : pokemon_guessed["stats"][0]["base_stat"],
                "attack" : pokemon_guessed["stats"][1]["base_stat"],
                "defense" : pokemon_guessed["stats"][2]["base_stat"],
                "sp. attack" : pokemon_guessed["stats"][3]["base_stat"],
                "sp. defense" : pokemon_guessed["stats"][4]["base_stat"],
                "speed" : pokemon_guessed["stats"][5]["base_stat"],
                "types" : types_list
            }
            
            # Comparing the user guess with the answer and getting wich caracteristics are correct and wich arent in the form of background colors
            sprite_b, generation_b, hp_b, attack_b, defense_b, sp_attack_b, sp_defense_b, speed_b, types_b = check_accuracy(pokemon_guessed_dict, correct_pokemon)
            
            # Deciding if the sprite is shiny or not
            shiny_number = random.randint(1,4096)
            if shiny_number == 1:
                sprite_type = "front_shiny"
            else:
                sprite_type = "front_default"
            
            # Asigning all the information to a dictionary to pass it to the template
            poke_info = {
                "name" : pokemon_guessed["name"],
                "sprite" : pokemon_guessed['sprites'][sprite_type],
                "sprite b" : sprite_b,
                "generation" : generation,
                "generation b" : generation_b,
                "hp" : pokemon_guessed_dict["hp"],
                "hp b" : hp_b,
                "attack" : pokemon_guessed_dict["attack"],
                "attack b" : attack_b,
                "defense" : pokemon_guessed_dict["defense"],
                "defense b" : defense_b,
                "sp. attack" : pokemon_guessed_dict["sp. attack"],
                "sp. attack b" : sp_attack_b,
                "sp. defense" : pokemon_guessed_dict["sp. defense"],
                "sp. defense b" : sp_defense_b,
                "speed" : pokemon_guessed_dict["speed"],
                "speed b" : speed_b,
                "types" : ', '.join(types_list),
                "types b" : types_b
            }
            
            
            # Adding the attempt to the log, so the informating will be correclty display
            attemps.insert(0,poke_info)
            
            if correct_pokemon["name"] == poke_info["name"]:
                return render_template("/correct.html", attemp=attemps[0], attemps_made=len(attemps))
            
            # Updating the progress dictionary
            progress = update_progress(progress, correct_pokemon, pokemon_guessed_dict)
            
            # Rendering the template
            return render_template("/index.html", attemps=attemps, progress=progress, format=format)
        
        except:
            # If the pokemon wasn't found, rendering the template with the attemps made beafore
            print(f"#Error loading pokemon {request.form.get('guess')}")
            return render_template("/index.html", attemps=attemps, progress=progress, format=format)
            
            


        
    
    else:
        # Rendering the template
        return render_template("/index.html", attemps=attemps, progress=progress, format=format)
    
  
  
   
@app.route("/reset")
def reset():
    # Using the global variable so the variables are correctly reset
    global attemps
    
    global correct_pokemon
    
    global progress
    
    # Reseting the variables
    
    attemps = []
    correct_pokemon = dict()
    progress = create_progress_dict()
    
    return redirect("/")

    
if __name__ == "__main__":
    app.run(debug=True)