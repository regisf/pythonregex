#
#
class cMessageDialog
    constructor: (title, msg) ->
        $("#messagedialog").find('[data-content]').html msg
        $("#messagedialog").find('[data-title]').html title

        $.UIkit.modal("#messagedialog").show();

    on: (signal, func) ->
        return