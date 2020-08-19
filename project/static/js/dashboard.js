var dashboardController = (function (){


    var sensors = [];
    var sensorReadings = [];
    var sensorIdToIndexMap = [];
    var cropData = [];

    var makeSensorChartTimings = {begin: 0,
                                  fetchSensorData: 0}

    var valves = [];

    function formatDate(item, options){
        const dateRecorded = new Date(item);
        let day = dateRecorded.getDate();
        let month = dateRecorded.getMonth() + 1;
        let timeOfDay = dateRecorded.toLocaleTimeString('en-US');
        let formatedDate = `${month}/${day}&nbsp;&nbsp;&nbsp;${timeOfDay}`
        if (options["timeOnly"]){
            formatedDate = `${timeOfDay}`
        }
        return formatedDate;
    }


    function fetchWeatherData(){
        console.log("Fetch Weather Data")
        let weatherDataUrl = "/weather/current";

        fetch(weatherDataUrl)
            .then( (resp) => resp.json())
            .then( function(data){
                console.log("Returned Weather Data (Dashboard):")
                console.log(data)
                console.log(data["temp"])
                let options = {timeOnly:true}
                let formatedDate = formatDate(data["timestamp"], options);
                $("#w-time-stamp").text(formatedDate);
                $("#w-temperature").text(data["temp"].toFixed(2) + " degF");
                $("#w-humidity").text(data["humidity"].toFixed(2) + "% rH");
                $("#w-pressure").text(data["pressure"].toFixed(3) + " inHG");
            })
            .catch( function(error){
                console.log("Error with weather Data (Dashboard)")

            });
    }

    function fetchCropData(){
        console.log("Fetch Crop Data")
        let cropDataUrl = "/crops/";

        fetch(cropDataUrl)
            .then( (resp) => resp.json())
            .then( function(data){
                // console.log("Returned Crop Data (Dashboard):")
                // console.log(data)
                cropData = data;

            })
            .catch( function(error){
                console.log("Error with crop Data (Dashboard)")

            });
    }
    //====================================================================================================
    //            SENSOR DASHBOARD
    //====================================================================================================


// computed_frequency: 1776.83
// kpa_value: 27
// max_frequency: 3676.471
// mean: 1776.83
// min_frequency: 766.871
// p_key: 1
// recorded_at: "2020-07-14T15:02:55.133286"
// sensor_id: 3
// sensor_name: "Tomato Wine Barrell"
// std_dev: 0

    function makeIndividualSensorReadingChart(sensor){

        // console.log("In make individual chart for :" );
        // console.log(sensor);

        let crop = cropData.filter(c => c.crop_id == sensor.crop_id);

// crop_id: 1
// crop_name: "Tomato"
// dry_kpa: 155
// ideal_kpa: 122
// saturated_kpa: 89

        let thisSensorReadingSet = sensorReadings.filter(s => s.sensor_id == sensor.sensor_id );
        sensorReadingData = [];
        thisSensorReadingSet.forEach( reading => {
            rowData = []
            // Extract KPa value, Sensor Id, and Date
            sensorId = reading["sensor_id"];
            date = reading["recorded_at"];
            let formatedDate = new Date(date);
            kpa = reading["kpa_value"]
            // console.log(`Next Reading: ${sensorId} ${formatedDate} ${kpa}`)
            rowData[0] = formatedDate;
            rowData[1] = kpa;
            rowData[2] = crop[0]["dry_kpa"];
            rowData[3] = crop[0]["ideal_kpa"];
            rowData[4] = crop[0]["saturated_kpa"];
            sensorReadingData.push(rowData)
        });
        // console.log(thisSensorReadingSet);

        let seriesData = [];
        seriesData[0] = (sensor.sensor_name);
        seriesData[1] = ("dry_kpa");
        seriesData[2] = ("ideal_kpa");
        seriesData[3] = ("saturated_kpa");

        let divId = `sensor-reading-chart-${sensor.sensor_id}`;
        chartingController.buildChart(divId, sensorReadingData, seriesData, "", "Kpa")
    }

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
            for (let x = 1; x < sensors.length+1; ++x){
                rowData[x] = NaN
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
            // rowData[2] = kpa - 5
            sensorReadingData.push(rowData)
        })
        // console.log("Final Sensor Chart Data:")
        // console.log(sensorReadingData);
        let seriesData = [];
        sensors.forEach(s => {
            seriesData.push(s.sensor_name);
        });
        chartingController.buildChart("sensorReadingsAll", sensorReadingData, seriesData, "All Sensors", "Kpa")
        makeSensorChartTimings["makeSensorReadingsChart"] =  performance.now();
        // console.log("Chart Timings:")
        // console.log(makeSensorChartTimings);
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
                makeSensorChartTimings["fetchSensorData"] =  performance.now();

                addSensorHTML(data);

            })
            .catch( function(error){

            });
    }

    function fetchSensorReadingData(){
        console.log(`Fetch Sensor Reading Data`)
        let sensorReadingsUrl = "/sensors/readings?days=14";

        fetch(sensorReadingsUrl)
            .then( (resp) => resp.json())
            .then( function(data){
                // console.log("Returned Sensor Reading Data (Dashboard):")
                // console.log(data)
                sensorReadings = data;
                makeSensorChartTimings["fetchSensorReadingData"] =  performance.now();
                // makeAllSensorReadingChart();
                sensors.forEach( s => {
                    makeIndividualSensorReadingChart(s);
                });
                // data.forEach(s => {
                //    sensors.push(s);
                // });
                // console.log("Sensors is : ");
                // console.log(sensors);
                // addSensorHTML(data);
                // addSensorReadingCharts();

            })
            .catch( function(error){
                console.log("Error with Sensor Data (Dashboard)")

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
                        <div class="card" style="width: 32rem;">
                        <div class="card-body">
                            <h5 class="card-title">Sensor: ${s.sensor_name}</h5>
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

                            <div class="sensor-reading-chart" id="sensor-reading-chart-${s.sensor_id}" style="width:400px; height:300px">
                            </div>
                        </div>
                    </div>
                </div>`

            finalMarkUp = finalMarkUp + markUp;
        });

        $("#db-sensors-div").html(finalMarkUp)
    }

    //====================================================================================================
    //            VALVE DASHBOARD
    //====================================================================================================
    function fetchValveData(){
        console.log("Fetch Valve Data")
        let valveDataUrl = "/valves/";

        fetch(valveDataUrl)
            .then( (resp) => resp.json())
            .then( function(data){
                // console.log("Returned Valve Data (Dashboard):")
                // console.log(data)
                valves = []
                data.forEach(v => {
                   valves.push(v);
                });
                // console.log("Sensors is : ");
                // console.log(sensors);
                addValveHTML(data);

            })
            .catch( function(error){
                console.log("Error with valve Data (Dashboard)")

            });
    }
    function addValveHTML(valveData){

        let finalMarkUp = "";
        valveData.forEach(v => {
            console.log("valveData Data:");
            console.log(v)

        var markUp = `<div class="col">
                        <div class="card" style="width: 36rem;">
                        <div class="card-body">
                            <h5 class="card-title">Valve: ${v.valve_name}</h5>
                            <table class="table table-sm">
                              <thead>
                                <tr>
                                  <th scope="col">Relay Controller</th>
                                </tr>
                              </thead>
                              <tbody>
                                <tr>
                                  <td>${v.relay_controller}</td>
                                </tr>
                              </tbody>
                            </table>

                            <div class="valve-watering-chart" id="valve-watering-chart-${v.valve_id}" style="display:none">
                            </div>
                        </div>
                    </div>
                </div>`

            finalMarkUp = finalMarkUp + markUp;
        });

        $("#db-valves-div").html(finalMarkUp)
    }
        // Public Methods/Data
    return {
        initPanel: function(){
            console.log("Init Dashboard Panel")
            makeSensorChartTimings["begin"] =  performance.now();
            fetchSensorData();
            fetchSensorReadingData();
            fetchValveData();
            fetchCropData();
            fetchWeatherData();
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










 $(document).ready(function() {
      var g, regression, clearLines;  // defined below
      document.getElementById("ry1").onclick = function() { regression(1); };
      document.getElementById("ry2").onclick = function() { regression(2); };
      document.getElementById("clear").onclick = function() { clearLines(); };

      var data = [];
      for (var i = 0; i < 120; i++) {
        data.push([i,
                   i / 5.0 + 10.0 * Math.sin(i / 3.0),
                   30.0 - i / 5.0 - 10.0 * Math.sin(i / 3.0 + 1.0)]);
      }

      // coefficients of regression for each series.
      // if coeffs = [ null, [1, 2], null ] then we draw a regression for series 1
      // only. The regression line is y = 1 + 2 * x.
      var coeffs = [ null, null, null ];
      regression = function(series) {
        // Only run the regression over visible points.
        var range = g.xAxisRange();

        var sum_xy = 0.0, sum_x = 0.0, sum_y = 0.0, sum_x2 = 0.0, num = 0;
        for (var i = 0; i < g.numRows(); i++) {
          var x = g.getValue(i, 0);
          if (x < range[0] || x > range[1]) continue;

          var y = g.getValue(i, series);
          if (y === null || y === undefined) continue;
          if (y.length == 2) {
            // using fractions
            y = y[0] / y[1];
          }

          num++;
          sum_x += x;
          sum_y += y;
          sum_xy += x * y;
          sum_x2 += x * x;
        }

        var a = (sum_xy - sum_x * sum_y / num) / (sum_x2 - sum_x * sum_x / num);
        var b = (sum_y - a * sum_x) / num;

        coeffs[series] = [b, a];
        if (typeof(console) != 'undefined') {
          console.log("coeffs(" + series + "): [" + b + ", " + a + "]");
        }

        g.updateOptions({});  // forces a redraw.
      };

      clearLines = function() {
        for (var i = 0; i < coeffs.length; i++) coeffs[i] = null;
        g.updateOptions({});
      };

      function drawLines(ctx, area, layout) {
        if (typeof(g) == 'undefined') return;  // won't be set on the initial draw.

        var range = g.xAxisRange();
        for (var i = 0; i < coeffs.length; i++) {
          if (!coeffs[i]) continue;
          var a = coeffs[i][1];
          var b = coeffs[i][0];

          var x1 = range[0];
          var y1 = a * x1 + b;
          var x2 = range[1];
          var y2 = a * x2 + b;

          var p1 = g.toDomCoords(x1, y1);
          var p2 = g.toDomCoords(x2, y2);

          var c = Dygraph.toRGB_(g.getColors()[i - 1]);
          c.r = Math.floor(255 - 0.5 * (255 - c.r));
          c.g = Math.floor(255 - 0.5 * (255 - c.g));
          c.b = Math.floor(255 - 0.5 * (255 - c.b));
          var color = 'rgb(' + c.r + ',' + c.g + ',' + c.b + ')';
          ctx.save();
          ctx.strokeStyle = color;
          ctx.lineWidth = 1.0;
          ctx.beginPath();
          ctx.moveTo(p1[0], p1[1]);
          ctx.lineTo(p2[0], p2[1]);
          ctx.closePath();
          ctx.stroke();
          ctx.restore();
        }
      }

      g = new Dygraph(
              document.getElementById("demodiv"),
              data,
              {
                labels: ['X', 'Y1', 'Y2'],
                underlayCallback: drawLines,
                drawPoints: true,
                drawAxesAtZero: true,
                strokeWidth: 0.0
              }
          );
    }
);