$(document).ready(function () {
	$('#start').click(function () {
		$.get("next", function(data){
    		//$.innerHTML = $.parseHTML(data);
			$("#displayMessage").html(data);
    		//alert(data);
		});

	});

});
