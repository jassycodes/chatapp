$( document ).ready(function() {
	var randomStringData;

	$("#target").click(function() {
		$.get("/hackernews", function(data) {
		  randomStringData = data;
		  console.log("Value of randomStringData inside callback", randomStringData);
		  $("#top_10_titles").append(randomStringData);
		});
	});
});
console.log("Value of randomStringData outside of callback", randomStringData);