var chartingController = (function(){

    var charts = {};
// 2020-03-20: {Ada: "4", Bingham: "1", Blaine: "19", Canyon: "1", Kootenai: "3", …}
    function formatData(unformatedData, counties){
        // var retData = "Date," + counties + "\n";
        var retData = [];
        for (var date in unformatedData) {
            var dateData = date.split('-');
            var formatedDate = new Date(parseInt(dateData[0]), parseInt(dateData[1])-1, parseInt(dateData[2]));
            var rowData = [];
            rowData[0] = formatedDate;
            counties.forEach(function(county,index){
                // console.log(`Check for county: ${county} at index: ${index}. Date:${date}`);
                if (unformatedData[date].hasOwnProperty(county)){
                    rowData[index+1] = parseInt(unformatedData[date][county]);
                }else {
                    rowData[index+1] = 0;
                }
            });
            retData.push(rowData);
        };
        // console.log(retData);
        return retData;
    }


    // Public Methods/Data
    return {
        buildChart: function(divId, graphData, series, title, yLabel){
            // var graphData = formatData(unformatedData, counties);
            // console.log("UnformatedFormated Data: ");
            // console.log(unformatedData)
            // console.log("Formated Data: ");
            // console.log(graphData)
            // labels: [ "x", "A", "B" ]
            var labels = [];
            labels.push("Date");
            series.forEach(element => {
                labels.push(element);
            });
            console.log("Labels:");
            console.log(labels)

            let rollPeriod = 1;
            test = document.getElementById(divId)

            charts[divId] =
                new Dygraph(
                        document.getElementById(divId),
                        graphData, {
                        rollPeriod: rollPeriod,
                        // legend: 'always',
                        // errorBars: true,
                        title: title,
                        titleHeight: 32,
                        ylabel: yLabel,
                        xlabel: 'Date ',
                        strokeWidth: 1.5,
                        labels: labels,
                        showLabelsOnHighlight: true,
                        connectSeparatedPoints: true
                        // highlightSeriesOpts: {
                        //     strokeWidth: 4,
                        //     strokeBorderWidth: 1,
                        //     highlightCircleSize: 5
                        // }

                        }
                    );
         },
         adjustRollPeriod: function(forChart, newRollPeriod){
             if (charts.hasOwnProperty(forChart)){
                 charts[forChart].adjustRoll(newRollPeriod);
             }
         },
         highlightSeries: function(countyName){

            //  console.log("Highlight Series: " + countyName);
            //  console.log(charts);
             for (nextChart in charts){
                 charts[nextChart].setSelection(0, countyName);
             }

         }
    }
})();

