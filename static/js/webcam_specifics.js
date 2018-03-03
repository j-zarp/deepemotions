
Webcam.set({
	width: 320,
	height: 240,
	image_format: 'jpeg',
	jpeg_quality: 90
});
Webcam.attach( '#my_camera' );

document.onkeypress = function(event) {
	if( event.which == 9 ) {
		console.log( event.target.href );
	}

//Si 0, changement entre static et dynamic
    //alert(event.which);
    if (event.which==48){
    	switchForm();
    }
    Submit();
};

function Submit() {
	$("#theForm").submit();
}


function myFunction() {
	if (submitForm==1){ 
		$("#theForm").submit();
	}
}

function switchForm() {
	if (submitForm==1){
		submitForm=0;
		document.getElementById('button').innerHTML='Dynamic mode';
	}
	else{
		submitForm=1;
		document.getElementById('button').innerHTML='Static mode';
	}
}

//Code to handle taking the snapshot and displaying it locally
function take_snapshot() {
	// take snapshot and get image data
	Webcam.snap( function(data_uri) {
		document.getElementById('id_pic').value=data_uri;
	});
}

