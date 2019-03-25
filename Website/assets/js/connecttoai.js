$("#analyseB").click(function(){
  $("#results").empty();
  var tccontract = $("#termsandconditions").val();
  var tcjson = {document : tccontract};
  var tcData = JSON.stringify(tcjson);

  if(!tccontract || tccontract.length < 500){
    $("#results").append("The text entered on the text area is not enough to be processed.");
  } else {
    $.ajax({
      type: 'POST',
      url: 'http://localhost:5000/ModelTest',
      data: tcData,
      cors: true,
      dataType: 'json',
      contentType: 'application/json',
      secure: true,
      timeout: 5000,
      success: function(data){
        if(!$.trim(data.rs)){
          $("#results").append("No Risky Statements found.");
        } else {
          $.each(data.rs, function(i, result){
            $("#results").append("<li>" + result + "</li>");
          })
        }
      },
      error: function(request, status, err){
        if (status == "timeout") {
          $("#results").append("Time out error. Server took too long to respond.");
        } else {
          $("#results").append("Error: " + request + status + err);
        }
      }
    });
  }
});
