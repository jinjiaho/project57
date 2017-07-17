function downloadCSV(csv, filename) {
    var csvFile;
    var downloadLink;

    // CSV file
    csvFile = new Blob([csv], {type: "text/csv"});

    // Download link
    downloadLink = document.createElement("a");

    // File name
    downloadLink.download = filename;

    // Create a link to the file
    downloadLink.href = window.URL.createObjectURL(csvFile);

    // Hide download link
    downloadLink.style.display = "none";

    // Add the link to DOM
    document.body.appendChild(downloadLink);

    // Click download link
    downloadLink.click();
}
    
function exportReview(category, tableid, filename) {

    var monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    var d = new Date();
    var month = monthNames[d.getMonth()];
    var year = d.getFullYear();
    var csv = [];
    var rows = $(tableid).find("tbody tr:visible");
    var header1 = ["Monthly Review of "+category,"","","","Month: "+month,"Year:"+year]
    var header2 = ["Property: Ascott Raffles Place Singapore"]//Property is hard coded for now
    var header3 = ["","","","","",""];
    var header4 = ["Name","Unit","Unit Price","Initial quantity","In","Value(In)","Out","Value(Out)","Remaining quantity"];    csv.push(header1.join(","));
    csv.push(header2);
    csv.push(header3.join(","));
    csv.push(header4.join(","));

    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll("td, th");

        for (var j = 0; j < cols.length; j++)
            row.push(cols[j].innerText);

        csv.push(row.join(","));
    }

    // Download CSV file
    downloadCSV(csv.join("\n"), filename);

}

function exportLogs(tableid, filename) {

    var monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    var d = new Date();
    var month = monthNames[d.getMonth()];
    var year = d.getFullYear();
    var header1 = ["Logs in current month","","","","","","Month: "+month,"Year:"+year];
    var header2 = ["Property: Ascott Raffles Place Singapore"];//Property is hard coded for now
    var header3 = ["","","","","",""];
    var header4 = ["Date-Time","User","Item","Category","In/Out","Quantity change","Quantity remaining","Location"];
    var csv = [];
    var rows = $(tableid).find("tbody tr:visible");
    csv.push(header1)
    csv.push(header2)
    csv.push(header3.join(","));
    csv.push(header4.join(","));
    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll("td,th");
        
        for (var j = 0; j < cols.length; j++) 
            row.push(cols[j].innerText);
        
        csv.push(row.join(","));        
    }

    // Download CSV file
    downloadCSV(csv.join("\n"), filename);
}