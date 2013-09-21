 var dialog;
 function create(options){
                options = $.extend({title:'wuluostudio'}, options || {})
                dialog = new Boxy($('#upload_form'), options);
          	}
			    
 			
function uploadWork(url){
			$('<div>').load(url,
                        {

                        'workName': document.getElementById('name').value,
                        'workDescription': document.getElementById('description').value,
			'workDownloadUrl': document.getElementById('url').value},
			function()
                    	{ 
                        dialog.hide();
                    	$('#deal').append($(this).html());
                        });
		}
function delete_work(url, work_id){
                //alert('ue');         
                var new_id = "#work_" + work_id;
                //alert(new_id);
                
                $('<div>').load(url,
                        {'work_id': work_id},
                        function()
                        {
                           //alert('nimeiya'); 
                            $("#work_"+work_id).text('');
                        }
                    );
                
                }
			
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
