$( document ).ready(function() {

function fetchall(){
    $.ajax({
            url: '/getmessages',
            data: $('form').serialize(),
            type: 'GET',
            success: function(data) {
                console.log(data);
                messages = data;
                $("#messages").empty();

               for (row = 0; row < messages.length; row++) {
                        a_message = messages[row][1]
                        console.log(a_message);
                        $("#messages").append(a_message + "<br>");
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
            url: '/sendmessage',
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