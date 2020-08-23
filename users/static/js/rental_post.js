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
	
	// House addr Form action and adding HH form
	$('#house_addr').on('submit', function(event){
		event.preventDefault();
		var form = $(this);
		var formData = new FormData(this);
		console.log(formData);
		console.log(form);
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
						'scrollTop': $('#second_div').position().top
					});
					$('#second_div').load(url+' #house_has');
					$('#second_div').find('#ha_id').remove();
					$('#pkhere').attr('id',data.id);

				}	
			},
			error:function(error){
				console.log(error)
				var hh_err = error.responseJSON['house_no'];
				console.log(hh_err)
				if(hh_err){
					console.log('True');
					$(this).find('#hh_no').append("<small class='has-text-danger is-size-7' id='hh_err'>"+hh_err+"</small>");
					$('html, body').animate({
						scrollTop:$('#ha_title_id').offset().top
					})
				}

			}		
		});
	});	

	// HH form section and adding the amenities
	$('#mn-bd').on('click','#house_has_submit', function(event){
		event.preventDefault();
		var form = $(this).closest('form');
		console.log(form, form.serialize());
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
				$(this).parents('#house_has').find('button:hidden').show();
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
				$(this).parents('#amenities').find('button:hidden').show();
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
				$(this).parents('#rules').find('button:hidden').show();
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
				$(this).parents('#preferred_tenenat').find('button:hidden').show();
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
	// prog(){

	// }
});

// Handling the Edit From individual Tiles
$(function(){

	$('#mn-bd').on('click', '#ha-s, #hh-s, #am-s, #rl-s, #pt-s, #ha-sa, #hh-sa, #am-sa, #rl-sa, #pt-sa', function(){

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
				// $(this).parents('#hh_a').find('#hh_lr').prepend("<button id='hh-e' class='level-item button is-small is-secondary'>Edit</button>");	
			},
			error:function(data){
				console.log(data);
			}
		});

	});

	$('#mn-bd').on('click','#ha-e, #hh-e, #am-e, #rl-e, #pt-e', function(event){
		event.preventDefault();
		// console.log('here..?');
		// console.log($(this).parents('.column'));
		$(this).parents('.column').find('input, select, textarea').prop('disabled',false);
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
		console.log('working');
		$('.modal').attr('class','modal is-active');

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
				console.log(data.city);
				// console.log($(this).parents('form').find('#id_city'));
				$(this).parents('form').find('#id_city').val(data.city);
			},
			error:function(error){
				err = error.responseJSON['zipcode'];
				console.log(err.zipcode);
				$(this).parent('.column').append("<small class='has-text-danger is-size-7' id='hh_err'>"+err+"</small>");
				$(this).parents('form').find('#id_city').val('');
				// console.log($(this).parent('.column'));

			}
		})
	});
	

});

$(function(){
	$('#tenet').on('click', function(){
		console.log($('.mapboxgl-ctrl-geocoder--input'));
		// $('.mapboxgl-ctrl-geocoder').focus();
		$('#hm-h-t-div').css('height','12vh');
		$('.mapboxgl-ctrl-geocoder--input').focus();
		$('#srch-bar').show();
		$('#srch-bar').css('height','30vh');
		$('html, body').animate({
			'scrollTop': $('#srch-bar').position().top
		});
		$('#owner').addClass('is-light');
		$('#otner').addClass('is-light')
		$.ajax({
			url:'usr/type',
			type:'POST',
			data:{'user_type':'tenant'},
			context:this,
			dataType:'json',
			success:function(data){
				console.log('success')
			},
			error:function(){
				console.log('failed')
			}
		})
	})

	$('#owner').on('click',function(){
		$.get('sign/', function(data){
			if(data.user == 'not_logged_in'){
				$('#owner').removeClass('is-light');
				$('#srch-bar').hide();
				// console.log('...?')
				// console.log($('#tit-neibo'));
				$('#own-tit-neibo').text('niebo to post your rent ad..!!')
				// $('owner').addClass('is-warning');
				$('#tenet').addClass('is-light');
				$('#own-lgn-mod').attr('class','modal is-active');
			}
		});		
	});
	
});

$(function(){

	$('#first_div').on('click', '.ovr', function(){
		$(this).siblings('.fa').css('transform','scale(0.98)');
		$('#del-mod').attr('class','modal is-active');
		
		var this_c = $(this);

		$('#mn-bd').on('click','#del-img', function(){
			var id = $(this_c).parent('.img-div').find('.img-ad-cls').attr('id');
			console.log('executing',id);
			$.ajax({
				url:'/del_img/'+id+'/',
				type:'DELETE',
				context:this_c,
				success:function(data){
					console.log(data);
					$(this).parent('.img-div').remove();
				},
				error:function(error){
					console.log(error);
				}

			});
		});
	});
});

// .off('click');