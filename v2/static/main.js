$(document).ready(function() {
    $(".clickable-row").click(function() {
        window.open($(this).data("href"), "_blank");
    });
    $(".clickable-row").each(function() {
      var value = parseFloat($(this).data("value"));
      if (value > 0) {
        $(this).css("background-color", "rgba(" + (255 - Math.round(value * 255)) + ",255,0,0.6)");
      } else if (value < 0) {
        $(this).css("background-color", "rgba(255," + Math.round((value+1) * 255) + ",0,0.6)");
      } else {
        $(this).css("background-color", "rgba(255,255,0,0.6)");
      }
    });
    $("#add-btn").click(function() {
      $(".input-field").css({"visibility": "visible"});
    });
    $("#get-btn").click(function() {
      var data = $("#ticker").val();
      if (data !== "") {
        $.post("/add/", { ticker: data }, function() {
          console.log(data);
          $.get("/");
          location.reload();
        });
      } else {

      }

    });
});
