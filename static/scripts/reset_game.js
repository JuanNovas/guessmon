// Waits the html to load before executing
document.addEventListener("DOMContentLoaded", () => {

    // Definding the on click function
    function resetClicked(){
        // redirecting to /reset to reset the game
        window.location.href = "/reset";
    }
    
    // Declaring the variable resetButton refering to the reset button in the html
    var resetButton = document.getElementById("resetButton");
    
    // Creating the event
    resetButton.addEventListener("click", resetClicked);
    
});
