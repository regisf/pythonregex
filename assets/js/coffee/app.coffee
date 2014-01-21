# The application class. The main cotnroller
class cApplication
    constructor: ->
        @view = new cUIView
        @optionsDialog = new cOptionDialog

        $("#src_evaluate").on 'click', @evaluate.bind @

        @model = if window.WebSocket then new cModelSocket else new cModelAjax
        @model
            .connect Model.Signals.SendError, (msg) =>
                new cMessageDialog "Error", "Unable to connect the server #{msg}"

            .connect Model.Signals.SendSuccess, (data) =>
                if not data.success
                    new cMessageDialog "Error", data.error
                else
                    $("#dest_result").html "<pre><code>#{data.content}</code></pre>"

    getModel: -> @model

    evaluate: ->
        regex = $.trim $("#src_regex").val()
        content = $.trim $("#sourcetext").val()
        method = $("input[name=regex]:checked").val()
        options = []

        if $("#displaycommand").is "checked"
            options.push("displaycommand")

        options.push $(check).data 'name' for check in $("input[type=checkbox]:checked", "#regex_flags")

        if not regex.length
            new cMessageDialog 'Error', 'No regular expression entered'

        else if not content.length
            new cMessageDialog 'Error', "You must enter some text to evaluate"

        else
            sub = count = undefined

            if $("#sub").is ':checked'
                sub = $("input[name=replacement]").val()
            else if $("#subn").is ':checked'
                count = parseInt $("input[name=maxreplacement]").val()
                sub = $("input[name=subnreplacement]").val()
            else if $("#split").is ':checked'
                count = $("#maxsplit").is ':checked'

            @model.sendRegex regex, content, method, options, sub, count


# The application starter
$ ->
    # Ensure the footer is on the buttom of the screen
    $("#main").css "min-height", $(document).height() - $("footer#footer").height() - 70

    app = new cApplication
