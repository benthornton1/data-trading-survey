// adapted from https://www.aspsnippets.com/Articles/Read-CSV-File-in-jQuery-using-HTML5-File-API.aspx
$(function () {
    $("#upload").bind("click", function () {
        var regex = /^([a-zA-Z0-9\s_\\.\-:])+(.csv|.txt)$/;
        if (regex.test($("#fileUpload").val().toLowerCase())) {
            if (typeof (FileReader) != "undefined") {
                var reader = new FileReader();
                reader.onload = function (e) {
                    var emails = e.target.result.split("\n");
                    for(var i = 0; i < emails.length; i++) {
                        $("#btnPlus").click()
                        var input = $(".recordset").last()
                        email = emails[i].split(",")[0]
                        input.find("input").val(email)
                    }
                }            
                reader.readAsText($("#fileUpload")[0].files[0]);
            } else {
                alert("This browser does not support HTML5.");
            }
        } else {
            alert("Please upload a valid CSV file.");
        }
    });
});