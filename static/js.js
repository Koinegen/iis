$(document).ready(function() {

	var toLoad = '/next';

	$('#btn-click').click(function(){
		$('#content').hide('fast',loadContent);

		function loadContent() {
			$('#content').load(toLoad,'',showNewContent)
		}
		function showNewContent() {
			$('#content').show('fast');
		}
	});

});