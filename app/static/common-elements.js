$(document).ready(function() {
    // Expand the navigation menu to show the options
    $('#menu-button').click(function() {
        $('.navigation-menu').toggleClass('active');
    });

    // cancel icon to close the opened navigation menu
    $('#cancel-button').click(function() {
        $('.navigation-menu').toggleClass('active');
    });

    // To display the content for respective pages only by selecting side navigation bar option
    var currentUrl = window.location.pathname;
    $('.sidebar a').each(function() {
        var href = $(this).attr('href');
        if (currentUrl === href) {
            $(this).addClass('active');
        } else {
            $(this).removeClass('active');
        }
    });
});