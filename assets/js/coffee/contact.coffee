#
# The contact object manage the #contact dialog
#
class ContactMessage
  constructor: ->
    dialog = $("#contact")
    @emailField = dialog.find "input[name=email]"
    @nameField = dialog.find "input[name=name]"
    @answerField = dialog.find "input[name=anwser]"
    @questionField = dialog.find "input[name=question]"
    @messageField = dialog.find "textarea[name=message]"

    # Remove fields content
    dialog.on 'uk.modal.show', () ->
      @emailField.val ""
      @nameField.val ""
      @answerField.val ""
      @questionField.val ""
      @messageField.val ""
      return

    dialog.find("[data-send]").on 'click', @validateForm

  # Validate the form to check errors
  validateForm: (e) =>
    error = false
    e.preventDefault()
    if $.trim(@emailField.val()).length == 0
      @emailField.addClass "uk-form-error"
      error = true

    if $.trim(@nameField.val()).length == 0
      @nameField.addClass "uk-form-error"
      error = true

    return

