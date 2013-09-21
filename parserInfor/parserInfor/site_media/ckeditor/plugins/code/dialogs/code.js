CKEDITOR.dialog.add(
	    "code",
	    function (a)
	    {
	        return {
	            title:"选择文件",
	            minWidth:200,
	            minHeight:100,
	            contents:
	            [
	                {
	                    id:"image_file",
	                    label:"image_file",
	                    title:"image_file",
	                    expand:true,
	                    padding:0,
	                    elements:
	                    [
	                        {
	                            type:"html",
								html:"<input id = 'image_file' type='file' value = 's'/ >",
	                        }
	                    ]
	                }
	            ],
	            onOk: function()
	            {
					alert('nih');
					this.imageElement = editor.document.createElement('img');
					this.imageElement.setAttribute('alt','nihao');
					this.imageElement.setAttribute('src',document.getElementById('image_file').value);
					editor.insertInnerHtml("sf");
					
	            }
	        };
	    }
	);
