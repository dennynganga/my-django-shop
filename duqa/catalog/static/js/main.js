$(document).ready(function(){
	$(".signin").click(function(e){
		e.preventDefault();
        $("fieldset#signin_menu").toggle();
		$(".signin").toggleClass("menu-open");
     });
			
	$("fieldset#signin_menu").mouseup(function(){
		return false
		});
	$(document).mouseup(function(e){
		if($(e.target).parent("a.signin").length==0){
			$(".signin").removeClass("menu-open");
			$("fieldset#signin_menu").hide();
			}
		});			
			
    });
    
$('.slider').tilesSlider({
	auto: true,
	loop: true,
	timer: false,
	thumbs: false,
	slideSpeed: 20000
})

function myCart(){
	$('#popup').bPopup({
	
	});};
	
function commaSeparatePrice(price){
    			while (/(\d+)(\d{3})/.test(price.toString())){
    				price = price.toString().replace(/(\d+)(\d{3})/, '$1' + ',' + '$2');
    			}
    			return price;
    		}

/* AJAX */

function getCookie(name){
	var cookieValue = null;
	if(document.cookie && document.cookie !=''){
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++){
			var cookie = jQuery.trim(cookies[i]);
			if (cookie.substring(0, name.length + 1) == (name + '=')){
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
				}
			}
		}
		return cookieValue;
	}
	
var csrftoken = getCookie('csrftoken');
	
function csrfSafeMethod(method){
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	
function sameOrigin(url){
	var host = document.location.host;
	var protocol = document.location.protocol;
	var sr_origin = '//' + host;
	var origin = protocol + sr_origin;
	return (url == origin || url.slice(0, origin.length + 1) == origin + '/') || (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') || !(/^(\/\/|http:|https:).*/.test(url));
	}
	
			$.ajaxSetup({
				beforeSend: function(xhr, settings){
					if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
						// Send the token to same-origin, relative URLs only.
						// Send the token only if the method warrants CSRF protection
						// Using the CSRFToken value acquired earlier
						xhr.setRequestHeader("X-CSRFToken", csrftoken);
						}
				},
				error: function(xhr, status, error) {   
					alert('An error occurred: ' + error);
				}
			});

