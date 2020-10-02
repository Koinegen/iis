$(document).ready(function() {

	var toLoad = '/next';

	$('#btn-click').click(function(){
		$.get(toLoad, function(data){
			$('#content').hide('fast', toHtml);
			$('#content').show("fast");
			function toHtml(){
				$(this).html(data);
			}
			// $('#content').html(data);
			// $('#content').show("fast");
		})
	});

	// var toLoad = '/next';
	//
	// $('#btn-click').click(function(){
	// 	$('#content').hide('fast',loadContent);
	//
	// 	function loadContent() {
	// 		$('#content').load(toLoad,'',showNewContent)
	// 	}
	// 	function showNewContent() {
	// 		$('#content').show('fast');
	// 	}
	// });

});