$(document).ready( function() { 

    $("#btnStart").click(function(){ 
        //make it event lister
        //alert("You have click 9 the Start button...");
    });

    $("#btnCancel").click(function(){ 
        //make it event lister
        //alert("You have click 9 the Cancel button...");
    });

    
    
}); 

var startTime = new Date(); 
let i=0; 


function myTimer(){ 
    var myTime = new Date(2020,1,1,00,00,00,00); 
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
    var outputDateTime = minutes+":"+seconds; 
    document.getElementById("dateTime").innerHTML = outputDateTime;  //d.toLocaleTimeString();

    var outputDate = startTime.toLocaleDateString(); 
    document.getElementById("date").innerHTML = outputDate;
}
var gdata 
function meterValue(){
    var power = [];
    gdata = getData();
    
    var power_value = gdata[i];
    power.push(power_value);
    i++; 

    var power_meter = power + " Watt";
    document.getElementById("powerMeter").innerHTML = power_meter;
  }
