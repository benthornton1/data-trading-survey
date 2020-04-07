$(document).ready(function(){
    
    $(".all-responses input:checkbox").click(function() {
        if ($("#all-responses").is(":checked")){
            $("#specific-responses").attr("disabled", true);
            $("#specific-responses").val([]);
        } else {
            $("#specific-responses").attr("disabled", false);    

        }
    });

    
    $(".create-pdf").click(function(){

        var csrf_token = $(this).attr("csrf_token");
        var url = $(this).attr("url");

        var all_responses = $("#all-responses").is(":checked");
        var average_response = $("#average-response").is(":checked");
        
        var response_ids = $(".specific-responses").children("option:selected").map(function(){return parseInt($(this).attr("response_id"));}).get();
        
        var data = {'all_responses':all_responses, 'average_response':average_response, 'response_ids':response_ids}
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
                download_pdf(response)
            },
            error : function (response) {
                console.log(response);
            }
        });

        function download_pdf(response) {
            var a = document.createElement('a');
            a.href = response['file_path'];
            a.id = "download"
            $("body").append(a);
            $("#download").attr("download", "")
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        }
        
    });
});