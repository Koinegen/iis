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

	$('#btn-yes').click(function (){
		$.post(toLoad, 'yes', function(data){
			$('#content').hide('fast', toHtml);
			$('#content').show("fast");
			function toHtml(){
				$(this).html(data);
			}
			// $('#content').html(data);
			// $('#content').show("fast");
		})
	});

	$('#btn-dont_know').click(function (){
		$.post(toLoad, 'dont_know', function(data){
			$('#content').hide('fast', toHtml);
			$('#content').show("fast");
			function toHtml(){
				$(this).html(data);
			}
			// $('#content').html(data);
			// $('#content').show("fast");
		})
	});

	$('#btn-no').click(function (){
		$.post(toLoad, 'no', function(data){
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