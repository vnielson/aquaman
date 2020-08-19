$(function() {
    console.log("WE Controller Running....")
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
    $("#jsGridWateringEvents").jsGrid({
        width: "100%",
        inserting: false,
        editing: false,
        paging: false,
        autoload: true,
        loadIndication: true,
         controller: {
            loadData: function() {
                console.log("LOAD DATA: Watering Events");
                var d = $.Deferred();
                var url = "/watering_events/"

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
            deleteItem: function(item) {
                var d = $.Deferred();
                var url = "/watering_events/"+ item.p_key;
                console.log(`Delete Watering Event : ${item.p_key}  :: URL: ${url}`)
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
        },
        fields: [
            { name: "p_key", type: "number", width: 20, title: "ID" },
            // { name: "created", type: "date", width: 40, title: "Created"},
             { title: "Created", name: "created", type: "date", width: 25, cellRenderer: function(item){
                let options = {timeOnly:false}
              return $("<td>").append(formatDate(item, options));
            } },
            { name: "valve_name", type: "text", width: 20, title: "Valve"},
            { name: "state", type: "text", width: 20, title: "Event State"},
            { name: "open_time", type: "number", width: 20, title: "Open Time", cellRenderer: function(item){
                if (item){
                    item = item.toFixed(2)
                }
                // else {
                //     item = 0;
                // }
              return $("<td>").append(item);
            } },
            { name: "water_start", type: "date", width: 40, title: "Start", cellRenderer: function(item){
                let options = {timeOnly:true}
              return $("<td>").append(formatDate(item, options));
            } },
           { name: "water_stop", type: "date", width: 40, title: "End", cellRenderer: function(item){
                let options = {timeOnly:true}
              return $("<td>").append(formatDate(item, options));
            } },
            { name: "trigger_kpa", type: "number", width: 20, title: "Trigger KPa", cellRenderer: function(item){
                if (item){
                    item = item.toFixed(2)
                }
              return $("<td>").append(item);
            } },
            { type: "control" }
        ]


    });

});
