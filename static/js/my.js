$(function() {

	var objects;
	var fuuid=null;

	var gdml_ready=false;


	$("#uploadform").submit(function(evt){	 
		evt.preventDefault();
		var fileSelect=$('#file');
		if(	fileSelect[0].files[0].size>10*1024*1024)
		{
			alert('File size must be <10 MB');
			return ;
		}
		$('#statusbar').html("Loading the file ... ");



		var data = new FormData($('#uploadform')[0]);
		$.ajax({
			xhr: function()
			{
				var xhr = new window.XMLHttpRequest();
				xhr.upload.addEventListener("progress", function(evt){
					if (evt.lengthComputable) {
						var percentComplete = evt.loaded*100. / evt.total;
						var per=(Math.round(percentComplete)).toFixed(2);
						$('#statusbar').html(per+'% loaded...');
					}
				}, false);
				return xhr;
			},

			url: 'upload',
			type: 'POST',
			data: data,
			cache: false,
			processData:false, 
			contentType: false, 
			enctype:'multipart/form-data',
			success: function(data, textStatus, jqXHR)
			{

				process(data);
			},
			error: function(jqXHR, textStatus, errorThrown)
			{
				$('#statusbar').html('ERRORS: ' + textStatus);
			}
		});
	});




	function process(data)
	{
		scene.remove.apply(scene, scene.children);
		objects=[];
		$('#leftbar').html('');
		console.log(data);
		if(data['status']=='error')
		{
			$('#statusbar').html('Failed to the load data from server');
			return;
		}
		if(data['status']=='ready')
		{
			$('#statusbar').html('Retrieving data from server ...');
			fuuid=data['fuuid'];
			var obs=data['obs'];
			$('#leftbar').append('<ul id="labellist">');
		$('#leftbar').show();

			var n_objects=obs.length;
			var n_loaded=0;

			for(i=0;i<n_objects;i++)
			{
				puuid=obs[i]['uuid'];
				label=obs[i]['label'];
				$('#leftbar').append('<li><input id="'+puuid+'" type="checkbox" checked>'+label+'</li>');
				var loc='/document/'+fuuid+'/'+puuid;
				var loader = new THREE.JSONLoader();
				$.getJSON(loc, function( json ) {
					var model=loader.parse(json);

					var col='#'+Math.floor(Math.random()*16777215).toString(16);
					var material=new THREE.MeshNormalMaterial({color:col});
					var object = new THREE.Mesh( model.geometry, material );
					object.castShadow = true;
					object.receiveShadow = true;
					scene.add(object );
					n_loaded++;
					if(n_loaded==n_objects)	fit_to_scene();
					puuid=json.metadata.userData;
					objects.push({object:object, puuid:puuid });
				});
			}

			$('#statusbar').html('loaded!');


			$('#leftbar').append('</ul>');
			setClickResponses();
		}


	}

	if (!(typeof fuuid_view=== "undefined")) {
		if(fuuid_view.length>0){
			$.getJSON( "/document/"+fuuid_view, function( data ) {
				process(data);
			});
		}
	}
	function setClickResponses()
	{
		$('input[type=checkbox]').on('click',function(e) {
			e.stopPropagation();
			var	sel_id=new String(this.id);
			console.log("look for:"+sel_id);
			var checked=$(this).prop("checked");


			for( i =0; i<objects.length;i++)
			{

				var uuid=new String(objects[i].puuid);
				console.log(typeof uuid);
				if(uuid.trim()==sel_id.trim())
				{
					var	selected_target=objects[i].object;
					selected_target.material.visible = checked;
					break;
				}
			}

		});
	}



});
