$(function(){
	// CSRF_TOKEN
	function getCookie(name) {
	    let cookieValue = null;
	    if (document.cookie && document.cookie !== '') {
	        const cookies = document.cookie.split(';');
	        for (let i = 0; i < cookies.length; i++) {
	            const cookie = cookies[i].trim();
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) === (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
    	return cookieValue;
	}
	const csrftoken = getCookie('csrftoken')

	function csrfSafeMethod(method) {
	    // these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    }
	}); 

});


$(function(){

	$('#house_has_form, #amenities_form, #rules_form, #pt_form').on('submit', function(event){
		event.preventDefault();
	})

	var tick_icon= '<span class="icon is-medium has-text-success">'
  						        +'<i class="fa fa-lg fa-check-square"></i>'
						        +'</span>';


	// Initialize all input of date type.
	const dates = bulmaCalendar.attach('[class="ip-date"]', {
		'type':'date',
		'minDate': new Date(new Date().getFullYear(), new Date().getMonth(),1),
		'maxDate':new Date(new Date().getFullYear(),11,31),
		'enableYearSwitch':false,
		'startDate': new function(){
			return new Date()
		},
		'disabledDates': new function(){
			var list = [];
			var today = new Date()
			var startDate = new Date(today.getFullYear(), today.getMonth(),1)
			var endDate = new Date(today.getFullYear(), today.getMonth(),today.getDate())
			while(startDate < endDate){
				// console.log(startDate, endDate)
				var relDate = new Date(startDate)
				list.push(relDate);
				startDate.setDate(startDate.getDate()+1)
			} 
			return list
			
		},
		'displayMode':'default',
		'allowSameDayRange':false,


	});

	// To access to bulmaCalendar instance of an element



	// var result;
	// console.log(element, 'noelement');
	// if (ip_element && ot_element) {
		// // bulmaCalendar instance is available as element.bulmaCalendar
		// // console.log(ip_element.bulmaCalendar.date.start);
		
		// var out_date;

		// ip_element.bulmaCalendar.on('select', function(datepicker){
		// 	// console.log(data.onSelectDateTimePicker);
		// 	// inp_date = new Date(datepicker.data.value());
		// 	inp_date = datepicker.data.value();
		// 	// console.log(inp_date.getFullYear());
		// 	// console.log(datepicker.data.value());
		// 	// console.log(Date.parse(datepicker.data.date));
		// });

		// // bulmaCalendar instance is available as element.bulmaCalendar

		// ot_element.bulmaCalendar.on('select', function(datepicker){
		// 	// console.log("Input date",inp_date.getFullYear());
		// 	// console.log(data.onSelectDateTimePicker);
		// 	// out_date = new Date(datepicker.data.value());
		// 	out_date = datepicker.data.value();
		// 	// inp_date;
			

		// });
	// }

	function calc(inp_date, out_date){
		
		const dt1 = Date.UTC(inp_date.getFullYear(), inp_date.getMonth(), inp_date.getDate());
		var out_date = new Date(out_date);
		const dt2 = Date.UTC(out_date.getFullYear(), out_date.getMonth(), out_date.getDate());
		// const dt1 = Date.UTC(inp_date);
		// const dt2 = Date.UTC(out_date);
		// console.log(dt1, dt2);

		diff =  Math.ceil(dt2-dt1);
		// console.log(diff);
		days = Math.floor(diff/(1000*60*60*24));
		return days
	}
	
	// House addr Form action and adding HH form
	$('#house_addr').on('submit', function(event){
		event.preventDefault();
		var form = $(this);
		var formData = new FormData(this);
		// console.log(formData);

		var ip_element = document.querySelector('#id_in_date');
		var ot_element = document.querySelector('#id_out_date');
		var inp_date = ip_element.bulmaCalendar.date.start;
		var out_date = ot_element.bulmaCalendar.date.start;
		// console.log(inp_date, out_date);
		// console.log()

		var result = calc(inp_date, out_date);
			
		var wrng = $('#wrng')
		// console.log(result);
		if(result == 0){
			$('.datetimepicker-dummy-input').css('border','1px solid red');
			if(wrng.length !=1 ){
			$('#avl').append('<h6 id="wrng" class="is-size-7"><span class="has-text-danger">From and To dates are same</span></h6>');
			}
		}
		else{
			if(wrng.length == 1){
				$(wrng).remove();
				$('.datetimepicker-dummy-input').css('border','1px');
			}
			$.ajax({
				url:form.attr('data-url'),
				context:this,
				type:'post',
				data:formData,
				dataType:'json',
				processData: false,
	    		contentType: false,
	    		beforeSend:function(){
	    			$(this).append('<progress id="ha_id" class="progress is-small is-primary" max="100">15%</progress>');
	    		},
	    		complete:function(){
	    			$(this).find('#ha_id').remove();
	    		},
				success:function(data){
					$('#ha_title_id').append(tick_icon);
					$('#house_addr').find('input, textarea, select').prop('disabled',true);
					$('#button_sec').hide();
					$(this).parents('.mn-col').find('button:hidden').show();
					var url = data.url;
					if(data.url){
						$('html, body').animate({
							scrollTop: $('#second_div').position().top
						});
						$('#second_div').load(url+' #house_has');
						$('#second_div').find('#ha_id').remove();
						$('#pkhere').attr('id',data.id);
						$(this).attr('data-url','/update_ad/'+data.id+'/');

					}	
				},
				error:function(error){
					// console.log(error)
					var hh_err = error.responseJSON['house_no'];
					// console.log(hh_err)
					if(hh_err){
						// console.log('True');
						$(this).find('#hh_no').append("<small class='has-text-danger is-size-7' id='hh_err'>"+hh_err+"</small>");
						$('html, body').animate({
							scrollTop:$('#ha_title_id').offset().top
						})
					}
				}		
			});
		}
	});	

	// HH form section and adding the amenities
	$('#mn-bd').on('click','#house_has_submit', function(event){
		event.preventDefault();
		var form = $(this).closest('form');
		// console.log(form, form.serialize());
		var pkhere = $('.mn-col').attr('id');
		// console.log('/hh/'+pkhere)+'/';
		$.ajax({
			url:'/hh'+'/'+pkhere+'/',
			context:this,
			type:'post',
			data:form.serialize(),
			dataType:'json',
			beforeSend:function prog(){
				$('#second_div').append('<progress id="ha_id" class="progress is-small is-primary" max="100">15%</progress>');
			},
			complete: function(){
				$('#second_div').find('#ha_id').remove();
			},
			success:function(data){
				// Hiding the HH submit buttons
				$('#h_has_btn').hide();
				// Adding tick for the HH pane
				$('#hh_btn_tit').append(tick_icon);
				// Disable the HH select fields
				$(this).closest('form').find('input, select').prop('disabled', true);
				$(this).parents('#house_has').find('#hh-e').show();
				var url = data.url;
				// var hh_uri = data.hh_url
				$(this).closest('form').attr('data-url',data.hh_url);
				$('#second_div').append("<div id='amenities'></div>");
				// Load the Amenitite pane
				$('#second_div').find('#amenities').load(url+' #amenities', function(){
					$('#second_div').find('#amenities').replaceWith($(this).contents());
				});
			},
			error:function(data){

			}

		})

	});
	// Amenities form and adding the Rules form
	$('#mn-bd').on('click','#am_as_submit', function(event){
		event.preventDefault();
		var form = $(this).closest('form');
		// console.log(form, form.serialize());
		var pkhere = $('.mn-col').attr('id');
		// console.log('/hh/'+pkhere)+'/';
		$.ajax({
			url:'/sa'+'/'+pkhere+'/',
			context:this,
			type:'post',
			data:form.serialize(),
			dataType:'json',
			beforeSend:function prog(){
				$('#third_div').append('<progress id="ap_id" class="progress is-small is-primary" max="100">15%</progress>');
			},
			complete: function(){
				$('#third_div').find('#ap_id').remove();
			},
			success:function(data){
				// Hiding the HH submit buttons
				$('#a_as_btn').hide();
				// Adding tick for the HH pane
				$('#amen-tit-id').append(tick_icon);
				// Disable the HH select fields
				$(this).closest('form').find('input, select').prop('disabled', true);
				$(this).parents('#amenities').find('#am-e').show();
				var url = data.url;
				// var a_uri = data.a_url;
				$(this).closest('form').attr('data-url',data.a_url);
				// $('#third_div').append("<div id='amenities'></div>");
				// Load the Amenitite pane
				$('#third_div').load(url+' #rules');
				$('html, body').animate({
						'scrollTop': $('#third_div').position().top
				});
			},
			error:function(data){

			}

		})

	});
	// Rules form and adding the PT form
	$('#mn-bd').on('click','#rl_has_submit', function(event){
		event.preventDefault();
		var form = $(this).closest('form');
		// console.log(form, form.serialize());
		var pkhere = $('.mn-col').attr('id');
		// console.log('/hh/'+pkhere)+'/';
		$.ajax({
			url:'/sr'+'/'+pkhere+'/',
			context:this,
			type:'post',
			data:form.serialize(),
			dataType:'json',
			beforeSend:function prog(){
				$('#third_div').append('<progress id="rp_id" class="progress is-small is-primary" max="100">15%</progress>');
			},
			complete: function(){
				$('#third_div').find('#rp_id').remove();
			},
			success:function(data){
				// Hiding the HH submit buttons
				$('#rules_button').hide();
				// Adding tick for the HH pane
				$('#rul-titl').append(tick_icon);
				// Disable the HH select fields
				$(this).closest('form').find('input, select').prop('disabled', true);
				$(this).parents('#rules').find('#rl-e').show();
				var url = data.url;
				// var r_uri = data.r_url;
				$(this).closest('form').attr('data-url',data.r_url);
				$('#third_div').append("<div id='preferred_tenenat'></div>");
				// Load the Amenitite pane
				$('#third_div').find('#preferred_tenenat').load(url+' #preferred_tenenat', function(){
					$('#third_div').find('#preferred_tenenat').replaceWith($(this).contents());
					
				});
			},
			error:function(data){

			}

		})

	});

	//  PT form and handling the final div
	$('#mn-bd').on('click','#pt_has_submit', function(event){
		event.preventDefault();
		var form = $(this).closest('form');
		// console.log(form, form.serialize());
		var pkhere = $('.mn-col').attr('id');
		// console.log('/hh/'+pkhere)+'/';
		$.ajax({
			url:'/spt'+'/'+pkhere+'/',
			context:this,
			type:'post',
			data:form.serialize(),
			dataType:'json',
			beforeSend:function prog(){
				$('#fourth_div').append('<progress id="fp_id" class="progress is-small is-primary" max="100">15%</progress>');
			},
			complete: function(){
				$('#fourth_div').find('#fp_id').remove();
			},
			success:function(data){
				// Hiding the HH submit buttons
				$('#pt_button').hide();
				// Adding tick for the HH pane
				$('#pt-titl').append(tick_icon);
				// Disable the HH select fields
				$(this).closest('form').find('input, select').prop('disabled', true);
				$(this).parents('#preferred_tenenat').find('#pt-e').show();
				var url = data.url;
				var erul = data.e_url;
				var durl = data.d_url;
				var hurl = data.h_url;
				// var pt_uri = data.pt_url;
				$(this).closest('form').attr('data-url',data.pt_url);
				$('#md-del').attr('href',durl);
				// $('#fourth_div').append("<div id='preferred_tenenat'></div>");
				// Load the Amenitite pane
				// console.log(hurl, durl);
				$('#fourth_div').load(url+' #final_sec', function(){
					// console.log(hurl, durl);
					$(this).find('#imok_btn').attr('href',hurl);
					$(this).find('#dl_btn').attr('href',durl);
					$('#md-del').attr('href',durl);
					
				})

				$('html, body').animate({
						'scrollTop': $('#fourth_div').position().top
				});
				// , function(){
					// $('#third_div').find('#preferred_tenenat').replaceWith($(this).contents());
				// });
			},
			error:function(data){

			}

		})

	});

	// Handling the Edit From individual Tiles
	$('#mn-bd').on('click', '#ha-s, #hh-s, #am-s, #rl-s, #pt-s, #ha-sa, #hh-sa, #am-sa, #rl-sa, #pt-sa', function(){

		var ip_element = document.querySelector('#id_in_date');
		var ot_element = document.querySelector('#id_out_date');
		var inp_date = ip_element.bulmaCalendar.date.start;
		var out_date = ot_element.bulmaCalendar.date.start;
		// console.log(inp_date, out_date);
		// console.log('-------------------------')

		var result = calc(inp_date, out_date);
		// console.log(result)
		var wrng = $('#wrng')
		// console.log(result);
		if(result == 0){
			$('.datetimepicker-dummy-input').css('border','1px solid red');
			if(wrng.length !=1 ){
			$('#avl').append('<h6 id="wrng" class="is-size-7"><span class="has-text-danger">From and To dates are same</span></h6>');
			}
		}else{
			// console.log('-------------------------')
			// var data = $('#house_has_form');
			var data = $(this).parents('.column').find('form');
			var fD = new FormData(data[0]);
			$.ajax({
				url: data.attr('data-url'),
				context:this,
				type:'post',
				data: fD,
				dataType:'json',
				processData: false,
	    		contentType: false,
				success:function(data){
					$(this).parents('.column').find('input, select, textarea').prop('disabled', true);
					$(this).parent().find('button:hidden').show();
					if($('#wrng').length == 1){$('#wrng').remove();$('.datetimepicker-dummy-input').css('border','1px');}
					$(this).hide();
					// $(this).parents('#hh_a').find('#hh_lr').prepend("<button id='hh-e' class='level-item button is-small is-secondary'>Edit</button>");	
				},
				error:function(data){
					console.log(data);
				}
			});
		}

	});

	$('#mn-bd').on('click','#ha-e, #hh-e, #am-e, #rl-e, #pt-e', function(event){
		event.preventDefault();
		$(this).parents('.column').find('input, select, textarea').prop('disabled',false);
		$(this).parent().find("button:hidden").show();
		$(this).hide();
	});

})

$(function(){

	$('#mn-bd').on('click','#lgn',function(event){
		event.preventDefault();
		$('#lgn-mod').attr('class','modal is-active');

	})

	$('.container').on('click','#dl_btn, .del-tmp',function(event){
		event.preventDefault();
		// console.log('working');
		$('#del-cncl').attr('class','modal is-active');

	});

	$('#md-cncl, .modal-close').on('click',function(event){
		event.preventDefault();
		$('.modal').attr('class','modal');
		if($('#tenet')){
			$('#tenet').removeClass('is-light');
		}
	});

	// $('#mc-id').on('blur')

	$('#lgn-mod, #del-cncl, #del-mod').mouseup(function(e){
		// console.log('heree..');
		var mod = $('#mc-id');
		if (!mod.is(e.target) && mod.has(e.target).length === 0){
			// console.log('clicked')
			// $('.modal').hide();
			$('.modal').attr('class','modal');
			$('#tenet').removeClass('is-light');
			// mod.off('click');
		}
	});

	// $('#bdy-ma').on('change','#id_zipcode', function(){
	// 	var err = $(this).parent().find('#hh_err')
	// 	// $(this).parents('form').find('#id_city').val('');
	// 	if(err){
	// 		$(err).remove();
	// 	}
	// })

	// $('#bdy-ma').on('keyup','#id_zipcode, #id_longitude, #id_latitude', function(){
	// 	if($(this).isisNumeric())
	// })
	$('#mn-bd').on('blur','#id_zipcode', function(){
		var dat = $('#id_zipcode').val();
		var err = $(this).parent().find('#hh_err')
		if(err){
			$(err).remove();
		}
		// console.log(dat);
		$.ajax({
			url:'/zp/',
			context:this,
			data:{'zipcode':dat},
			type:'GET',
			dataType:'json',
			success:function(data){
				// console.log(data.city);
				// console.log($(this).parents('form').find('#id_city'));
				$(this).parents('form').find('#id_city').val(data.city);
			},
			error:function(error){
				err = error.responseJSON['zipcode'];
				// console.log(err.zipcode);
				$(this).parent('.column').append("<small class='has-text-danger is-size-7' id='hh_err'>"+err+"</small>");
				$(this).parents('form').find('#id_city').val('');
				// console.log($(this).parent('.column'));

			}
		})
	});
	

});

$(function(){
	$('#tenet').on('click', function(){
		// console.log($('.mapboxgl-ctrl-geocoder--input'));
		// $('.mapboxgl-ctrl-geocoder').focus();
		$('#hm-h-t-div').css('height','12vh');
		$('.mapboxgl-ctrl-geocoder--input').focus();
		$('#srch-bar').show();
		$('#srch-bar').css('height','30vh');
		$('html, body').animate({
			'scrollTop': $('#srch-bar').position().top
		});
		$('#owner').addClass('is-light');
		$('#otner').addClass('is-light');
		$('#tenet').removeClass('is-light');
		$('#tenet').addClass('is-warning');
		var dd_tt = $('#dd-tt');
		var dd_ll = $('#dd-ll');
		// console.log(dd_tt.length != 1);
		if(dd_tt.length != 1){
			// console.log('if');
			$.ajax({
				url:'/usr/type/',
				type:'POST',
				data:{'user_type':'tenant'},
				context:this,
				dataType:'json',
				success:function(data){
					// console.log($('#dd-ll'));
					if($('#dd-ll').length == 1)$('#dd-ll').remove();
					$('.nb-end').prepend('<div id="dd-tt" class="navbar-item has-dropdown is-hoverable"><a id="tt" class="navbar-link">'+data.user_type+'</a><div class="navbar-dropdown"><a id="ll" class="navbar-item">LandLord</a></div></div>');
				},
				error:function(error){
					console.log('nl')
				}
			})
		}else if(dd_ll.length == 1){
			// console.log('elseif');
			// console.log(dd_ll);
			$.ajax({
				url:'/usr/type/',
				type:'POST',
				data:{'user_type':'tenant'},
				context:this,
				dataType:'json',
				success:function(data){
					// console.log($('#dd-ll'));
					if($('#dd-ll').length == 1)$('#dd-ll').remove();
					$('.nb-end').prepend('<div id="dd-tt" class="navbar-item has-dropdown is-hoverable"><a id="tt" class="navbar-link">'+data.user_type+'</a><div class="navbar-dropdown"><a id="ll" class="navbar-item">LandLord</a></div></div>');
				},
				error:function(error){
					console.log('nl')
				}
			});
		}
	})

	$('#owner').on('click',function(){
		$.get('sign/', function(data){
			if(data.user == 'not_logged_in'){
				$('#owner').removeClass('is-light');
				// console.log('...?')
				// console.log($('#tit-neibo'));
				$('#own-tit-neibo').text('niebo to post your rent ad..!!')
				// $('owner').addClass('is-warning');
				$('#tenet').addClass('is-light');
				$('#own-lgn-mod').attr('class','modal is-active');
			}
		});		
	});

	$('#navbar-shadow').on('click', '#tt, #ll', function(event){
		event.preventDefault();
		var id_val = $(this).attr('id');
		if(id_val == 'tt'){
			var	data_val = {'user_type':'tenant'}
		}else if(id_val == 'll'){
			var data_val = {'user_type':'owner'}	
		}	
		var path = window.location.pathname;
		console.log(path);
		if(path != "/post_ad/" ){
			$.ajax({
				url:'/usr/type/',
				type:'POST',
				data:data_val,
				context:this,
				dataType:'json',
				success:function(data){
					// console.log($('#navbar-shadow').find('#dd-ll'));
					// console.log($('#dd-ll'));
					// console.log($('#dd-tt'));
					if(data.user_type == 'Tenant'){
						if($('#dd-ll').length == 1){
							// console.log('Found dd-ll in the tenet', $('#dd-ll').length == 1);
							$('#dd-ll').remove();
						}
						if($('#dd-tt').length != 1){
							$('.nb-end').prepend('<div id="dd-tt" class="navbar-item has-dropdown is-hoverable"><a class="navbar-link">'+data.user_type+'</a><div class="navbar-dropdown"><a id="ll" class="navbar-item">LandLord</a></div></div>');
							$('#tenet').removeClass('is-light');
							$('#tenet').addClass('is-warning');
							$('#otner').addClass('is-light');
							$('#owner').addClass('is-light');
						}

					}else if(data.user_type == 'Owner'){
						if($('#dd-tt').length == 1){
							// console.log('Found dd-tt in owner', $('#dd-tt').length == 1);
							$('#dd-tt').remove();
						}
						if($('#dd-ll').length != 1){
							$('.nb-end').prepend('<div id="dd-ll" class="navbar-item has-dropdown is-hoverable"><a class="navbar-link">LandLord</a><div class="navbar-dropdown"><a id="tt" class="navbar-item">Tenant</a></div></div>');
							if($('#srch-bar'))$('#srch-bar').hide();
							$('#hm-h-t-div').css('height','40vh');
							$('#onwer').removeClass('is-light');
							$('#onwer').addClass('is-warning');
							$('#otner').removeClass('is-light');
							$('#otner').addClass('is-warning');
							$('#tenet').addClass('is-light');
						}
					}			
				},
				error:function(){
					console.log('failed')
				}
			});
		}
	});
	
});

$(function(){

	$('#first_div').on('click', '.ovr', function(){
		$(this).siblings('.fa').css('transform','scale(0.98)');
		$('#del-mod').attr('class','modal is-active');
		
		var this_c = $(this);

		$('#mn-bd').on('click','#del-img', function(){
			var id = $(this_c).parent('.img-div').find('.img-ad-cls').attr('id');
			// console.log('executing',id);
			$.ajax({
				url:'/del_img/'+id+'/',
				type:'DELETE',
				context:this_c,
				success:function(data){
					// console.log(data);
					$(this).parent('.img-div').remove();
				},
				error:function(error){
					console.log(error);
				}

			});
		});
	});
});


$(function(){
	$('.hurs').on('mouseenter', function(){
		if($(this).find('.incp').length == 1){
			$(this).find('.del-ovr').find('.left').append('<a href="" class="viw button">Edit <i class="fa fa-edit fa-1x" aria-hidden="true"></i></a>')	
		}else{
			$(this).find('.del-ovr').find('.left').append('<a href="" class="viw button">View <i class="fa fa-eye fa-1x" aria-hidden="true"></i></a>')
		}
		
		$(this).find('.del-ovr').find('.right').append('<button class="del button">Delete <i class="fa fa-trash-alt fa-1x" aria-hidden="true"></i></button>');
		// $(this).find('.del-ovr').css({'background-color':'#fffafa','opacity':'0.6'});
		// console.log($(this).find('.ovr'));
		// $(this).closest('.ovr').css(styles);
	}).on('mouseleave', function(){
		// console.log($(this).closest('.ovr'));
		// $(this).find('.del-ovr').css({'background-color':'none'});
		$(this).find('.del-ovr').find('.left').empty();
		$(this).find('.del-ovr').find('.right').empty();
	});

	$('.del-ovr').on('mouseenter',function(){
		// console.log($(this));
		$(this).attr('title','Delete Ad');
		$(this).css('opacity',1);
	});

	$('.hurs').on('click','.del', function(){
		// console.log('here');
		$('#del-cncl').attr('class','modal is-active');
		var id = $(this).parents('.del-ovr').attr('id');
		$('#del-cncl').find('#md-del').attr('href','/dlw/'+id+'/');
	})

	$('.hurs').on('click','.viw',function(){
		var id = $(this).parents('.del-ovr').attr('id');
		if($(this).parents('.incp').length == 1){
			$(this).attr('href','/edw/'+id+'/');
		}else{
			$(this).attr('href','/hd/'+id+'/');
		}
		
	})
	

});

// .off('click');