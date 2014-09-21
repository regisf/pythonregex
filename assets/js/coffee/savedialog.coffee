#_require cobject

class SaveDialog extends cObject
    constructor: ->
        super()
        @saveDialog = $("#savedialog")
        @saveDialog.find("button#save").on 'click', @onSave.bind @
        @inputName = @saveDialog.find 'input[name=name]'

        @saveDialog.on 'uk.modal.show', () =>
            @inputName.val ''
            @emit Dialog.Signals.Open
            @inputName.focus()
            @saveDialog.find('i.uk-icon-spin').addClass 'uk-hidden'
            @saveDialog.find('i.uk-icon-times').removeClass 'uk-hidden'
            return

    onSave: ->
        # Get the name
        name = $.trim @inputName.val()

        # Ensure it's not empty
        if name == ''
            return

        @saveDialog.find('i').toggleClass 'uk-hidden'

        @emit Dialog.Signals.SaveSuccess, name
        return

    close: ->
        ($.UIkit.modal @saveDialog).hide()

    setName: (name) =>
        if typeof name == 'string'
            @inputName.val name