#_require cobject

#
# BaseModel is the base class for
#
class BaseModel extends cObject
    #
    # Interface for send a regex
    #
    sendRegex: (regex, content, method, options, sub, count) ->
        throw "saveRegex is not implemented"

    #
    # Interface for saving a regex. Must be called before real (ajax or ws save)
    #
    saveRegex: (name, regex) ->
        @setRegexName name

    #
    # Interface for delete a regex
    #
    deleteRegex: (id) ->
        throw "deleteRegex is not implementated"

    #
    # Save the regex and the source text
    #
    saveTempRegex: ->
        window.localStorage.setItem 'regex', document.getElementById("src_regex").value or ''
        window.localStorage.setItem 'sourcetext', document.getElementById("sourcetext").value or ''
        return

    #
    # Store the regex saved into the localStorage
    #
    setTempRegex: (regex) ->
        window.localStorage.setItem 'regex',  regex
        return

    #
    # Restore the stored regex.
    #
    restoreTempRegex: ->
        $("#src_regex").val (window.localStorage.getItem 'regex') or ''
        $("#sourcetext").val (window.localStorage.getItem 'sourcetext') or ''
        return

    #
    # Set the regex name
    #
    setRegexName: (name) ->
        window.localStorage.setItem 'regexname', name

    #
    # Get the regex name
    #
    getRegexName: ->
        name = window.localStorage.getItem 'regexname'
        console.log name
        if name == null or name == undefined
            return 'Untitled'
        return name

    #
    # Clear all stored data
    #
    clearLocal: ->
        window.localStorage.removeItem 'regex'
        window.localStorage.removeItem 'sourcetext'
        window.localStorage.removeItem 'regexname'
