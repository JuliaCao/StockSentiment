$(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.open($(this).data("href"), "_blank");
    });
    $(".clickable-row").each(function() {
      value = .8;
      // var value = $(this).data(value);
      if (value > 0) {
        $(this).css({"background-color": "rgba(0," + (value * 255) + ",0,0.6)"});
      } else if (value < 0) {
        $(this).css({"background-color": "rgba(" + (-value * 255) + ",0,0,0.6)"});
      } else {
        $(this).css({"background-color": "rgba(0,0,0,0.5)"});
      }

    })
});
