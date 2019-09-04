function readURL(input) {

  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      var target = $('#card-1-target-img');
      var img = "url('" + e.target.result + "')";
      target.css("background-image", img);
    }
    
    reader.readAsDataURL(input.files[0]);
  }
}
$("#card-1-target-img").on("click", function(){
  $("#card-1-upload").trigger("click");
});
//
$("#card-1-upload").on("change", function() {
  var fileName = $(this)[0].files[0].name;
  var label = $("#card-1-filename")
  label.html(fileName);
  readURL(this);
  var check = $("#card-1-check-it").removeClass("disabled");
  
});
//
$("#card-1-check-it").on("click", function(){
  var answer = $("#card-1-answer");
  var upload = $("#card-1-upload");
  var me = $(this);
  if (me.hasClass("disabled") == false) {
    answer.html('<i class="fas fa-yin-yang fa-spin"></i>');
    
    // post the data to /analyze
    var myUrl = "/analyze";
    var myData = new FormData($("#card-1-form")[0]); 
    me.addClass("disabled");
    upload.attr("disabled", "disabled");
    var handle = $.ajax({
      type: "POST",
      url: myUrl,
      data: myData,
      processData: false,
      contentType: false,
      dataType: "json",
      // process success data
      success: function(pdata, pstatus, pxhr) {
        var answer = $("#card-1-answer");
        p = " @" + Math.round(parseFloat(pdata.percent) * 100) + "%";
        s = pdata.result + p;
        answer.html(s);
        
      }
    });
    // 
    handle.fail(function(pdata, pstatus, pxhr){
      var answer = $("#card-1-answer");
      answer.html(pstatus)
    });
    //
    handle.always(function(pdata, pstatus, pxhr){
      var i = 0;
      var upload = $("#card-1-upload");
      var check = $("#card-1-check-it");
      upload.removeAttr("disabled");
      check.addClass("disabled");
      
    });
  }
});
//
