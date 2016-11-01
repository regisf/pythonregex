#
# The contact object manage the #contact dialog
#
class ContactMessage
    constructor: ->
        dialog = $("#contact")
        @emailField = dialog.find "input[name=email]"
        @nameField = dialog.find "input[name=name]"
        @answerField = dialog.find "input[name=question]"
        @messageField = dialog.find "textarea[name=message]"

        # Remove fields content
        dialog.on 'uk.modal.show', () =>
            @emailField.val ""
            @emailField.removeClass "uk-form-danger"
            @nameField.val ""
            @nameField.removeClass "uk-form-danger"
            @answerField.val ""
            @answerField.removeClass "uk-form-danger"
            @messageField.val ""
            @messageField.removeClass "uk-form-danger"

        dialog.find("[data-send]").on 'click', @validateForm

    # Validate the form to check errors
    validateForm: (e) =>
        error = [];
        if $.trim(@emailField.val()).length == 0
            @emailField.addClass "uk-form-danger"
            error.push "The email is empty"
        else
            @emailField.removeClass "uk-form-danger"

        if $.trim(@nameField.val()).length == 0
            @nameField.addClass "uk-form-danger"
            error.push "The name is empty"
        else
            @nameField.removeClass "uk-form-danger"

        if $.trim(@answerField.val()).length == 0
            @answerField.addClass "uk-form-danger"
            error.push "The answer is empty"

        else if @answerField.val() != $("#result").val()
            @answerField.addClass "uk-form-danger"
            error.push "This isn't the good answer"

        else
            @answerField.removeClass "uk-form-danger"

        if $.trim(@messageField.val()).length == 0
            @messageField.addClass "uk-form-danger"
            error.push "The message is empty"
        else
            @messageField.removeClass "uk-form-danger"

        if error.length
            e.preventDefault()
            alert "There is one or more error\n\n" + error.join "\n"
            return

        # Get the form
        formData = new FormData(document.getElementById("contactform"))

        # Display a wheel
        $("#form-container").slideUp 'fast', () ->
            $("#wheel-container").removeClass 'uk-hidden'
            @addClass 'uk-hidden'

        jqxhr = $.ajax
            url: '/contact'
            type: 'POST'
            data: formData
            processData: false
            contentType: false

        # Restore form
        jqxhr.always (data) ->
            $("#wheel-container").addClass 'uk-hidden'
            $("#form-container").attr 'style', '' # Remove all jQuery additionnal style

        jqxhr.done (data) ->
            if not data.match /^error/
                okModal = new $.UIkit.modal("#send-success")
                okModal.show()
            else
                errorModal = $.UIkit.modal("#connection-error")
                document.getElementById("connection-error-msg").innerHTML = data;
                errorModal.show()

        jqxhr.fail (xhr) ->
            errorModal = $.UIkit.modal("#connection-error")
            document.getElementById("connection-error-msg").innerHTML = xhr.responseText;
            errorModal.show()

        return

