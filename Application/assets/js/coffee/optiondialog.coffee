###
OptionDialogModel - Manage persistant options
###
class cOptionDialogModel
    constructor: ->
        @evaluateOnChange = false
        @liveEvaluation = false
        @shortTag = false
        @tags =
            debug: false,
            ignoreCase: false,
            multiline: false,
            dotAll: false,
            unicode: false,
            verbose: false

        if window.localStorage
            ls = window.localStorage
            @evaluateOnChange = ls.getItem 'opt_change' is '1';
            @liveEvaluation = ls.getItem 'opt_typing' is '1';
            @shortTag = ls.getItem 'opt_short' is '1';
            @tags.debug = ls.getItem 're_debug' is '1';
            @tags.ignoreCase = ls.getItem 're_ignore' is '1';
            @tags.multiline = ls.getItem 're_multiline' is '1';
            @tags.dotAll = ls.getItem 're_dotall' is '1';
            @tags.unicode = ls.getItem 're_unicode' is '1';
            @tags.verbose = ls.getItem 're_verbose' is '1';

    change: ->
        @evaluateOnChange = $("#opt_change").is ':checked'
        @liveEvaluation =   $("#opt_typing").is ':checked'
        @shortTag =         $("#opt_short").is ':checked'
        @tags.debug =       $("#re_debug").is ':checked'
        @tags.ignoreCase =  $("#re_ignore").is ':checked'
        @tags.multiline =   $("#re_multiline").is ':checked'
        @tags.dotAll =      $("#re_dotall").is ':checked'
        @tags.unicode =     $("#re_unicode").is ':checked'
        @tags.verbose =     $("#re_verbose").is ':checked'

        if window.localStorage
            ls = window.localStorage
            ls.setItem 'opt_change',  if @evaluateOnChange is true then '1' else '0'
            ls.setItem 'opt_typing',  if @liveEvaluation is true then '1' else '0'
            ls.setItem 'opt_short',   if @shortTag is true then '1' else '0'
            ls.setItem 're_debug',    if @tags.debug is true then '1' else '0'
            ls.setItem 're_ignore',   if @tags.ignoreCase is true then '1' else '0'
            ls.setItem 're_multiline',if @tags.multiline is true then '1' else '0'
            ls.setItem 're_dotall',   if @tags.dotAll is true then '1' else '0'
            ls.setItem 're_unicode',  if @.tags.unicode is true then '1' else '0'
            ls.setItem 're_verbose',  if @tags.verbose is true then '1' else '0'


###
OptionDialog - Manage UIKit dialog box
###
class cOptionDialog
    constructor: ->
        @model = new cOptionDialogModel
        $("#options").on 'click', '[data-ok]', @model.change.bind @model
        $("#options").on 'uk-model-show', @onOpen.bind @

    # The dialog is opened-> force options (on reload or load)
    onOpen: ->
        $("#opt_change").attr 'checked', @model.evaluateOnChange
        $("#opt_typing").attr 'checked', @model.liveEvaluation
        $("#opt_short").attr 'checked', @model.shortTag
        $("#re_debug").attr 'checked', @model.tags.debug
        $("#re_ignore").attr 'checked', @model.tags.ignoreCase
        $("#re_multiline").attr 'checked', @model.tags.multiline
        $("#re_dotall").attr 'checked', @model.tags.dotAll
        $("#re_unicode").attr 'checked', @model.tags.unicode
        $("#re_verbose").attr 'checked', @model.tags.verbose
