function PopulateCountrySelect () {
	var select = $("#select-countrycode");
	var opt; 
	select.empty();
	$.ajax({
		url: "/api/country/select",
		method: "GET"
	})
	.success(function(data) {
		$.each(data, function(idx, obj) {
			opt = $("<option/>")
				.attr("value", obj["code"])
				.text(obj["name"]);
			select.append(opt);
		});
	})
	.fail(function (error) {
		console.log(error);
	})
	.done(function () {
		if (profile_country) {
			// select the cached country, and trigger population of subdivision
			select.find("option").each(function(idx, obj) {
				if (obj.value == profile_country) {
					$(obj).attr("selected", true);
					select.trigger("change");
				}
			});
		} else {
			select.find("option[value='US']").attr("selected", true);
			select.trigger("change");
		}
	});
}

function BuildSubSelect(country_code) {
	var select = $("#select-subdivision");
	var label = $("#select-sd-label");
	var opt;
	select.empty();
	$.ajax({
		url: "/api/country/subdivision/"+country_code,
		method: "GET"
	})
	.success(function (data) {
		label.text(data["sd_type"]);
		$.each(data["subdivisions"], function(idx, obj) {
			opt = $("<option/>")
				.attr("value", obj["code"])
				.text(obj["name"]);
			select.append(opt);
		});
	})
	.fail(function (error) {
		console.log(error);
	})
	.done(function () {
		if (profile_sub) {
			// select the cached country, and trigger population of subdivision
			select.find("option").each(function(idx, opt) {
				if (opt.value == profile_sub) {
					$(opt).attr("selected", true);
					select.trigger("change");
				}
			});
		}
	});
}

// set the value of a select box
function SetSelects(select_id, val) {
	var select = $("#select-"+select_id);

	if (val === undefined) {
		return;
	}
	select.find("option").each(function(i, opt) {
		if (opt.value === val) {
			$(opt).attr("selected", true);
			select.trigger("change");
		}
	});
} 

$(document).ready(function () {
	SetSelects("role", role);
	PopulateCountrySelect();
	
	// listen for country change
	$("#select-countrycode").on("change", function () {
		BuildSubSelect($("#select-countrycode").val());
	});
});
