$(document).ready(function(){
    

    $(".add-heatmap").click(function(){
        var card_x_id = $("#card-x").children("option:selected").attr("card_id");
        var card_y_id = $("#card-y").children("option:selected").attr("card_id");
        var label_id = $("#label").children("option:selected").attr("label_id");
        var is_count = ($("#type").children("option:selected").attr("type") == 'true');
        var type = $(this).attr("type");

        $(".loading").empty();
        $(".loading").append("<div class='spinner-border text-primary mx-auto' role='status'><span class='sr-only'>Loading...</span></div>");

        var url = $(this).attr("url");
        var csrf_token = $(this).attr("csrf_token");

        var data = {}
        if(is_count == true){
            data = {'card_x_id':card_x_id, 'card_y_id':card_y_id, 'label_id':null, 'is_count':is_count, 'type':type}
        } else {
            data = {'card_x_id':card_x_id, 'card_y_id':card_y_id, 'label_id':label_id, 'is_count':is_count, 'type':type}
        }
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
                addHeatmaps(response)
            },
            error : function (response) {
                console.log(response);
            }
        });
    });

    function addHeatmaps(response) {
        $.each(response['plots'], function(key,value){
            var script = key
            var div = "<div class='col-xs heat-map'> "+value+" </div>"
            $("head").append(script)
            $(".heat-map-grid").append(div)
        });
        $(".loading").empty();
    }
    $( ".heat-map-grid" ).sortable({
        connectWith:".heat-map-grid"
    });


    $('.heat-map').mousemove(function(event){
        $(".selected").removeClass("selected");
        $(event.target).addClass("selected");
    });

    $( ".heat-map" ).mouseleave(function() {
        $(".selected").removeClass("selected");    
    });

    $('#remove-all-heatmaps').click(function(){
        $(".heat-map").remove();
    });


});
