var weatherController = (function (){

    let weatherReadings = []

    //====================================================================================================
    //            WEATHER DASHBOARD
    //====================================================================================================

    // function makeWeatherDataChart(){
    //
    //     let thisSensorReadingSet = weatherReadings.filter(s => s.sensor_id == sensor.sensor_id );
    //     weatherReadingData = [];
    //     thisSensorReadingSet.forEach( reading => {
    //         rowData = []
    //         // Extract KPa value, Sensor Id, and Date
    //         sensorId = reading["sensor_id"];
    //         date = reading["recorded_at"];
    //         let formatedDate = new Date(date);
    //         kpa = reading["kpa_value"]
    //         // console.log(`Next Reading: ${sensorId} ${formatedDate} ${kpa}`)
    //         rowData[0] = formatedDate;
    //         rowData[1] = kpa;
    //         rowData[2] = crop[0]["dry_kpa"];
    //         rowData[3] = crop[0]["ideal_kpa"];
    //         rowData[4] = crop[0]["saturated_kpa"];
    //         weatherReadingData.push(rowData)
    //     });
    //     // console.log(thisSensorReadingSet);
    //
    //     let seriesData = [];
    //     seriesData[0] = (sensor.sensor_name);
    //     seriesData[1] = ("dry_kpa");
    //     seriesData[2] = ("ideal_kpa");
    //     seriesData[3] = ("saturated_kpa");
    //
    //     let divId = `sensor-reading-chart-${sensor.sensor_id}`;
    //     chartingController.buildChart(divId, weatherReadingData, seriesData, "", "Kpa")
    // }

//     0:
// humidity: 16.167
// p_key: 1
// pressure: 27.345
// sensor_id: "BME_1"
// temperature: 86.721
// timestamp: "2020-08-14T14:44:46.737009"

    function makeWeatherDataChart(seriesData, divId, title, yLabel){
        //  Iterate through the reading data
        weatherReadingData = [];
        let seriesLabels = [];
        for (const [key, value] of Object.entries(seriesData)) {
            seriesLabels.push(value);
        }
        console.log(seriesLabels)
        weatherReadings.forEach(reading => {
            rowData = []
            date = reading["timestamp"];
            let formatedDate = new Date(date);
            rowData[0] = formatedDate;
            rowDataIndex = 1;
            for (const [key, value] of Object.entries(seriesData)) {
                rowData[rowDataIndex] = reading[key];
                rowDataIndex += 1;
            }
            weatherReadingData.push(rowData)
        })
        console.log("Final Sensor Chart Data:")
        console.log(weatherReadingData);
        chartingController.buildChart(divId, weatherReadingData, seriesLabels, title, yLabel)
    }

    function fetchWeatherReadingData(){
        console.log(`Fetch Sensor Reading Data`)
        // let weatherReadingsUrl = "/weather/readings?days=14";
        let weatherReadingsUrl = "/weather/readings";

        fetch(weatherReadingsUrl)
            .then( (resp) => resp.json())
            .then( function(data){
                console.log("Returned Weather Reading Data (Dashboard):")
                console.log(data)
                weatherReadings = data;
                let seriesData = {};
                seriesData = {"temperature":"Temperature"};
                makeWeatherDataChart(seriesData,"weatherReadingsTemperature","Temperature", "deg (F)");
                seriesData = {"humidity":"Humidity"};
                makeWeatherDataChart(seriesData,"weatherReadingsHumidity","Humidity", "rel hum (%)");
                seriesData = {"pressure":"Pressure"};
                makeWeatherDataChart(seriesData,"weatherReadingsPressure","Pressure", "inHG");
                seriesData = {"temperature":"Temperature", "humidity":"Humidity","pressure":"Pressure"};
                makeWeatherDataChart(seriesData,"weatherReadingsAll","Temperature, Humidity, Pressure", "Value");
            })
            .catch( function(error){
                console.log("Error with Weather Data (Dashboard)")

            });
    }



        // Public Methods/Data
    return {
        initPanel: function(){
            console.log("Init Weather Panel")
            fetchWeatherReadingData();
        },
        publicFunction2: function(){
            console.log("Public Function 2 Called")
        }
    }

})();










