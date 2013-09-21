
function show_write_form()
{
	document.getElementById("write_form").style.display = 'inline';
}


$('document').ready(function(){
    var height = $('#head').height();
    height = height + 'px';

    var footer_h = $('#footer').height();
    var footer_t = $('#footer').offset().top;
    var g = document.body.clientHeight;
    if(g > footer_t + footer_h)
    {
        var tp = g  - footer_h - footer_t;
        $('#footer').css('margin-top',tp);
    }
});
