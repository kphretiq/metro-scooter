// root-only javascript

$(document).ready(function() {
	// form for initializing database and/or root user
	$("#init-root-form").validator().on("submit", function(evt) {
		if (evt.isDefaultPrevented()) {
			return false;
		} else {
			// clean up validator
			$("#init-form").validator("destroy");
			$("#init-form").submit();
		}
	});
});
