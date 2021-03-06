$(function() {
    $("#jsGridCropInfo").jsGrid({
        width: "100%",
        inserting: true,
        editing: true,
        paging: false,
        autoload: true,
        loadIndication: true,
         controller: {
            loadData: function() {
                console.log("LOAD DATA: Crop Info");
                var d = $.Deferred();
                var url = "/crops/"

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
                var url = "/crops/" + item.crop_id
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
                var url = "/crops/"+ item.crop_id;
                console.log(`Delete Crop : ${item.crop_id}  :: URL: ${url}`)
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
                var url = "/crops/";
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
            { name: "crop_id", type: "number", width: 20, title: "ID", filtering: false, readOnly: true},
            { name: "crop_name", type: "text", width: 20, title: "Crop", filtering: false},
            { name: "ideal_kpa", type: "number", width: 20, title: "Ideal KPa Value", filtering: false},
            { name: "dry_kpa", type: "number", width: 20, title: "Dry KPa Value", filtering: false},
            { name: "saturated_kpa", type: "number", width: 20, title: "Saturated KPa Value", filtering: false},
            { type: "control" }
        ]

    });

});
