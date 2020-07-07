$(document).ready(function(){
    console.log("On document Ready function runningxxxxxx...");
});

var panelIds = ['#panel-dashboard', '#panel-sensors', '#panel-valves', '#panel-crops', '#panel-watering-events','#panel-system-test']
console.log("Index.js is running")

function hidePanels(){
    panelIds.forEach( p => {
        console.log(`Hide: ${p}`);
       $(p).hide()
    });
}

function showPanel(panelToShow){
        console.log(`Show: ${panelToShow}`);
    $(panelToShow).show();
}

$(".panel-nav").on('click', function(e){
    console.log("Dashboard Clicked");
    console.log(e.target)
    var panelToShow = $(e.target).attr("data-target");
    console.log(`Panel to Show: ${panelToShow}`)
    fetchCropandValveData();
    hidePanels();
    showPanel(panelToShow);

    if (panelToShow == "#panel-system-test"){
        systemTestController.initPanel();
    }

    if (panelToShow == "#panel-dashboard"){
        dashboardController.initPanel();
    }

});

async function fetchCropandValveData() {

    try {
        //Get Crop information
        var cropDataUrl = "/crops/";
        var cropDataResponse = await fetch(cropDataUrl);
        var cropData = await cropDataResponse.json();

        // console.log(`Crop Data ${cropData}`)
        // console.log(cropData);
        $("#jsGridSensorInfo").jsGrid("fieldOption", "crop_id", "items", cropData);


        //Get Valve information
        var valveDataUrl = "/valves/";
        var valveDataResponse = await fetch(valveDataUrl);
        var valveData = await valveDataResponse.json();

        // console.log(`Valve Data ${cropData}`)
        // console.log(valveData);
        $("#jsGridSensorInfo").jsGrid("fieldOption", "valve_id", "items", valveData);

        $("#jsGridSensorInfo").jsGrid("loadData");
        $("#jsGridWateringEvents").jsGrid("loadData");

    } catch (error) {
        alert("Problem with refresh state")
    }

}
