var startTime = new Date(); 
let timeCounter=0; 

var gtime
function time(){
    var clock = [];
    gtime = getTime();
    
    
    var clock_value = gtime[timeCounter];
    clock.push(clock_value);
    timeCounter++;

    var display_clock = clock;
    document.getElementById("dateTime").innerHTML = display_clock;

    var outputDate = startTime.toLocaleDateString(); 
    document.getElementById("date").innerHTML = outputDate;
}

var gdata; 
var meterCounter=0; 
function meterValue(){
    var power = [];
    gdata = getData();
    
    var power_value = gdata[meterCounter];
    power.push(power_value);
    meterCounter++; 

    var power_meter = power + " Watt";
    document.getElementById("powerMeter").innerHTML = power_meter;
}

var sub; 
var subcounter=0; 
function setSubmeterStatus(){ 
    
    sub=getSubmeterV(); 
    var subValue = sub[subcounter]; 
    var s1 = subValue[0]; 
    var s2 = subValue[1]; 
    var s3 = subValue[2]; 
    
    switch(s1){ 
        case 1: 
            document.getElementById("status_microwave").style.backgroundColor= "green";
            break; 
        case 0: 
            document.getElementById("status_microwave").style.backgroundColor= "red";
            break; 
        default: 
            break; 
    }

    switch(s2){ 
        case 1: 
            document.getElementById("status_washing").style.backgroundColor= "green";
            break; 
        case 0: 
            document.getElementById("status_washing").style.backgroundColor= "red";
            break; 
        default: 
            break; 
    }

    switch(s3){ 
        case 1: 
            document.getElementById("status_aircon").style.backgroundColor= "green";
            break; 
        case 0: 
            document.getElementById("status_aircon").style.backgroundColor= "red";
            break; 
        default: 
            break; 
    }

    subcounter++; 
}

var intervalGraph, intervalTime, intervalMeter, intervalSubMeter;

function stopInterval(){ 
    clearInterval(intervalGraph); 
    clearInterval(intervalTime); 
    clearInterval(intervalMeter); 
    clearInterval(intervalSubMeter); 

  }

