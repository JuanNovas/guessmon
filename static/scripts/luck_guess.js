// Waits the html to load before executing
document.addEventListener("DOMContentLoaded", () => {

    // Declaring the on click function
    function luckGuess(){
        // Creating a temporary form to submit the information, declaring the method and the action
        var form = document.createElement("form");
        form.method = "post";
        form.action = "/";

        // Creating a temporary input to complete with the "random" value to pass to the back, and declaring the type (Hidden so it wouldn't show), name (So the back script wouldn't need to change) and value.
        var input = document.createElement("input");
        input.type = "hidden";
        input.name = "guess";
        input.value = "random";
        // Including the input into the form
        form.appendChild(input);

        // Including the form to the document
        document.body.appendChild(form);

        // Submiting the form
        form.submit();
    }
    
    // Declaring the variable who refers to the lucky Butoon
    var luckyButton = document.getElementById("luckyButton");
    
    // Creating the event
    luckyButton.addEventListener("click", luckGuess);
    
});