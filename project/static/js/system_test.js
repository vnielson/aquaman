var systemTestController = (function (){

    function fetchSensorData(){
        console.log("Fetch Sensor Data")
        let sensorDataUrl = "/sensors/";

        fetch(sensorDataUrl)
            .then( (resp) => resp.json())
            .then( function(data){
                console.log("Returned Sensor Data:")
                console.log(data)
                addSensorHTML(data);

            })
            .catch( function(error){

            });
    }

    function fetchSensorReading(sensorTarget){
        console.log("Fetch Sensor Reading")
        let sensorId = 1;
        let sensorDataUrl = "/sensors/get_reading/" + sensorId;

        fetch(sensorDataUrl)
            .then( (resp) => resp.json())
            .then( function(data){
                console.log("Returned Sensor Data:")
                console.log(data)
                setSensorReadingData(sensorTarget, data);

            })
            .catch( function(error){

            });
    }


    function addSensorHTML(sensorData){

        let finalMarkUp = "";
        sensorData.forEach(s => {
        var markUp = `<div class="card" style="width: 24rem;">
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
                                  <td>${s.valve}</td>
                                  <td>${s.bcm_pin}</td>
                                  <td>${s.crop}</td>
                                  <td>${s.configuration}</td>
                                </tr>
                              </tbody>
                            </table>
                            <a href="#" class="card-link get-sensor-reading" data-target="#sensor-reading-${s.sensor_id}">Get Sensor Reading</a>


                            <div class="sensor-reading" id="sensor-reading-${s.sensor_id}" style="display:none">
                            </div>
                        </div>
                    </div>`

            finalMarkUp = finalMarkUp + markUp;
        });

        $("#sensors-div").html(finalMarkUp)
    }

    function setSensorReadingData(target, sensorData){
        console.log("Set Sensor data: ")
        console.log(sensorData);
        let markUp = `<table class="table table-sm">
                          <thead>
                            <tr>
                              <th scope="col">Kpa Val</th>
                              <th scope="col">Min Freq</th>
                              <th scope="col">Max Freq</th>
                              <th scope="col">Computed Freq</th>
                              <th scope="col">Mean</th>
                              <th scope="col">STD Dev</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td>${sensorData.kpa_value.toFixed(2)}</td>
                              <td>${sensorData.min_frequency.toFixed(2)}</td>
                              <td>${sensorData.max_frequency.toFixed(2)}</td>
                              <td>${sensorData.computed_frequency.toFixed(2)}</td>
                              <td>${sensorData.mean.toFixed(2)}</td>
                              <td>${sensorData.std_dev.toFixed(2)}</td>
                            </tr>
                          </tbody>
                    </table>`;
        $(target).html(markUp);
        $(target).show();
    }

    $("body").on('click',".get-sensor-reading", function(e){
        var sensorTarget = $(e.target).attr("data-target");
        console.log(`Get sensor reading for : ${sensorTarget}`);
        fetchSensorReading(sensorTarget);
    });

    // Public Methods/Data
    return {
        initPanel: function(){
            console.log("Initialize Panel")
            let sensorData = fetchSensorData();
        }
    }




})();