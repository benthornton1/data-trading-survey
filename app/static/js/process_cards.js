$(document).ready(function(){


    $(function() {
        $( ".droptrue1" ).sortable({
        connectWith: ".droptrue1",
        forcePlaceholderSize: true
        });

        $( ".droptrue2" ).sortable({
        connectWith: ".droptrue2"
        });

        $( "ul.dropfalse" ).sortable({
        connectWith: "ul",
        dropOnEmpty: false
        });
        $( "#sortable-x #sortable-y" ).disableSelection();
    });


    $("a#submit").click(function(){
        	
        $( ".error" ).remove();
        if(($("#sortable-container-x").children().length > 0)){
            $('<div class="error alert alert-warning" role="alert">All cards must be placed on the X axis</div>').insertAfter("#sortable-container-x");
        }
        if(($("#sortable-container-y").children().length > 0)){
            $('<div class="error alert alert-warning" role="alert">All cards must be placed on the Y axis</div>').insertAfter("#sortable-container-y");
        }

        var cards_x = {}
        var cards_y = {}
        var data_values = {}

        $(".cards-row").each(function(){
            var row = $(this).attr("row")
            cards_y[row] = []
            $(".card", $(this)).each(function(){
                var card_id = parseInt($(this).attr("card_id"));
                var card_name = $(this).find(".title").text();
                var card_img = ""
                var card_desc = ""
                if($(this).find(".img") != ""){
                    card_path = $(this).find(".img").attr("src")
                    if(card_path !== "undefined" ){
                        card_path_split = card_path.split('/')
                        card_img = card_path_split[card_path_split.length-1]
                    }
                }
                if ($(this).find(".description").attr("title")){
                    card_desc = $(this).find(".title").attr("title");
                }
                card = {'id':card_id, 'name':card_name, 'image':card_img, 'description':card_desc} 
                cards_y[row].push(card)
            })        
        });

        $(".cards-col").each(function(){
            var col = $(this).attr("col")
            cards_x[col] = []
            $(".card", $(this)).each(function(){
                var card_id = parseInt($(this).attr("card_id"))
                var card_name = $(this).find(".title").text()
                var card_img = ""
                var card_desc = ""
                if($(this).find(".img")){
                    card_path = $(this).find(".img").attr("src")
                    if(typeof card_path !== "undefined" ){
                        card_path_split = card_path.split('/')
                        card_img = card_path_split[card_path_split.length-1]
                    }
                }
                if ($(this).find(".description").attr("title")){
                    card_desc = $(this).find(".title").attr("title")
                }
                card = {'id':card_id, 'name':card_name, 'image':card_img, 'description':card_desc}
                cards_x[col].push(card)
            });        
        });

        $(".data-values").each(function(){
            var col_row = $(this).attr("col-row");
            $(".data-value", $(this)).each(function(){
                var label = $(this).find("label").text()
                var label_id = parseInt($(this).find("label").attr("label_id"))
                var value = parseInt($(this).find("input").val())
                
                var col_row_split = col_row.split("_");
                var col = col_row_split[0].concat("_",col_row_split[1]);
                var row = col_row_split[2].concat("_", col_row_split[3]); 
                if((cards_x[col].length !== 0 )&&(cards_y[row].length !== 0)&&(isNaN(value))&&(!($(this).find(".alert").length))){
                    $('<span class="error" style="color: red;"><b>Must contain an integer.</b></span>').insertAfter(this);
                }
                var data_value = {}
                if(!(col in cards_x)||!(row in cards_y)){
                    data_value = {'id':label_id, 'label':label, 'value':NaN}
                } else {
                    data_value = {'id':label_id, 'label':label, 'value':value}
                }
                if(col_row in data_values){
                    data_values[col_row].push(data_value)
                } else {
                    data_values[col_row] = []
                    data_values[col_row].push(data_value)
                }
            });
        });
        if($('.error').length > 0 ){
            return;
        }

        var url = $(this).attr('url');
        var csrf_token = $(this).attr('csrf');

        var data = {'cards_x':cards_x, 'cards_y':cards_y, 'data_values':data_values}


        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token);
                }
            }
        });

        $.ajax({
            type : 'POST',
            url : url,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify(data),
            dataType: "json",
            success: function(response){
                window.location.href = response['url'];
            },
            error : function (response) {
                console.log(response);
            }
        
        });
    });
    });