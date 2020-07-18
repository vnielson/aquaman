var systemTestController = (function (){

    $("#test-do-watering").on('click', function(e){
       console.log("In do click......................")
        e.preventDefault();
        let testDoWateringUrl = "/test_do_watering";

        fetch(testDoWateringUrl)
            .then( (resp) => resp.json())
            .then( function(data){
                console.log("Returned Test Do Watering Data:")
                console.log(data)

            })
            .catch( function(error){
                console.log("Error in test do watering");
            });
    });

    function fetchValveData(){
        console.log("Fetch Valve Data")
        let valveDataUrl = "/valves/";

        fetch(valveDataUrl)
            .then( (resp) => resp.json())
            .then( function(data){
                console.log("Returned Valve Data:")
                console.log(data)
                addValveHTML(data);

            })
            .catch( function(error){

            });
    }
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
        let splitTarget = sensorTarget.split('-');
        console.log(splitTarget)
        let sensorId = sensorTarget.split('-')[2];
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

    function fetchValveStatus(valveTarget){
        console.log("Fetch Valve Status")
        console.log(valveTarget)
        let splitTarget = valveTarget.split('-');
        console.log(splitTarget)
        let valveId = valveTarget.split('-')[2];
        let valveDataUrl = "/valves/get_status/" + valveId;

        fetch(valveDataUrl)
            .then( (resp) => resp.json())
            .then( function(data){
                console.log("Returned Valve Data:")
                console.log(data)
                setValveStatusData(valveTarget, data);

            })
            .catch( function(error){

            });
    }

    function openValve(valveTarget){
        console.log("Open Valve")
        let splitTarget = valveTarget.split('-');
        console.log(splitTarget)
        let valveId = valveTarget.split('-')[2];
        let openValveUrl = "/valves/open/" + valveId;

        fetch(openValveUrl)
            .then( (resp) => resp.json())
            .then( function(data){
                console.log("Returned Valve Data:")
                console.log(data)
                splitTarget[1] = "status"
                let statusTarget = splitTarget.join('-')
                fetchValveStatus(statusTarget)
                // setValveStatusData(valveTarget, data);

            })
            .catch( function(error){

            });
    }

    function closeValve(valveTarget){
        console.log("Close Valve")
        let splitTarget = valveTarget.split('-');
        console.log(splitTarget)
        let valveId = valveTarget.split('-')[2];
        let closeValveUrl = "/valves/close/" + valveId;

        fetch(closeValveUrl)
            .then( (resp) => resp.json())
            .then( function(data){
                console.log("CLOSE Returned Valve Data:")
                console.log(data)
                splitTarget[1] = "status"
                let statusTarget = splitTarget.join('-')
                fetchValveStatus(statusTarget)
                // setValveStatusData(valveTarget, data);

            })
            .catch( function(error){

            });
    }


    function addSensorHTML(sensorData){

        let finalMarkUp = "";
        sensorData.forEach(s => {
            console.log("Sensor Data:");
            console.log(s)




        var markUp = `<div class="col">
                        <div class="card" style="width: 24rem;">
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
                            <a href="#" class="card-link get-sensor-reading" data-target="#sensor-reading-${s.sensor_id}">Get Sensor Reading</a>


                            <div class="sensor-reading" id="sensor-reading-${s.sensor_id}" style="display:none">
                            </div>
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


    function setValveStatusData(target, valveData){
        console.log("Set Valve Status data: ")
        console.log(valveData);
        let markUp = `<table class="table table-sm">
                          <thead>
                            <tr>
                              <th scope="col">Status</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td>${valveData.status}</td>
                            </tr>
                          </tbody>
                    </table>`;
        $(target).html(markUp);
        $(target).hide();
        $(target).show();
    }

    function addValveHTML(valveData){
        console.log("Valve Data HTML METHOD:");
        console.log(valveData);

        let finalMarkUp = "";
        valveData.forEach(v => {
            console.log(v)

        var markUp = `<div class="col">
                        <div class="card" style="width: 24rem;">
                        <div class="card-body">
                            <h5 class="card-title">Valve ${v.valve_id}</h5>
                            <table class="table table-sm">
                              <thead>
                                <tr>
                                  <th scope="col">Valve ID</th>
                                  <th scope="col">Valve Name</th>
                                  <th scope="col">Relay Controller</th>
                                </tr>
                              </thead>
                              <tbody>
                                <tr>
                                  <td>${v.valve_id}</td>
                                  <td>${v.valve_name}</td>
                                  <td>${v.relay_controller}</td>
                                </tr>
                              </tbody>
                            </table>
                            <a href="#" class="card-link open-valve" data-target="#valve-open-${v.valve_id}">Open Valve</a>
                            <a href="#" class="card-link close-valve" data-target="#valve-close-${v.valve_id}">Close Valve</a>
                            <a href="#" class="card-link get-valve-status" data-target="#valve-status-${v.valve_id}">Get Valve Status</a>

                            <div class="valve-status" id="valve-status-${v.valve_id}" style="display:none">
                            </div>
                        </div>
                    </div>
                </div>`

            finalMarkUp = finalMarkUp + markUp;
        });

        $("#valves-div").html(finalMarkUp)
    }

    $("body").on('click',".get-sensor-reading", function(e){
        var sensorTarget = $(e.target).attr("data-target");
        console.log(`Get sensor reading for : ${sensorTarget}`);
        fetchSensorReading(sensorTarget);
    });

    $("body").on('click',".get-valve-status", function(e){
        var valveTarget = $(e.target).attr("data-target");
        console.log(`Get valve status for : ${valveTarget}`);
        fetchValveStatus(valveTarget);
    });

    $("body").on('click',".open-valve", function(e){
        var valveTarget = $(e.target).attr("data-target");
        console.log(`OPEN Valve: ${valveTarget}`);
        openValve(valveTarget);
    });

    $("body").on('click',".close-valve", function(e){
        var valveTarget = $(e.target).attr("data-target");
        console.log(`CLOSE Valve: ${valveTarget}`);
        closeValve(valveTarget);
    });

    // Public Methods/Data
    return {
        initPanel: function(){
            console.log("Initialize Panel")
            fetchSensorData();
            fetchValveData();

        }
    }




})();