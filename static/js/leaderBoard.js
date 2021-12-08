window.onload = function(){
    var todaydate = new Date();
    var dd = todaydate.getDate();
    var mm = todaydate.getMonth() + 1; //January is 0!
    var yyyy = todaydate.getFullYear();

    console.log("hii");
    if (dd < 10) {
    dd = '0' + dd;
    }

    if (mm < 10) {
    mm = '0' + mm;
    } 
        
    var today = yyyy + '-' + mm + '-' + dd;
    document.getElementById("endDate").setAttribute("max", today);

    var past30 = new Date(new Date().setDate(todaydate.getDate() - 30));
    dd =  past30.getDate();
    mm = past30.getMonth() + 1; //January is 0!
    yyyy = past30.getFullYear();

    if (dd < 10) {
    dd = '0' + dd;
    }

    if (mm < 10) {
    mm = '0' + mm;
    } 
        
    past30 = yyyy + '-' + mm + '-' + dd;
    document.getElementById("startDate").setAttribute("min", past30);
    document.getElementById("endDate").setAttribute("min", past30);

    var yesterday = new Date(new Date().setDate(todaydate.getDate() - 1));
    dd =  yesterday.getDate();
    mm = yesterday.getMonth() + 1; //January is 0!
    yyyy = yesterday.getFullYear();

    if (dd < 10) {
    dd = '0' + dd;
    }

    if (mm < 10) {
    mm = '0' + mm;
    } 
        
    yesterday = yyyy + '-' + mm + '-' + dd;
    document.getElementById("startDate").setAttribute("max", yesterday);
}

