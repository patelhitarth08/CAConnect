function maxHeight() {
	var maxHeight = 0;
	$('.announcebox').each(function () {
		maxHeight = Math.max(maxHeight, $(this).outerHeight());
	});
	console.log(maxHeight);
	$('.newsbox').height(maxHeight);
}
(function ($) {
	/*=============================================================================================*/
	/* Ready Function START Here*/
	$(document).ready(function () {
		'use strict';
		$('select:not(.select-multiple)').niceSelect();

		$('.form_row.password .icon').on('click', function (e) {
			$(this).parent().toggleClass('show');
		});
		$("#newsContent").mCustomScrollbar({ theme: "dark" });

		//newbox max-height
		maxHeight();
	});

	/*=============================================================================================*/
	// ham barger menu
	$(".ham_menubtn a").click(function () {
		$("body").toggleClass("open-sidebar");
	});
	// ham barger menu
	/*=============================================================================================*/


	/*=============================================================================================*/
	//Search-toggle
	$(".mobile_src_btn").click(function () {
		$("header").toggleClass("mobile-search");
	});
	//Search-toggle
	/*=============================================================================================*/

	/* Ready Function END Here*/
	/*=============================================================================================*/
	$(window).on('resize', function () {
		maxHeight();
	});
	$(window).on('load', function () {
		maxHeight();
	});

})(jQuery);


/*=============================================================================================*/
// announcement-page
jQuery(".add_btn a").click(function () {
	jQuery('#add-announcement').modal('show')
});


jQuery(".ann-main-top__dropdown > a").click(function () {
	jQuery(".ann-main-top__dropdown_box").toggleClass("show");
});
// announcement-page
/*=============================================================================================*/




/*=============================================================================================*/
// clint-datails-page
jQuery(".filter_right_list.delete_file a").click(function () {
	jQuery('#delete-pop').modal('show')
});
// clint-datails-page
/*=============================================================================================*/



/*=============================================================================================*/
// Inquire-list
jQuery(document).ready(function () {
	var groupColumn = 2;
	var table = jQuery("#personal_files").DataTable({
		//columnDefs: [{ visible: false, targets: groupColumn }],
		pagingType: "numbers",
		order: [[groupColumn, "asc"]],
		displayLength: 10,
		language: {
			paginate: {
				next: "", // or '→'
				previous: "", // or '←'
			},
		},
		responsive: true,
		//"lengthMenu": [ 10, 15, 20, 25 ],
		//searching: false,
		dom: '<"bottom"f>rt<"bottom_datatable"lp><"clear">',

		columnDefs: [
			{
				//'targets': [2,3,5,6], /* table column index */
				orderable: false,
				bSort: false /* here set the true or false */,
				visible: false,
				targets: groupColumn,
			},
		],
		drawCallback: function (settings) {
			var api = this.api();
			var rows = api.rows({ page: "current" }).nodes();
			var last = null;

			api
				.column(groupColumn, { page: "current" })
				.data()
				.each(function (group, i) {
					if (last !== group) {
						$(rows)
							.eq(i)
							.before(
								'<tr class="group"><td colspan="6">' + group + "</td></tr>"
							);

						last = group;
					}
				});
		},
		language: {
			searchPlaceholder: "Search here...",
			search: "",
		},
	});
	// Order by the grouping
	jQuery("#personal_files tbody").on("click", "tr.group", function () {
		var currentOrder = table.order()[0];
		if (currentOrder[0] === groupColumn && currentOrder[1] === "asc") {
			table.order([groupColumn, "desc"]).draw();
		} else {
			table.order([groupColumn, "asc"]).draw();
		}
	});
});

jQuery(document).ready(function () {
	var table2 = jQuery("#general_files").DataTable({
		pagingType: "numbers",
		displayLength: 10,
		language: {
			paginate: {
				next: "", // or '→'
				previous: "", // or '←'
			},
		},
		responsive: true,
		dom: '<"bottom"f>rt<"bottom_datatable"lp><"clear">',
		language: {
			searchPlaceholder: "Search here...",
			search: "",
		},
	});
});
// Inquire-list
/*=============================================================================================*/


/*=============================================================================================*/
// admin-edit

jQuery(".admin-edit-form .form-input .icon").click(function () {
	var paswd = jQuery(this).parent().find('input');
	if (paswd.attr("type") == "password") {
		paswd.attr("type", "text");
		jQuery(this).parent().addClass('show_password');
		console.log('test');
	}
	else {
		paswd.attr("type", "password");
		jQuery(this).parent().removeClass('show_password');
		console.log('test');
	}
});


  // admin-edit
/*=============================================================================================*/