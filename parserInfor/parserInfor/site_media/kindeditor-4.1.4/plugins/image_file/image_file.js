KindEditor.plugin('image_file', function(K) {
    var editor = this, name = 'image_file';
	// 点击图标时执行
	editor.clickToolbar(name, function() {
    //$('#image_div').css('display','inline');
	
    $('#image_div').dialog({
       buttons:{
        'upload': function(){
            show_picture_and_upload();
            }
        }
    );
    /*    
    var box1 = new Boxy($('#image_div').html(), //显示内容
         {
           	title: "上传文件", //对话框标题
            modal: false, //是否为模式窗口
            afterHide: function(e) {  }, //隐藏时的回调函数
            afterShow: function(e) {  }, //显示时的回调函数
            closeText: "X",   //关闭功能按钮的标题文字
            draggable: true //是否可以拖动
         });
	*/});
});
