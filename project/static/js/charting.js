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
            console.log("Formated Data: ");
            console.log(graphData)
            // labels: [ "x", "A", "B" ]
            var labels = [];
            labels.push("Date");
            series.forEach(element => {
                labels.push(element);
            });
            console.log("Labels:");
            console.log(labels)

//     //         let testData =   "Date,Temperature\n" +
//     // "2008-05-07,75\n" +
//     // "2008-05-08,70\n" +
//     // "2008-05-09,80\n"
//             let testData =   "Date,KPa\n" +
// "30 Jun 2020 10:15:09 GMT, 4\n" +
// "30 Jun 2020 10:20:09 GMT, 6\n" +
// "30 Jun 2020 10:25:09 GMT, 12\n" +
// "30 Jun 2020 10:30:09 GMT, 3\n" +
// "30 Jun 2020 10:35:09 GMT, 0\n" +
// "30 Jun 2020 10:40:09 GMT, 1\n" +
// "30 Jun 2020 10:45:09 GMT, 3\n" +
// "30 Jun 2020 10:54:02 GMT, 0\n" +
// "30 Jun 2020 10:59:02 GMT, 12\n"
//
//             g = new Dygraph(
//
//     // containing div
//     document.getElementById(divId), testData
//
//
//   );
//             graphData =  [
//                 ["Wed Jun 24 2020 00:00:00 GMT-0600 (Mountain Daylight Time),10,100],
//                 ["Thu Jun 25 2020 00:00:00 GMT-0600 (Mountain Daylight Time)",20,80],
//                 ["Fri Jun 26 2020 00:00:00 GMT-0600 (Mountain Daylight Time)",50,60],
//                 ["Sat Jun 27 2020 00:00:00 GMT-0600 (Mountain Daylight Time)",70,80]
//               ];

// [Tue Jun 23 2020 00:00:00 GMT-0600 (Mountain Daylight Time), 13, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 9, 0, 28, 0, 0, 4, 0, 0, 0, 0, 0, 8, 15, 2, 0, 0, 42, 0, 52, 1, 43, 42, 0, 0, 5, 0, 0, 116]
// 103: (40) [Wed Jun 24 2020 00:00:00 GMT-0600 (Mountain Daylight Time), 18, 0, 0, 0, 3, 5, 0, 22, 5, 0, 0, 21, 0, 73, 0, 0, 19, 0, 0, 0, 0, 0, 0, 38, 11, 0, 0, 0, 0, 52, 1, 0, 84, 0, 0, 14, 0, 21, 16]
// 104: (40) [Thu Jun 25 2020 00:00:00 GMT-0600 (Mountain Daylight Time), 18, 0, 0, 0, 0, 20, 0, 27, 2, 0, 0, 22, 0, 11, 0, 61, 0, 0, 0, 10, 13, 0, 0, 0, 9, 3, 0, 0, 0, 17, 0, 109, 91, 0, 0, 11, 0, 21, 0]
// 105: (40) [Fri Jun 26 2020 00:00:00 GMT-0600 (Mountain Daylight Time), 30, 0, 4, 0, 0, 5, 0, 0, 0, 0, 0, 21, 0, 39, 0, 0, 14, 30, 15, 10, 0, 0, 8, 7, 2, 3, 0, 0, 0, 86, 3, 21, 28, 0, 47, 8, 0, 129, 16]
// 106: (40) [Sat Jun 27 2020 00:00:00 GMT-0600 (Mountain Daylight Time), 16, 0, 0, 0, 11, 0, 29, 0, 0, 0, 0, 16, 0, 50, 0, 0, 9, 0, 0, 0, 0, 0, 8, 0, 6, 0, 0, 0, 6, 43, 0, 0, 35, 0, 0, 7, 0, 0, 0]
// 107: (40) [Sun Jun 28 2020 00:00:00 GMT-0600 (Mountain Daylight Time), 0, 0, 6, 0, 15, 0, 0, 0, 4, 0, 0, 0, 122, 0, 0, 122, 0, 45, 0, 10, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 38, 0, 0, 0, 0, 0]
// 108: (40) [Mon Jun 29 2020 00:00:00 GMT-0600 (Mountain Daylight Time), 35, 0, 0, 0, 0, 20, 58, 38, 0, 0, 0, 29, 0, 106, 0, 0, 9, 0, 15, 20, 26, 17, 0, 38, 26, 6, 0, 0, 6, 190, 3, 130, 49, 0, 0, 22, 0, 0, 33]
// length: 109
// (2) ["2020-06-30T12:51:56.678102", 0]
// 1: (2) ["2020-06-30T12:52:56.675307", 0]
// 2: (2) ["2020-06-30T12:53:56.673200", 0]
// 3: (2) ["2020-06-30T12:54:56.668309", 0]
// 4: (2) ["2020-06-30T12:55:56.674599", 0]
// 5: (2) ["2020-06-30T12:56:56.696463", 0]
// 6: (2) ["2020-06-30T12:57:56.665549", 0]
// 7: (2) ["2020-06-30T12:58:56.664262", 0]
// 8: (2) ["2020-06-30T12:59:56.672963", 0]
// 9: (2) ["2020-06-30T13:00:56.664771", 0]
            let rollPeriod = 1;
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

