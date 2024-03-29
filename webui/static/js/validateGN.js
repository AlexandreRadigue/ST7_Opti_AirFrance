window.onload = function () {
    var form = document.querySelector("form");
    var groupNumberInput = document.getElementById("group-number");
    var errorMessage = document.getElementById("error-message");

    form.addEventListener("submit", function (event) {
        var groupNumber = parseInt(groupNumberInput.value);
        if (isNaN(groupNumber) || groupNumber % 1 !== 0 || groupNumber == 0 || groupNumber > 111) {
            errorMessage.style.display = "inline";
            errorMessage.textContent = "Please enter a valid group number";
            event.preventDefault();
        } else {
            errorMessage.style.display = "none";
        }
    });
    const Message = JSON.parse(message)
    if (Message === "Group number already registered") {
        errorMessage.style.display = "inline";
        errorMessage.textContent = Message;
    }
};