$(document).ready( function() { 

    $("#btnStart").click(function(){ 
        //make it event lister
        //alert("You have click 9 the Start button...");
    });

    $("#btnCancel").click(function(){ 
        //make it event lister
        //alert("You have click 9 the Cancel button...");
    });

    setInterval(function(){myTimer()},1000);
    
}); 

var startTime = new Date(); 

function myTimer(){ 
    var myTime = new Date(2020,1,1,12,00,00,00); 
    var diff = new Date() - startTime; 

    myTime.setMilliseconds(myTime.getMilliseconds()+ diff); 

    var hours=myTime.getHours();
    var minutes=myTime.getMinutes();
    var seconds=myTime.getSeconds();
    
    if(minutes < 10){ 
        minutes="0" + minutes; 
    }
    if(seconds < 10) { 
        seconds="0" + seconds; 
    }
    var outputDateTime = hours+":"+minutes+":"+seconds; 
    document.getElementById("dateTime").innerHTML = outputDateTime;  //d.toLocaleTimeString();

    var outputDate = startTime.toLocaleDateString(); 
    document.getElementById("date").innerHTML = outputDate;
}