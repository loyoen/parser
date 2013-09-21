var editor;
KindEditor.ready(function(K) {
	editor = K.create('textarea[name="content"]', {
		resizeType : 1,
		allowPreviewEmoticons : false,
		allowImageUpload : true,
        uploadJson:'/upload_blog_pic/',
		items : [
			'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold', 'italic', 'underline',
			'removeformat', '|', 'justifyleft', 'justifycenter', 'justifyright', 'insertorderedlist',
			'insertunorderedlist', 'lineheight','image', 'emoticons', 'link','|']	
	});
    editor.html('');
    /*
    var show_content = "title: <textarea value = 'nihao' id = 'input_bu'>sf</textarea>";
    editor.html(show_content + "<hr><br/>");
    editor.sync();
    alert(document.getElementById('content').value);
    */
});
$(document).ready(function(){
	$(".corner_4").corner("4px");

});
var dialog;
function create(options){
    options = $.extend({title:'wuluostudio'}, options || {})
    dialog = new Boxy($('#write_form'), options);
}
function st(){
	//alert('niha');
}
//change profile
function change_profile()
{
    var en = new Array("hobby","skill","sexy","major","grade");
    var ch = new Array("爱好","专长","性别","专业","年级");
    var i = 0;
    for(i = 0; i < 5;i ++)
    {
        var show_content = "";
        var value = $('#'+en[i]+'_x').text();
        show_content += ch[i] + ":" + "<input type='text' id='" + en[i] +"_y' style='width:40%;height:15px;borer:0px;background-color:#eeeeff;font-size:10px;' value ="+value+" ><br />";
        //#alert(show_content);
        $('#'+en[i]).html(show_content);
    //alert($('#hobby_x').text());
    }
    $('#save_link').css('display','inline');
}
//save change in back-end
function save_to_backend(back_value)
{
    var i = 0;
    $('<div>').load('/change_profile/',
        {'hobby':back_value[0],
        'skill':back_value[1],
        'sexy':back_value[2],
        'major':back_value[3],
        'grade':back_value[4]},
         function(){alert('succes!');}
    );
}
//save change in front-end
function save_change()
{
    var en = new Array("hobby","skill","sexy","major","grade");
    var ch = new Array("爱好","专长","性别","专业","年级");
    var i = 0;
    var back_value = new Array(5);
    for(i = 0;i < 5;i ++)
    {
        var show_content = "";
        var value = $('#'+en[i]+'_y').attr("value");
        back_value[i] = value; 
        show_content += ch[i] + ": " + "<span id = '" + en[i] + "_x'> " + value + "</span><br/>";
        $('#'+en[i]).html(show_content);
        }
    $('#save_link').css('display','none');
    save_to_backend(back_value);
}
//write blog
function write_blog(url){
	$('<div>').load(url,
        {
            'title': document.getElementById('articleTitle').value,
            'content': document.getElementById('articleContent').value},
		function()
        { 
            dialog.hide();
        	$('#deal').append($(this).html());
        });
}
//delte blog
function delete_blog(url, blog_id){
    //alert('ue');         
    var new_id = "#blog_content" + blog_id;
    //alert(new_id);
    
    $('<div>').load(url,
            {'blog_id': blog_id},
            function()
            {
               //alert('nimeiya'); 
                $("#blog_content_"+blog_id).text('');
            }
        );
    
}
/*
function ajaxFileUpload(){
    $.ajaxSetup(
    {
        url:'/update_avatar/',
        global:false,
        type:'POST',
        });
    $.ajax({data:
  */
    //alert('ue');         
    //var new_id = "#blog_content" + blog_id;
    //alert(new_id);
    /*
    $('<div>').load('/update_avatar/',
            {'avatar': document.getElementById('fileToUpload').value},
            function()
            {
               alert('nimeiya'); 
            }
        );
   
}*/


/*
ajax to send image file 
*/
function ajaxFileUpload()
{
	$("#loading").ajaxStart(function(){
		$(this).show();
	});
	$('#loading').ajaxComplete(function(){
		$(this).hide();
	});

	$.ajaxFileUpload
	(
	{
		url:'/update_avatar/',
		secureuri:true,
		fileElementId:'fileToUpload',
		dataType: 'json',
		beforeSend:function()
		{
			$("#loading").show();
		},
		complete:function()
		{
			$("#loading").hide();
		},				
		success: function (data, status)
		{
			if(typeof(data.error) != 'undefined')
			{
				if(data.error != '')
				{
					alert(data.error);
				}
				else
				{
					alert(data.msg);
				}
			}
			$('#avatar_form').hide();
			var json = eval(data);
			$('#image_src').attr("src",json.url);
		},
		error: function (data, status, e)
		{
			alert(e);
		}
	}
	)
	return false;
}


function show_picture_and_upload()
{
	$("#loading_img").ajaxStart(function(){
		$(this).show();
	});
	$('#loading_img').ajaxComplete(function(){
		$(this).hide();
	});
	$.ajaxFileUpload
	(
	{
		url:'/upload_blog_pic/',
		secureuri:true,
		fileElementId:'blog_image_file',
		dataType: 'json',
		success: function (data, status)
		{
			if(typeof(data.error) != 'undefined')
			{
				if(data.error != '')

				{
					alert(data.error);
				}
				else
				{
					alert(data.msg);
				}
			}
			var json = eval(data);
            alert(json);
		},
		error: function (data, status, e)
		{
            alert(e);
        }
    });
    return false;
}
function show_form(){
    if($('#avatar_form').css('display') == "none")
        $('#avatar_form').css('display','inline');
    else
        $('#avatar_form').css('display','none');
}
    /*
			function save_change(url){
				$('<div>').load(url,
					{'name':document.getElementById('wizard_name').value,
					 'hobby':document.getElementById('wizard_hobby').value,
					 'major':document.getElementById('wizard_major').value,
					 'img':  document.getElementById('wizard_img').value},
					function(){
						$('#deal').append('nihao');
					});
			}
	*/
