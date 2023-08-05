function myPopup() {

    var overlay = $('<div id="overlay"></div>');
    $('.x').click(function () {
        $('.popup').hide();
        overlay.appendTo(document.body).remove();
        return false;
    });
    var obj = document.getElementsByClassName('card-body');

    // alert("name");
    myScript = function () {
        overlay.show();
        overlay.appendTo(document.body);
        $('.popup').show();
        return false;
    };

    obj[0].addEventListener("click", myScript);

}