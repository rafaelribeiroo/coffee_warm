$(document).ready(
		function() {
			$('#search').keyup(
					function() {
						$.ajax({
							type : "POST",
							url : "/buscar/",
							data : {
								'search_text' : $('#search').val(),
								'csrfmiddlewaretoken' : $(
										"input[name=csrfmiddlewaretoken]")
								.val()
							},
							success : searchSuccess,
							dataType : 'html'
						});
					});
			$('#search').val("Search...").addClass("empty");
			$('#searchbox').val('').addClass("empty");
			$('#search').focus(function() {
				// If the value is equal to "Search..."
				if ($(this).val() == "Search...") {
					// remove all the text and the class of .empty
					$(this).val("").removeClass("empty");
					$('#searchbox').show();
				}

			});
			$("#search").blur(function() {
				// If the input field is empty
				if ($(this).val() == "") {
					// Add the text "Search..." and a class of .empty
					$(this).val("Search...").addClass("empty");
//					Unbinds the keylistener 
					$('#searchbox').hide();
				}

			});
			
		});



function searchSuccess(data, textStatus, jqXHR) {
	$('#searchbox').html(data);
	
}