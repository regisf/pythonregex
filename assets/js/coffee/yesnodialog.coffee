#
#
class YesNoDialog
    constructor: (title, msg) ->
        dialog = document.querySelector "#yesnodialog"

        dialog.querySelector("[data-content]").innerHTML = msg
        dialog.querySelector('[data-title]').innerHTML = title

    show: () ->
        new $.UIkit.modal("#yesnodialog").show()

    hide: () ->
        $("#yesnodialog").hide()

    on: (signal, func) ->
        document.querySelector("button##{signal}").onclick = func
        return