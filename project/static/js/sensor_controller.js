
var aqSensorController = (function(){


    // Public Methods/Data
    return {
        loadDataTable: function(){
            return false
        },
        getTableData: function(filter){
            console.log("Build Data Table");
            let tableData = [];
            return tableData;
        }

    }
})();

    var crops = [
                {
                    name: "WA_1",
                    id: 1
                },
                {
                    name: "WA_2",
                    id: 2
                },
                {
                    name: "WA_3",
                    id: 3
                }


            ];

    var valves = [
                {
                    name: "WA_1",
                    id: 1
                },
                {
                    name: "WA_2",
                    id: 2
                },
                {
                    name: "WA_3",
                    id: 3
                }


            ];
    $(function() {
    $("#jsGridSensorInfo").jsGrid({
        width: "100%",
        inserting: true,
        editing: true,
        paging: false,
        autoload: true,
        loadIndication: true,
         controller: {
            loadData: function() {
                console.log("LOAD DATA: Sensor Info");
                var d = $.Deferred();
                var url = "/sensors/"

                $.ajax({
                    url: url,
                    dataType: "json",
                    type: "GET"
                }).done(function(response) {
                    console.log(response)
                    d.resolve(response);
                });
                return d.promise();
            },
            updateItem: function(item) {
                var d = $.Deferred();
                // console.log(item);
                var url = "/sensors/" + item.sensor_id
                $.ajax({
                    url: url,
                    data: JSON.stringify(item),
                    type: "PUT",
                    dataType: "json",
                    contentType: "application/json",
                }).done(function(response) {
                    // console.log("Update Response")
                    // console.log(response);
                    d.resolve(response);
                });
                return d.promise();
            },
            deleteItem: function(item) {
                var d = $.Deferred();
                var url = "/sensors/"+ item.sensor_id;
                console.log(`Delete Sensor : ${item.sensor_id}  :: URL: ${url}`)
                $.ajax({
                    url: url,
                    data: item,
                    type: "DELETE",
                }).done(function(response) {
                    // console.log("Delete Response");
                    // console.log(response);
                    if (response.success){
                        console.log("Deleted success")
                        d.resolve(response);
                    }else {
                        console.log(`Delete Failed with message: ${response.message}`)
                        displayToast(response.type, response.title, response.message);
                        d.reject(response);
                    }
                });
                return d.promise();
            },
            insertItem: function(item) {
                var d = $.Deferred();
                var url = "/sensors/";
                // console.log("URL for POST")
                // console.log(url)
                console.log("Insert Sensor:");
                console.log(item);
                $.ajax({
                    url: url,
                    data: JSON.stringify(item),
                    dataType: "json",
                    contentType: "application/json",
                    type: "POST",
                }).done(function(response) {
                    console.log("Insert Response")
                    console.log(response);
                    // This approach leads to a bug where added school is listed twice
                    // addSchool(response);
                    // updateContestantTabInfo();
                    d.resolve(response);
                });
                return d.promise();
            },
        },

        fields: [
            { name: "sensor_id", type: "number", width: 20, title: "ID", filtering: false, readOnly: true},
            { name: "configuration", type: "text", width: 20, title: "Config", filtering: false},
            {
                name: "crop_id",
                type: "select",
                items: crops,
                valueField: "crop_id",
                valueType: "number",
                textField: "crop_name",
                width: 20,
                validate: "required",
                title: "Crop"
            },
            {
                name: "valve_id",
                type: "select",
                items: valves,
                valueField: "valve_id",
                valueType: "number",
                textField: "valve_name",
                width: 20,
                validate: "required",
                title: "Valve"
            },
            // { name: "crop", type: "text", width: 20, title: "Crop", filtering: false},
            // { name: "valve", type: "number", width: 20, title: "valve", filtering: false},
            { name: "bcm_pin", type: "number", width: 20, title: "BCM Pin", filtering: false},
            { type: "control" }
        ]


    });

});

$(function() {
    $("#jsGridSensorReadings").jsGrid({
        width: "100%",
        inserting: false,
        editing: false,
        sorting: true,
        filtering: true,
        paging: true,
        autoload: true,
        loadIndication: true,
         controller: {
            loadData: function() {
                console.log("LOAD DATA: Sensor Readings");
                var d = $.Deferred();
                var url = "/sensors/readings"

                $.ajax({
                    url: url,
                    dataType: "json",
                    type: "GET"
                }).done(function(response) {
                    console.log("Readings")
                    console.log(response)
                    d.resolve(response);
                });
                return d.promise();
            },
            updateItem: function(item) {
                var d = $.Deferred();
                // console.log(item);
                var url = "/sensors/" + item.id
                $.ajax({
                    url: url,
                    data: JSON.stringify(item),
                    type: "PUT",
                    dataType: "json",
                    contentType: "application/json",
                }).done(function(response) {
                    // console.log("Update Response")
                    // console.log(response);
                    d.resolve(response);
                });
                return d.promise();
            },
            deleteItem: function(item) {
                var d = $.Deferred();
                var url = "/sensors/"+ item.id;
                $.ajax({
                    url: url,
                    data: item,
                    type: "DELETE",
                }).done(function(response) {
                    // console.log("Delete Response");
                    // console.log(response);
                    if (response.success){
                        console.log("Deleted success")
                        d.resolve(response);
                    }else {
                        console.log(`Delete Failed with message: ${response.message}`)
                        displayToast(response.type, response.title, response.message);
                        d.reject(response);
                    }
                });
                return d.promise();
            },
            insertItem: function(item) {
                var d = $.Deferred();
                var url = "/sensors/";
                // console.log("URL for POST")
                // console.log(url)
                $.ajax({
                    url: url,
                    data: JSON.stringify(item),
                    dataType: "json",
                    contentType: "application/json",
                    type: "POST",
                }).done(function(response) {
                    console.log("Insert Response")
                    console.log(response);
                    // This approach leads to a bug where added school is listed twice
                    // addSchool(response);
                    // updateContestantTabInfo();
                    d.resolve(response);
                });
                return d.promise();
            },
        },
        fields: [
            { name: "sensor_id", type: "number", width: 20, title: "ID"},
            { name: "recorded_at", type: "date", width: 20, title: "Date Recorded"},
            { name: "kpa_value", type: "number", width: 20, title: "KPa Value"},
            { name: "computed_frequency", type: "number", width: 20, title: "Computed Freq"},
            { name: "min_frequency", type: "number", width: 20, title: "Min Freq"},
            { name: "max_frequency", type: "number", width: 20, title: "Max Freq"},
            { name: "mean", type: "number", width: 20, title: "Mean"},
            { name: "std_dev", type: "number", width: 20, title: "STD Dev"},
            { type: "control",
                editButton: false,
                deleteButton: false
            }
        ]


    });

});
