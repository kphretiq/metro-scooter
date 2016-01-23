
function upload_file(url) {
	console.log(url);
	$.ajax({
		url: url,
		method: "PUT"
	})
	.success(function(data) {
		console.log(data);
	})
	.fail(function(error) {
		console.log(error);
	});
}

function get_signed_request(file) {
	$.ajax({
		url: "/api/sign_s3/" + file.name,
		method: "GET"
	})
	.success(function(data) {
		console.log(data);
		//upload_file(data.url);
	})
	.fail(function(error) {
		console.log(error);
	});
}


$(document).ready(function() {
	$("#input-file-new").on("change", function (evt) {
		var file = $("#input-file-new").prop("files")[0];
		var tmppath = URL.createObjectURL(evt.target.files[0]);
		console.log(tmppath);
		console.log(file)
		//get_signed_request(file);
	});
});
