$(function(ready) {
    $(".deleteButton").click(function() {
        var form = $(this).closest("form");
        var message = null;
        if (form.hasClass("deleteForm")) {
            message = "Do you want to delete this topic?";
        } else if (form.hasClass("subscribeForm")) {
            message = "On this email you will receive changes on most hot topics in last 24 hours.";
        } else if (form.hasClass("deleteCommentForm")) {
            message = "Do you want to delete this comment?"
        }

        if (confirm(message)) {
            form.submit();
        } else {
            return false;
        }
    });
});