var iifetemplate = (function (){

   function privateFunction(){
       console.log("Private Function Called")
    }

        // Public Methods/Data
    return {
        publicFunction1: function(){
            console.log("Public Function 1 Called")
        },
        publicFunction2: function(){
            console.log("Public Function 2 Called")
        }
    }

})();