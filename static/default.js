// this function is based on the script at
// www.krijnhoetmer.nl/stuff/javascript/table-align-char/
var setupCharAligns = function() {
    $.each($('.char-align'), function(index, value) {
        var leftWidth = 0;
        $.each($(value).find('.left'), function(index, value) {
            if (leftWidth < $(value).innerWidth()) {
                leftWidth = $(value).innerWidth();
            }
        });
        $(value).find('.left').attr('style', 'width: '+leftWidth+'px;');
    });
}

$(function() {
    $('.net-button').click(function() {
        window.location.href += '/' + $(this).val();
    });

    setupCharAligns();
});
