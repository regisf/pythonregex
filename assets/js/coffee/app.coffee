# The application class. The main controller
class cApplication
    constructor: ->
        @currentSave = null

        @view = new cUIView
        @optionsDialog = new cOptionDialog

        # Create the message dialog
        @contactDialog = new ContactMessage()

        @model = if window.WebSocket then new cModelSocket else new cModelAjax
        @model
            .connect Model.Signals.SendError, (msg) =>
                new cMessageDialog "Error", "Unable to connect the server #{msg}"
                return

            .connect Model.Signals.SendSuccess, (data) =>
                if not data.success
                    new cMessageDialog "Error", data.error
                else
                    $("#dest_result").html "<pre><code>#{data.content}</code></pre>"
                return

            .connect Model.Signals.SaveSuccess, (data) =>
                @saveDialog.close()

                if not data.success
                    new cMessageDialog "Error", data.error
                else
                    @view.displaySuccessMessage "Regular expression saved with success"
                    @currentSave = data.name
                return

            .connect Model.Signals.SaveError, (data) =>
                new cMessageDialog "Error", data
                return

        # Connect: Save the regex and source text into localStorage
        if document.location.pathname == '/'
            window.onunload = (e) =>
                @model.saveTempRegex()

            # Restore previous regex
            @model.restoreTempRegex()

            # Create the save dialog
            @saveDialog = new SaveDialog()
            @saveDialog.connect Dialog.Signals.Open, () =>
                @saveDialog.setName @model.getRegexName()

            @saveDialog.connect Dialog.Signals.SaveSuccess, (name) =>
                regex = $("#src_regex").val()
                @model.saveRegex name, regex

            $("#src_evaluate").on 'click', @evaluate.bind @
            document.getElementById('regex-name').textContent = @model.getRegexName()

        # Display notification
        for message in messages
            $.UIkit.notify
                message: message.message
                status: if not message.level then 'success' else 'danger'
                pos: 'top-center'
                timeout: 3000


        if document.location.pathname.indexOf "/user/regex/" != -1
            # Regex list
            @regexList = new RegexList
                delete: (id, cb) =>
                    @model.deleteRegex id, cb
                    return

                use: (regex, name) =>
                    @model.setTempRegex regex
                    @model.setRegexName name
                    document.location = '/'
                    return

        el = document.getElementById('clear-data')
        if el
            el.onclick = (e) =>
                e.preventDefault()
                @model.clearLocal()
                src = document.getElementById 'src_regex'
                if src
                    src.value = ''
                    document.getElementById('sourcetext').value = ''

                # Give feedback to the user
                document.location = '/'

        return

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
        @

# The application starter
$ ->
    # Ensure the footer is on the buttom of the screen
    $("#main").css "min-height", $(document).height() - $("footer#footer").height() - 70

    app = new cApplication()
    return