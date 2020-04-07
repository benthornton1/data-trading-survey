$(document).ready(function(){
    $(".compare-responses").click(function(){

        var csrf_token = $(this).attr("csrf_token")
        var url = $(this).attr("url")
        var response_id_1 = $("#response-1").children("option:selected").attr("response_id");
        var response_id_2 = $("#response-2").children("option:selected").attr("response_id");

        var data = {'response_id_1':response_id_1, 'response_id_2':response_id_2}
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
                compareResponses(response)
            },
            error : function (response) {
            }
        });

        function compareResponses(response){
            $(".responses").append(response['data'])
        }
    });

    $("#remove-all").click(function(){
       $(".responses").empty()
    });
});