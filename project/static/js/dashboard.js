var dashboardController = (function (){

    var sensors = [];
    var sensorReadings = [];
    var sensorIdToIndexMap = []

    function makeAllSensorReadingChart(){
        // Create a mapping between sensor id and data index value
        nxtIndex = 1;
        sensors.forEach(s => {
            sensorIdToIndexMap[s.sensor_id] = nxtIndex;
            nxtIndex++;
        });
        //  Iterate through the reading data
        sensorReadingData = [];
        sensorReadings.forEach(reading => {
            rowData = []
            for (let x = 1; x < sensors.length; ++x){
                rowData[x] = ''
            }
            // Extract KPa value, Sensor Id, and Date
            sensorId = reading["sensor_id"];
            date = reading["recorded_at"];
            let formatedDate = new Date(date);
            // console.log(formatedDate)
            // 2020-06-30T13:05:56.665702
            // dateData = date.split
            // formatedDate = new Date(year, monthIndex [, day [, hours [, minutes [, seconds [, milliseconds]]]]])
            kpa = reading["kpa_value"]
            // console.log(`Next Reading: ${sensorId} ${formatedDate} ${kpa}`)
            rowData[0] = formatedDate;
            rowData[sensorIdToIndexMap[sensorId]] = kpa
            sensorReadingData.push(rowData)
        })
        // console.log("Final Sensor Chart Data:")
        // console.log(sensorReadingData);
        let seriesData = [];
        sensors.forEach(s => {
            seriesData.push(s.sensor_name);
        });
        chartingController.buildChart("sensorReadingsAll", sensorReadingData, seriesData, "All Sensors", "Kpa")

    }

    function fetchSensorData(){
        console.log("Fetch Sensor Data")
        let sensorDataUrl = "/sensors/";

        fetch(sensorDataUrl)
            .then( (resp) => resp.json())
            .then( function(data){
                // console.log("Returned Sensor Data (Dashboard):")
                // console.log(data)
                sensors = []
                data.forEach(s => {
                   sensors.push(s);
                });
                // console.log("Sensors is : ");
                // console.log(sensors);
                addSensorHTML(data);

            })
            .catch( function(error){

            });
    }

    function fetchSensorReadingData(){
        console.log(`Fetch Sensor Reading Data`)
        let sensorReadingsUrl = "/sensors/readings/";

        fetch(sensorReadingsUrl)
            .then( (resp) => resp.json())
            .then( function(data){
                console.log("Returned Sensor Reading Data (Dashboard):")
                console.log(data)
                sensorReadings = data;
                makeAllSensorReadingChart();
                // data.forEach(s => {
                //    sensors.push(s);
                // });
                // console.log("Sensors is : ");
                // console.log(sensors);
                // addSensorHTML(data);
                // addSensorReadingCharts();

            })
            .catch( function(error){

            });
    }
    function addSensorReadingCharts(){

        sensors.forEash(s => {

        });

    }


    function addSensorHTML(sensorData){

        let finalMarkUp = "";
        sensorData.forEach(s => {
            // console.log("Sensor Data:");
            // console.log(s)

        var markUp = `<div class="col">
                        <div class="card" style="width: 36rem;">
                        <div class="card-body">
                            <h5 class="card-title">Sensor ${s.sensor_id}</h5>
                            <table class="table table-sm">
                              <thead>
                                <tr>
                                  <th scope="col">Valve</th>
                                  <th scope="col">BCM Pin</th>
                                  <th scope="col">Crop</th>
                                  <th scope="col">Config</th>
                                </tr>
                              </thead>
                              <tbody>
                                <tr>
                                  <td>${s.valve_name}</td>
                                  <td>${s.bcm_pin}</td>
                                  <td>${s.crop_name}</td>
                                  <td>${s.configuration}</td>
                                </tr>
                              </tbody>
                            </table>

                            <div class="sensor-reading-chart" id="sensor-reading-chart-${s.sensor_id}" style="display:none">
                            </div>
                        </div>
                    </div>
                </div>`

            finalMarkUp = finalMarkUp + markUp;
        });

        $("#db-sensors-div").html(finalMarkUp)
    }

        // Public Methods/Data
    return {
        initPanel: function(){
            console.log("Init Dashboard Panel")
            fetchSensorData();
            fetchSensorReadingData();
            // sensorData = "Date,Temperature\n" +
            //                 "2008-05-07,75\n" +
            //                 "2008-05-08,70\n" +
            //                 "2008-05-09,80\n"
            // chartingController.buildChart("chart-sensor-1",sensorData, "Sensor Title", "X Label", "yLable")
        },
        publicFunction2: function(){
            console.log("Public Function 2 Called")
        }
    }

})();