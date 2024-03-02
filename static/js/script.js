document.getElementById('searchButton').addEventListener('click', function() {
    const airline = document.getElementById('airline').value;
    const departureAirport = document.getElementById('departureAirport').value;
    const arrivalAirport = document.getElementById('arrivalAirport').value;
    const departureDate = document.getElementById('departureDate').value;
    const returnDate = document.getElementById('returnDate').value;

    // Log values to console (for debugging purposes)
    console.log(airline, departureAirport, arrivalAirport, departureDate, returnDate);

    // Example condition: If departure is Sydney and arrival is Melbourne, change h1 color to red
    if (airline === 'jetstar' && departureAirport === 'depSydney' && arrivalAirport === 'arrMelbourne') {
        document.getElementById('test').style.color = 'hotpink';
    } else if (departureAirport === 'depMelbourne' && arrivalAirport === 'arrSydney') {
        // Another condition: If departure is Melbourne and arrival is Sydney, change h1 color to blue
        document.getElementById('test').style.color = 'blue';
    } else {
        // For any other combination, reset to default color (you can specify what you consider "default")
        document.getElementById('test').style.color = 'black'; // Or whatever your default color is
    }

    // Prevent form submission if you only want to change the color without submitting the form
    // event.preventDefault();
});
