$(document).ready(function(){
    

    $("#add-heatmap").click(function(){
        var card_x_id = $("#card-x").children("option:selected").attr("card_id");
        var card_y_id = $("#card-y").children("option:selected").attr("card_id");
        var type = $(this).attr("type");

        var url = $(this).attr("url");
        var csrf_token = $(this).attr("csrf_token");

        data = {'card_x_id':card_x_id, 'card_y_id':card_y_id, 'type':type}
    
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
            var div = "<div class='col-xs'> {{ "+value+" }} </div>"
            $("head").append(script)
            $("#heatmap-grid").append(div)
        });
    }

});
