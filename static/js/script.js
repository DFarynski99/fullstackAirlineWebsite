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
    const arrivalAirport = document.getElementById('arrivalAirport');
    const allAirportsDep = departureAirport.innerHTML; // Save all options to restore them when needed
    const allAirportsArr = arrivalAirport.innerHTML;

    airlineSelection.addEventListener('change', function() {
        const airline = this.value;
        departureAirport.innerHTML = allAirportsDep; // Reset to all airports on every change
        arrivalAirport.innerHTML = allAirportsArr;

        if (airline === 'regionalExpress') {
            const allowedDepAirports = ['', 'depSydney', 'depMelbourneTullamarine', 'depAdelaide', 'depBrisbane', 'depGoldCoast']; // Specify allowed values for Rex
            const allowedArrAirports = ['', 'arrSydney', 'arrMelbourneTullamarine', 'arrAdelaide', 'arrBrisbane', 'arrGoldCoast']
            filterAirportsOrigin(allowedDepAirports);
            filterAirportsArrival(allowedArrAirports);
        }

        else if (airline === 'qantas'){
            const allowedDepAirports = ['', 'depSydney', 'depMelbourneTullamarine', 'depAdelaide', 'depBrisbane', 'depGoldCoast', 'depHobart', 'depPerth']; // Specify allowed values for Rex
            const allowedArrAirports = ['', 'arrSydney', 'arrMelbourneTullamarine', 'arrAdelaide', 'arrBrisbane', 'arrGoldCoast', 'arrHobart', 'arrPerth']
            filterAirportsOrigin(allowedDepAirports);
            filterAirportsArrival(allowedArrAirports);
        }

        else if (airline === 'virgin'){
            const allowedDepAirports = ['', 'depSydney', 'depMelbourneTullamarine', 'depAdelaide', 'depBrisbane', 'depGoldCoast', 'depHobart', 'depPerth']; // Specify allowed values for Rex
            const allowedArrAirports = ['', 'arrSydney', 'arrMelbourneTullamarine', 'arrAdelaide', 'arrBrisbane', 'arrGoldCoast', 'arrHobart', 'arrPerth']
            filterAirportsOrigin(allowedDepAirports);
            filterAirportsArrival(allowedArrAirports);
        }

        else if (airline === 'jetstar'){
            const allowedDepAirports = [
                '',
                'depSydney',
                'depMelbourneTullamarine',
                'depAdelaide',
                'depBrisbane',
                'depCairns',
                'depCanberra',
                'depDarwin',
                'depGoldCoast',
                'depHobart',
                'depLaunceston',
                'depMackay',
                'depMelbourneAvalon',
                'depNewcastle',
                'depPerth',
                'depTownsville'
            ];
            const allowedArrAirports = [
                '',
                'arrSydney',
                'arrMelbourneTullamarine',
                'arrAdelaide',
                'arrBrisbane',
                'arrCairns',
                'arrCanberra',
                'arrDarwin',
                'arrGoldCoast',
                'arrHobart',
                'arrLaunceston',
                'arrMackay',
                'arrMelbourneAvalon',
                'arrNewcastle',
                'arrPerth',
                'arrTownsville'
            ];
            filterAirportsOrigin(allowedDepAirports);
            filterAirportsArrival(allowedArrAirports);
        }

    });

    function filterAirportsOrigin(allowedValues) {
        Array.from(departureAirport.options).forEach(option => {
            if (!allowedValues.includes(option.value)) {
                option.remove(); // Remove options not in the allowed list
            }
        });
    }

    function filterAirportsArrival(allowedValues) {
        Array.from(arrivalAirport.options).forEach(option => {
            if (!allowedValues.includes(option.value)) {
                option.remove(); // Remove options not in the allowed list
            }
        });
    }
});




