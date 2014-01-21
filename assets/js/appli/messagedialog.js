var MessageDialog = Class.extend({
    init: function(title, msg) {
        $("#messagedialog").find('[data-content]').html(msg);
        $("#messagedialog").find('[data-title]').html(title);
        new $.UIkit.modal.Modal("#messagedialog").show();
    }
});
