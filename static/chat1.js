$( document ).ready(function() {
    // alert( "ready!" );
    // console.log("hi from snowy vancouver");

     // $.get("/getmessages", function(data) {
     //   // randomStringData = data;
     //   // console.log("Value of randomStringData inside callback", randomStringData);
     //   // $("#top_10_titles").append(randomStringData);
     //    messages = data


     //    // messages{
     //    //     1: "mssages"

     //    // }

     //   for (row = 0; row < messages.length; row++) {
     //        // for (col = 0; col < messages[row].length; col++) {
     //        //     console.log("row: ");
     //        //     console.log(row);
     //        //     console.log("col: ");
     //        //     console.log(col);
     //        //     console.log(messages[row][col]);
     //            a_message = messages[row][1]
     //            console.log(a_message);
     //            $("#messages").append(a_message + "<br>");
     //        // }  
     //    }
     // });


function fetchall(){
    $.get('/getmessages', function(data) {
        console.log(data);
        messages = data;

        $("#messages").empty();

       for (row = 0; row < messages.length; row++) {
                a_message = messages[row][1]
                console.log(a_message);
                $("#messages").append(a_message + "<br>");
        }
        setTimeout(fetchall,1000);
    });
}

fetchall();

// function doPoll(){
//     $.post('ajax/test.html', function(data) {
//         alert(data);  // process results here
//         setTimeout(doPoll,5000);
//     });
// }


	$("#send").click(function(e) {
		e.preventDefault()
		$.ajax({
            url: '/sendmessage',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                a_message = response;
                console.log("Testing our chatapp", a_message);
                $("#themessage").append("\n" + a_message);
            },
            error: function(error) {
                console.log(error);
            }
        });

	});








});