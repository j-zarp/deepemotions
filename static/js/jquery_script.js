var submitForm=0;
$(document).ready(function() {

	$('.vertical .progress-fill span').each(function(){
		var percent = $(this).html();
		var pTop = 100 - ( percent.slice(0, percent.length - 1) ) + "%";
		$(this).parent().css({
			'height' : percent,
			'top' : pTop
		});
	});


	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
    			// Does this cookie string begin with the name we want?
    			if (cookie.substring(0, name.length + 1) == (name + '=')) {
    				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
    				break;
    			}
    		}
    	}
    	return cookieValue;
    }
    
    var csrftoken = getCookie('csrftoken');
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


	$("#id_pic").change(function () {
		console.log( $(this).val() );
	});

	$("#theForm").submit(function(event){
		take_snapshot();
		event.preventDefault();
		$.ajax({
			type:"POST",
			url:"",
			data: {
                'url': $('#id_pic').val(), // from form
                'img': $('#id_image_data').val()
            },
            success: function(data) {
            	$("#t_pic2").attr('src', "static/temp2.jpeg" + '?' + new Date().getTime());
            	document.getElementById("id_emotion").innerHTML=data["label"];

            	document.getElementById("happy").innerHTML= (data["prob"][2]*100).toFixed(1) + '%';

            	document.getElementById("sad").innerHTML= (data["prob"][3]*100).toFixed(1) + '%';

            	document.getElementById("angry").innerHTML= (data["prob"][0]*100).toFixed(1) + '%';

            	document.getElementById("neutral").innerHTML= (data["prob"][5]*100).toFixed(1) + '%';

            	document.getElementById("surprised").innerHTML= (data["prob"][4]*100).toFixed(1) + '%';

            	document.getElementById("scared").innerHTML= (data["prob"][1]*100).toFixed(1) + '%';

            	myFunction();
            	$('.vertical .progress-fill span').each(function(){
            		var percent = $(this).html();

            		var pTop = 100 - ( percent.slice(0, percent.length - 1) ) + "%";
            		$(this).parent().css({
            			'height' : percent,
            			'top' : pTop
            		});
            	});

            	document.getElementById('id_image_data').value=document.documentElement.innerHTML;
            }
        });
		return false;
	});

});
