$(document).ready(function() {
    $(".clickable-row").click(function() {
        window.open($(this).data("href"), "_blank");
    });
    $(".clickable-row").each(function() {
      var value = $(this).data("value");
      if (value > 0) {
        $(this).css('background-color', 'rgba(0,' + Math.round(value * 255) + ',0,0.6)');
      } else if (value < 0) {
        $(this).css("background-color", "rgba(" + Math.round(-value * 255) + ",0,0,0.6)");
      } else {
        $(this).css("background-color", "rgba(255,255,255,1)");
      }
    });
});
