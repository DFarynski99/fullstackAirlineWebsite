document.getElementById('searchButton').addEventListener('click', function() {
    const airline = document.getElementById('airline').value;
    const departureAirport = document.getElementById('departureAirport').value;
    const arrivalAirport = document.getElementById('arrivalAirport').value;
    const departureDate = document.getElementById('departureDate').value;
    const returnDate = document.getElementById('returnDate').value;
});
function goBack() {
    console.log("Back button was clicked");
    window.history.back();
}

document.addEventListener('DOMContentLoaded', function() {
    const airlineSelection = document.getElementById('airline');
    const departureAirport = document.getElementById('departureAirport');
    const allAirports = departureAirport.innerHTML; // Save all options to restore them when needed

    airlineSelection.addEventListener('change', function() {
        const airline = this.value;
        departureAirport.innerHTML = allAirports; // Reset to all airports on every change

        // Example: If airline is Rex, only show specific airports
        if (airline === 'regionalExpress') {
            const allowedAirports = ['depSydney', 'depMelbourneTullamarine']; // Specify allowed values for Rex
            filterAirports(allowedAirports);
        }
        // Add more conditions for other airlines here
        // Example: if (airline === 'jetstar') { ... }
    });

    function filterAirports(allowedValues) {
        Array.from(departureAirport.options).forEach(option => {
            if (!allowedValues.includes(option.value)) {
                option.remove(); // Remove options not in the allowed list
            }
        });
    }
});



