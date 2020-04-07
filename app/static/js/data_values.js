$( document ).ready(function() {
    var val = $(".data-values").val()

    if(val == 1 ){
        $("#data_value_labels-0").parent().attr("hidden", false);
    } else if (val == 2) {
        $("#data_value_labels-0").parent().attr("hidden", false);
        $("#data_value_labels-1").parent().attr("hidden", false);
    }

    $(".data-values").on("change", function(){
        $(".item").attr("hidden", true);
        $("#data_value_labels-0").val('');
        $("#data_value_labels-1").val('');
        
        if($(".data-values").val() == 1 ){
            $("#data_value_labels-0").parent().attr("hidden", false);
        } else if ($(".data-values").val() == 2) {
            $("#data_value_labels-0").parent().attr("hidden", false);
            $("#data_value_labels-1").parent().attr("hidden", false);
        }
    });
});