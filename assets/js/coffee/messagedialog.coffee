#
#
class cMessageDialog
    constructor: (title, msg) ->
        $("#messagedialog").find('[data-content]').html msg
        $("#messagedialog").find('[data-title]').html title

        new $.UIkit.modal("#messagedialog").show();

    on: (signal, func) ->
        return