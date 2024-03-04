// Waits the html to load before executing
document.addEventListener("DOMContentLoaded", () => {

    // Declaring constants who referrs to elements in the documents and the max suggestions allowed
    const guess = document.getElementById("guess");
    const suggestionsList = document.getElementById("suggestions");
    const MAX_SUGGESTIONS = 5;

    // Hidding the list
    suggestionsList.style.display = "none";

    // Creating the event
    guess.addEventListener("input", async (event) => {
        // Formating and declaring a constant for the users write in the input
        const searchTerm = event.target.value.toLowerCase().trim();
        
        // Reseting the suggestions
        suggestionsList.innerHTML = "";
        selectedSuggestionIndex = -1;

        // Only show suggestions if the caracters wrote are 2 or more
        if (searchTerm.length >= 2) { 
            try {
                // Getting the informacion from the api (pokeapi)
                const response = await fetch("https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0");
                const data = await response.json();
                // Adding the matching ones into a constant
                const matchingPokemon = data.results.filter(pokemon => pokemon.name.includes(searchTerm));

                // If there are coincidences shows the suggestions bar
                if (matchingPokemon.length > 0) { 
                    // Shows the bar
                    suggestionsList.style.display = "block";
                    // Shows the list of coincident pokemons with a max previousle delcare
                    matchingPokemon.slice(0,MAX_SUGGESTIONS).forEach(pokemon => {
                        // Creating and adding the list items to the document
                        const listItem = document.createElement("li");
                        listItem.textContent = pokemon.name;
                        suggestionsList.appendChild(listItem);

                        // Creating the event of clicking in a list item
                        listItem.addEventListener("click", () => {
                            // Getting the value of the pokemon clicked and clearing the list
                            guess.value = pokemon.name;
                            suggestionsList.innerHTML = "";
                            // Submiting the form with the value choosen
                            guessForm.submit();
                        });

                    });

                // If not coincidences hides the bar
                } else {
                    suggestionsList.style.display = "none"; 
                }
            // If something went wrong
            } catch (error) {
                console.error("Error searching pokemon:", error);
            }
        }
    });

});

