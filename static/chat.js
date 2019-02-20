$( document ).ready(function() {
    // alert( "ready!" );
    // console.log("hi from snowy vancouver");
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