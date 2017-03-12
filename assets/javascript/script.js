$(function(ready) {
    $("#deleteButton").click(function() {
        if (confirm("Do you want to delete this topic?")) {
            $("#formDelete").submit();
        } else {
            return false;
        }
    });
});
