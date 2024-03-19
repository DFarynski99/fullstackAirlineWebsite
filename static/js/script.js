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