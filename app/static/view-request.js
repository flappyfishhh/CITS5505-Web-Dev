$(document).ready(function() {
    // On clicking respond button, the response content section will be displayed
    $('.respond-button').click(function() {
        $('.respond-button').css('display', 'none');
        $('.response-content').css('display', 'block');
        $('.response-content .back-button').css('display', 'inline-block');
    });

    // On clicking back button, user can go back to view request page and response content section will be hidden
    $('.back-button').click(function() {
        $('.respond-button').css('display', 'block');
        $('.response-content').css('display', 'none');
    });

    // On clicking submit button, the response content section is hidden and back to view request page 
    $('.submit-button').click(function() {
        $('.respond-button').css('display', 'block');
        $('.response-content').css('display', 'none');
    });

});