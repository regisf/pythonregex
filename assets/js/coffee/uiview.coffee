###
Class UIView
This class handle all views on the screen.
There's only one view because there isn't a lot of UIs
###

class cUIView
    constructor: ->
        @slideDown = true
        @storejQueryObjects()
        @forceCheck()
        @prepareUI()
        @connectUI()

    # Force the checkboxes value on reload
    forceCheck: ->
        for checked in $("input[type=radio]:checked")
            switch checked.getAttribute 'id'
                when 'split' then @displaySplitOptions()
                when 'sub'   then @displaySubOptions()
                when 'subn'  then @displaySubnOptions()
                when 'displaycommand' then @displayCommandLine()


    # Store all jQuery objects to avoid the DOM search on each
    # calls
    storejQueryObjects: ->
        @splitOptions = $("#splitoptions")
        @subnOptions = $("#subnoptions")
        @subOptions = $("#suboptions")
        @inputRadioSplit = $("input#split")
        @inputRadioSub = $("input#sub")
        @inputRadioSubn = $("input#subn")
        @inputFieldReplacement = $("input[name=replacement]")
        @inputFieldSubnreplacement = $("input[name=subnreplacement]")
        @inputFieldMaxreplacement = $("input[name=maxreplacement]")
        @inputFieldMaxsplit = $("input[name=maxsplit]")

    # Hide some elements (in case of)
    prepareUI: ->
        @splitOptions.hide()
        @subnOptions.hide()
        @subOptions.hide()

    # connect HTML elements
    connectUI: ->
        $("input[type=radio]").on 'click': (e) ->
            $("[data-option]").hide()

        @inputRadioSplit.on 'click', @displaySplitOptions.bind @
        @inputRadioSub.on 'click', @displaySubOptions.bind @
        @inputRadioSubn.on 'click', @displaySubnOptions.bind @
        $("input#displaycommand").on 'click', @displayCommandLine.bind @

    # Display options for re.split
    displaySplitOptions: (e) ->
        @inputFieldMaxsplit.val 0
        @splitOptions.show()

    # Display all re.sub options
    displaySubOptions: (e) ->
        @inputFieldReplacement.val ''
        @subOptions.show()

    # Display options for re.subn
    displaySubnOptions: (e) ->
        @inputFieldSubnreplacement.val ''
        @inputFieldMaxreplacement.val 0
        @subnOptions.show()

    # Display the python command line result
    displayCommandLine: (e) ->
        if $("#dest_result").html() isnt 'Not yet evaluated'
            $("#src_evaluate").trigger 'click'
        null

    # Display a fine little message
    displaySuccessMessage : (msg) ->
        $.UIkit.notify
            message : msg
            status  : 'success'
            timeout : 5000
            pos     : 'top-center'

