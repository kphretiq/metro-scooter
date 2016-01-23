// anything having to do with creating or updating a password

$(document).ready(function() {
	// password strength listener for bootstrap
	// https://github.com/ablanco/jquery.pwstrength.bootstrap
	$(":password").pwstrength();
	// set bootstrap-validator listeners for various forms
	// http://1000hz.github.io/bootstrap-validator/
	$("#signup-form").validator();
	$("#login-form").validator();
});
