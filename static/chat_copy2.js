$( document ).ready(function() {

function fetchall(){
    $.ajax({
            url: '/getchats',
            data: $('form').serialize(),
            type: 'GET',
            success: function(data) {
                console.log(data);
                messages = data;
                $("#messages").empty();

               for (row = 0; row < messages.length; row++) {
                        a_message = messages[row][1]
                        username = messages[row][5]
                        date = messages[row][2]
                        time = messages[row][3]
                        console.log(a_message);
                        $("#messages").append("<b>" + username + "   </b>" + "<i>" + "[" + date + " " + time + "] : </i> "  + a_message + "<br>");
                        // $("#messages").append("<b>" + username + ":   </b>" + a_message + "<br>" + "<i>" + date + " " + time + "</i>" + "<br>");
                }
                setTimeout(fetchall,1000);
            },
            error: function(error) {
                console.log(error);
            }
    });
}

fetchall();


	$("#send").click(function(e) {
		e.preventDefault()
		$.ajax({
            url: '/sendtochatbox',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                // a_message = response;
                // console.log("Testing our chatapp", a_message);
                // $("#themessage").append("\n" + a_message);
            },
            error: function(error) {
                console.log(error);
            }
        });

	});


});