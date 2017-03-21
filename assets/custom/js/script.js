$(function(ready) {
    $(".deleteButton").click(function() {
        var form = $(this).closest("form");
        var message = null;
        if (form.hasClass("deleteForm")) {
            message = "Do you want to delete this topic?";
        } else if (form.hasClass("subscribeForm")) {
            message = "On this email you will receive changes on hottest topics in last 24 hours.";
        } else if (form.hasClass("deleteCommentForm")) {
            message = "Do you want to delete this comment?"
        }

        if (confirm(message)) {
            form.submit();
        } else {
            return false;
        }
    });

    firstNumber = Math.floor(Math.random()*11);
    secondNumber = Math.floor(Math.random()*11);
    $("#generateNumber").html("What is the sum of " + firstNumber + " and " + secondNumber + "?");

    $("#add-topic-button").click(function() {
        var result = $("#checkResult").val();
        try {
            if (parseInt(result) === firstNumber + secondNumber) {
                $(this).prop("disabled", true);
            } else {
                alert("You are robot!");
                $("#checkResult").val("");
                return false;
            }
        } catch (err) {
            alert("You are robot!");
            $("#checkResult").val("");
            return false;
        }
    });
});